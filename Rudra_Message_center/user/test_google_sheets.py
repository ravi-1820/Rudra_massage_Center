from datetime import timedelta
from io import StringIO
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from user.google_sheets import (
    APPROVED_SCHEMAS,
    WORKSHEET_APPOINTMENTS,
    WORKSHEET_CONTACTS,
    WORKSHEET_ENQUIRIES,
    enqueue_sync_record,
    get_sheets_config_diagnostics,
    get_sheets_service,
    get_spreadsheet_id,
    get_spreadsheet_metadata,
    get_worksheet_headers,
    process_pending_syncs,
    queue_backfill_records,
    sanitize_cell_value,
    sync_single_record,
    validate_or_init_header,
)
from user.models import Appointment, Category, Enquiry, GoogleSheetsSyncRecord, Service, SupportRequest


class GoogleSheetsConfigTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Wellness", slug="wellness", is_active=True)
        self.service = Service.objects.create(
            category=self.category,
            name="Therapy Machine",
            slug="therapy-machine",
            short_description="Test machine",
            description="Long description",
            is_active=True,
        )

    @override_settings(GOOGLE_SHEETS_ENABLED=False)
    def test_diagnostics_when_disabled(self):
        diag = get_sheets_config_diagnostics()
        self.assertFalse(diag["enabled"])
        self.assertFalse(diag["is_configured"])
        self.assertIn("Disabled", diag["status"])
        self.assertIsNone(get_sheets_service())

    @override_settings(
        GOOGLE_SHEETS_ENABLED=True,
        GOOGLE_SHEETS_SPREADSHEET_ID="",
        GOOGLE_SERVICE_ACCOUNT_FILE="",
    )
    def test_diagnostics_when_settings_empty(self):
        diag = get_sheets_config_diagnostics()
        self.assertTrue(diag["enabled"])
        self.assertFalse(diag["spreadsheet_id_configured"])
        self.assertFalse(diag["service_account_file_configured"])
        self.assertFalse(diag["service_account_file_exists"])
        self.assertFalse(diag["is_configured"])
        self.assertIsNone(get_sheets_service())
        self.assertIsNone(get_spreadsheet_id())

    @override_settings(
        GOOGLE_SHEETS_ENABLED=True,
        GOOGLE_SHEETS_SPREADSHEET_ID="sample_id_123",
        GOOGLE_SERVICE_ACCOUNT_FILE="C:\\nonexistent\\path\\creds.json",
    )
    def test_diagnostics_when_file_not_found(self):
        diag = get_sheets_config_diagnostics()
        self.assertTrue(diag["enabled"])
        self.assertTrue(diag["spreadsheet_id_configured"])
        self.assertTrue(diag["service_account_file_configured"])
        self.assertFalse(diag["service_account_file_exists"])
        self.assertFalse(diag["is_configured"])
        self.assertIn("not found", diag["status"])
        self.assertIsNone(get_sheets_service())

    def test_diagnostics_keys_contain_no_sensitive_values(self):
        diag = get_sheets_config_diagnostics()
        allowed_keys = {
            "enabled",
            "spreadsheet_id_configured",
            "service_account_file_configured",
            "service_account_file_exists",
            "library_installed",
            "is_configured",
            "status",
        }
        self.assertEqual(set(diag.keys()), allowed_keys)
        for k, v in diag.items():
            if k == "status":
                self.assertIsInstance(v, str)
            else:
                self.assertIsInstance(v, bool)

    def test_management_command_check_sheets_config(self):
        out = StringIO()
        call_command("check_sheets_config", stdout=out)
        output = out.getvalue()
        self.assertIn("Google Sheets Configuration Diagnostics", output)
        self.assertIn("Integration Enabled:", output)
        self.assertIn("Overall Integration Ready:", output)


class GoogleSheetsSecurityAndSanitizationTests(TestCase):
    def test_formula_injection_sanitization(self):
        # Characters that can trigger formulas: =, +, -, @, \t, \r, %
        self.assertEqual(sanitize_cell_value("=HYPERLINK('badurl')"), "'=HYPERLINK('badurl')")
        self.assertEqual(sanitize_cell_value("+1234567890"), "'+1234567890")
        self.assertEqual(sanitize_cell_value("-500"), "'-500")
        self.assertEqual(sanitize_cell_value("@SUM(A1:A10)"), "'@SUM(A1:A10)")
        self.assertEqual(sanitize_cell_value("\tcmd"), "'\tcmd")
        self.assertEqual(sanitize_cell_value("\rcmd"), "'\rcmd")
        self.assertEqual(sanitize_cell_value("%20discount"), "'%20discount")

        # Safe normal values should remain unchanged
        self.assertEqual(sanitize_cell_value("Ramesh Patel"), "Ramesh Patel")
        self.assertEqual(sanitize_cell_value("9825012345"), "9825012345")
        self.assertEqual(sanitize_cell_value("Ahmedabad"), "Ahmedabad")
        self.assertEqual(sanitize_cell_value(""), "")
        self.assertEqual(sanitize_cell_value(None), "")


class DatabaseFirstSubmissionSyncQueueTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Machines", slug="machines", is_active=True)
        self.service = Service.objects.create(
            category=self.category,
            name="Spine Traction Unit",
            slug="spine-traction",
            short_description="Decompression unit",
            description="Spinal relief",
            is_active=True,
        )

    def test_appointment_submission_enqueues_sync_record(self):
        tomorrow = (timezone.localdate() + timedelta(days=2)).strftime("%Y-%m-%d")
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("user:appointment"),
                {
                    "name": "Kavita Shah",
                    "phone": "9825011223",
                    "email": "kavita@example.com",
                    "city": "Ahmedabad",
                    "service": self.service.id,
                    "appointment_date": tomorrow,
                    "time_slot": "morning",
                    "demo_format": "centre",
                    "notes": "Testing db-first appointment queueing",
                },
                follow=True,
            )
        self.assertEqual(response.status_code, 200)

        # Database record exists
        apt = Appointment.objects.get(phone="9825011223")
        self.assertEqual(apt.name, "Kavita Shah")

        # Sync record was created in database
        sync_rec = GoogleSheetsSyncRecord.objects.get(
            source_type=GoogleSheetsSyncRecord.SourceType.APPOINTMENT,
            source_id=apt.id,
        )
        self.assertEqual(sync_rec.status, GoogleSheetsSyncRecord.SyncStatus.PENDING)
        self.assertEqual(sync_rec.source_identifier, apt.booking_reference)

    def test_enquiry_submission_enqueues_sync_record(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("user:enquiry"),
                {
                    "name": "Pranav Mehta",
                    "phone": "9825044556",
                    "email": "pranav@example.com",
                    "city": "Surat",
                    "service": self.service.id,
                    "enquiry_type": "therapy_machine",
                    "preferred_contact_method": "phone",
                    "usage_intention": "personal",
                    "callback_time": "morning",
                    "message": "Interested in home trial",
                },
                follow=True,
            )
        self.assertEqual(response.status_code, 200)

        enq = Enquiry.objects.get(phone="9825044556")
        self.assertEqual(enq.name, "Pranav Mehta")

        sync_rec = GoogleSheetsSyncRecord.objects.get(
            source_type=GoogleSheetsSyncRecord.SourceType.ENQUIRY,
            source_id=enq.id,
        )
        self.assertEqual(sync_rec.status, GoogleSheetsSyncRecord.SyncStatus.PENDING)
        self.assertEqual(sync_rec.source_identifier, f"ENQ-{enq.id}")

    def test_contact_submission_enqueues_sync_record(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("user:contact"),
                {
                    "name": "Mitesh Joshi",
                    "email": "mitesh@example.com",
                    "phone": "9825099887",
                    "subject": "Other",
                    "message": "General query about warranty",
                },
                follow=True,
            )
        self.assertEqual(response.status_code, 200)

        sr = SupportRequest.objects.get(phone="9825099887")
        self.assertEqual(sr.name, "Mitesh Joshi")

        sync_rec = GoogleSheetsSyncRecord.objects.get(
            source_type=GoogleSheetsSyncRecord.SourceType.SUPPORT_REQUEST,
            source_id=sr.id,
        )
        self.assertEqual(sync_rec.status, GoogleSheetsSyncRecord.SyncStatus.PENDING)
        self.assertEqual(sync_rec.source_identifier, sr.ticket_number)


class GoogleSheetsSyncEngineMockedTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Equip", slug="equip", is_active=True)
        self.service = Service.objects.create(
            category=self.category,
            name="Bed Machine",
            slug="bed-machine",
            short_description="Bed",
            description="Bed desc",
            is_active=True,
        )
        self.enquiry = Enquiry.objects.create(
            name="Aarav Sharma",
            phone="9825012345",
            email="aarav@example.com",
            city="Ahmedabad",
            service=self.service,
            service_name_snapshot=self.service.name,
            enquiry_type="therapy_machine",
            usage_intention="personal",
            callback_time="morning",
            preferred_contact_method="phone",
            message="Need delivery details",
            status="new",
        )
        self.sync_record = enqueue_sync_record(
            GoogleSheetsSyncRecord.SourceType.ENQUIRY,
            self.enquiry.id,
            f"ENQ-{self.enquiry.id}",
        )

    def test_header_initialization_when_empty(self):
        mock_service = MagicMock()
        # Row 1 get returns empty
        mock_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = {
            "values": []
        }

        res = validate_or_init_header(
            service=mock_service,
            spreadsheet_id="test_sheet_id",
            sheet_name=WORKSHEET_ENQUIRIES,
            init_if_empty=True,
            dry_run=False,
        )

        self.assertTrue(res["valid"])
        self.assertTrue(res["initialized"])
        # Update called with approved headers
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()
        call_kwargs = mock_service.spreadsheets.return_value.values.return_value.update.call_args[1]
        self.assertEqual(call_kwargs["body"]["values"], [APPROVED_SCHEMAS[WORKSHEET_ENQUIRIES]])

    def test_header_validation_detects_schema_mismatch_and_halts(self):
        mock_service = MagicMock()
        # Row 1 returns mismatched header
        mock_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = {
            "values": [["Wrong Col 1", "Wrong Col 2"]]
        }

        res = validate_or_init_header(
            service=mock_service,
            spreadsheet_id="test_sheet_id",
            sheet_name=WORKSHEET_ENQUIRIES,
            init_if_empty=True,
            dry_run=False,
        )

        self.assertFalse(res["valid"])
        self.assertEqual(res["error_type"], "schema_mismatch")
        # Ensure update was NOT called
        mock_service.spreadsheets.return_value.values.return_value.update.assert_not_called()

    def test_sync_single_record_inserts_new_row_when_not_in_sheet(self):
        mock_service = MagicMock()
        # Header check returns valid matching headers
        mock_get = mock_service.spreadsheets.return_value.values.return_value.get.return_value
        mock_get.execute.side_effect = [
            {"values": [APPROVED_SCHEMAS[WORKSHEET_ENQUIRIES]]},  # Row 1 headers
            {"values": [["Enquiry ID"], ["ENQ-998"], ["ENQ-999"]]},  # Column A (ID not present)
        ]

        res = sync_single_record(
            sync_record=self.sync_record,
            service=mock_service,
            spreadsheet_id="test_id",
            dry_run=False,
            init_headers=True,
        )

        self.assertTrue(res["success"])
        self.assertEqual(res["action"], "appended")
        # append called
        mock_service.spreadsheets.return_value.values.return_value.append.assert_called_once()
        self.sync_record.refresh_from_db()
        self.assertEqual(self.sync_record.status, GoogleSheetsSyncRecord.SyncStatus.SYNCED)
        self.assertEqual(self.sync_record.sheet_name, WORKSHEET_ENQUIRIES)

    def test_sync_single_record_updates_existing_row_when_found(self):
        mock_service = MagicMock()
        # Column A has ENQ-1 at row 3
        mock_get = mock_service.spreadsheets.return_value.values.return_value.get.return_value
        mock_get.execute.side_effect = [
            {"values": [APPROVED_SCHEMAS[WORKSHEET_ENQUIRIES]]},  # Row 1 headers
            {"values": [["Enquiry ID"], ["ENQ-998"], [f"ENQ-{self.enquiry.id}"]]},  # Row 3 matches
        ]

        res = sync_single_record(
            sync_record=self.sync_record,
            service=mock_service,
            spreadsheet_id="test_id",
            dry_run=False,
            init_headers=True,
        )

        self.assertTrue(res["success"])
        self.assertEqual(res["action"], "updated")
        self.assertEqual(res["row_index"], 3)
        # update called targeting row 3
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()
        call_kwargs = mock_service.spreadsheets.return_value.values.return_value.update.call_args[1]
        self.assertIn("A3:", call_kwargs["range"])

        self.sync_record.refresh_from_db()
        self.assertEqual(self.sync_record.status, GoogleSheetsSyncRecord.SyncStatus.SYNCED)
        self.assertEqual(self.sync_record.row_index, 3)

    def test_sync_single_record_halts_on_duplicate_identifiers(self):
        mock_service = MagicMock()
        # Column A has duplicate ENQ-1 at row 2 and row 4
        mock_get = mock_service.spreadsheets.return_value.values.return_value.get.return_value
        mock_get.execute.side_effect = [
            {"values": [APPROVED_SCHEMAS[WORKSHEET_ENQUIRIES]]},
            {"values": [["Enquiry ID"], [f"ENQ-{self.enquiry.id}"], ["ENQ-55"], [f"ENQ-{self.enquiry.id}"]]},
        ]

        res = sync_single_record(
            sync_record=self.sync_record,
            service=mock_service,
            spreadsheet_id="test_id",
            dry_run=False,
            init_headers=True,
        )

        self.assertFalse(res["success"])
        self.assertEqual(res["error_type"], "duplicate_identifier")
        # Neither append nor update called
        mock_service.spreadsheets.return_value.values.return_value.append.assert_not_called()
        mock_service.spreadsheets.return_value.values.return_value.update.assert_not_called()

        self.sync_record.refresh_from_db()
        self.assertEqual(self.sync_record.status, GoogleSheetsSyncRecord.SyncStatus.FAILED)
        self.assertEqual(self.sync_record.last_error_category, "duplicate_identifier")

    def test_sync_single_record_dry_run_performs_no_writes(self):
        mock_service = MagicMock()
        mock_get = mock_service.spreadsheets.return_value.values.return_value.get.return_value
        mock_get.execute.side_effect = [
            {"values": [APPROVED_SCHEMAS[WORKSHEET_ENQUIRIES]]},
            {"values": [["Enquiry ID"], ["ENQ-998"]]},
        ]

        res = sync_single_record(
            sync_record=self.sync_record,
            service=mock_service,
            spreadsheet_id="test_id",
            dry_run=True,
            init_headers=True,
        )

        self.assertTrue(res["success"])
        self.assertEqual(res["action"], "would_append")
        mock_service.spreadsheets.return_value.values.return_value.append.assert_not_called()
        mock_service.spreadsheets.return_value.values.return_value.update.assert_not_called()

    def test_backoff_retry_calculation(self):
        # Attempt 1 -> 1 min backoff
        self.sync_record.mark_failed("api_error", "Timeout")
        self.assertEqual(self.sync_record.attempts, 0)
        self.assertIsNotNone(self.sync_record.next_retry_at)

        self.sync_record.attempts = 5
        self.sync_record.mark_failed("api_error", "Persistent error")
        self.assertIsNone(self.sync_record.next_retry_at)  # Terminal failure after max attempts

    def test_backfill_queues_existing_records(self):
        # Create un-synced appointment
        tomorrow = timezone.localdate() + timedelta(days=3)
        apt = Appointment.objects.create(
            name="Deepak Patel",
            phone="9825066778",
            city="Ahmedabad",
            service=self.service,
            service_name_snapshot=self.service.name,
            appointment_date=tomorrow,
            time_slot="morning",
            demo_format="centre",
        )

        queued = queue_backfill_records(source_type=GoogleSheetsSyncRecord.SourceType.APPOINTMENT)
        self.assertGreaterEqual(queued, 1)

        sync_rec = GoogleSheetsSyncRecord.objects.get(
            source_type=GoogleSheetsSyncRecord.SourceType.APPOINTMENT,
            source_id=apt.id,
        )
        self.assertEqual(sync_rec.source_identifier, apt.booking_reference)


class GoogleSheetsManagementCommandsTests(TestCase):
    @patch("user.management.commands.init_sheets_headers.get_sheets_config_diagnostics")
    @patch("user.management.commands.init_sheets_headers.validate_or_init_header")
    @patch("user.management.commands.init_sheets_headers.get_sheets_service")
    def test_init_sheets_headers_command(self, mock_get_service, mock_validate, mock_diag):
        mock_diag.return_value = {"is_configured": True, "status": "Ready"}
        mock_get_service.return_value = MagicMock()
        mock_validate.return_value = {
            "valid": True,
            "initialized": True,
            "message": "Initialized Row 1",
        }

        out = StringIO()
        call_command("init_sheets_headers", stdout=out)
        output = out.getvalue()

        self.assertIn("Google Sheets Header Management", output)
        self.assertIn("Checking Worksheet: [Enquiries]", output)
        self.assertIn("INITIALIZED", output)

    @patch("user.management.commands.sync_google_sheets.get_sheets_config_diagnostics")
    @patch("user.management.commands.sync_google_sheets.process_pending_syncs")
    @patch("user.management.commands.sync_google_sheets.get_sheets_service")
    def test_sync_google_sheets_command(self, mock_get_service, mock_process, mock_diag):
        mock_diag.return_value = {"is_configured": True, "status": "Ready"}
        mock_get_service.return_value = MagicMock()
        mock_process.return_value = {
            "processed": 2,
            "succeeded": 2,
            "failed": 0,
            "dry_run": False,
            "records": [
                {
                    "source_type": "enquiry",
                    "source_identifier": "ENQ-1",
                    "result": {"success": True, "action": "appended", "sheet_name": "Enquiries", "row_index": 2},
                }
            ],
        }

        out = StringIO()
        call_command("sync_google_sheets", "--limit", "10", stdout=out)
        output = out.getvalue()

        self.assertIn("Google Sheets Synchronization Engine", output)
        self.assertIn("Batch Results Summary:", output)
        self.assertIn("Processed: 2", output)
        self.assertIn("Succeeded: 2", output)

    @patch("user.management.commands.sync_google_sheets.get_sheets_config_diagnostics")
    @patch("user.management.commands.sync_google_sheets.process_pending_syncs")
    @patch("user.management.commands.sync_google_sheets.get_sheets_service")
    def test_sync_google_sheets_command_with_explicit_filters(self, mock_get_service, mock_process, mock_diag):
        mock_diag.return_value = {"is_configured": True, "status": "Ready"}
        mock_get_service.return_value = MagicMock()
        mock_process.return_value = {
            "processed": 1,
            "succeeded": 1,
            "failed": 0,
            "dry_run": True,
            "records": [
                {
                    "source_type": "appointment",
                    "source_identifier": "APT-TEST-123",
                    "result": {"success": True, "action": "would_append", "sheet_name": "Appoinments", "row_index": 2},
                }
            ],
        }

        out = StringIO()
        call_command(
            "sync_google_sheets",
            "--source-type", "appointment",
            "--identifier", "APT-TEST-123",
            "--dry-run",
            stdout=out,
        )
        output = out.getvalue()

        self.assertIn("Running in DRY-RUN mode", output)
        self.assertIn("APT-TEST-123", output)
        mock_process.assert_called_once()
        _, kwargs = mock_process.call_args
        self.assertEqual(kwargs.get("source_type"), "appointment")
        self.assertEqual(kwargs.get("identifier"), "APT-TEST-123")
        self.assertTrue(kwargs.get("dry_run"))

    @patch("user.google_sheets.sync_single_record")
    def test_process_pending_syncs_filtering(self, mock_sync_single):
        mock_sync_single.return_value = {"success": True, "action": "synced"}
        # Create 3 records: enquiry, appointment, support_request
        r1 = GoogleSheetsSyncRecord.objects.create(
            source_type=GoogleSheetsSyncRecord.SourceType.ENQUIRY,
            source_id=101,
            source_identifier="ENQ-101",
            status=GoogleSheetsSyncRecord.SyncStatus.PENDING,
        )
        r2 = GoogleSheetsSyncRecord.objects.create(
            source_type=GoogleSheetsSyncRecord.SourceType.APPOINTMENT,
            source_id=202,
            source_identifier="APT-202",
            status=GoogleSheetsSyncRecord.SyncStatus.PENDING,
        )
        r3 = GoogleSheetsSyncRecord.objects.create(
            source_type=GoogleSheetsSyncRecord.SourceType.SUPPORT_REQUEST,
            source_id=303,
            source_identifier="SR-303",
            status=GoogleSheetsSyncRecord.SyncStatus.PENDING,
        )

        res = process_pending_syncs(
            source_type=GoogleSheetsSyncRecord.SourceType.APPOINTMENT,
            identifier="APT-202",
            dry_run=True,
            service=MagicMock(),
            spreadsheet_id="test_id",
        )

        self.assertEqual(res["processed"], 1)
        self.assertEqual(len(res["records"]), 1)
        self.assertEqual(res["records"][0]["source_identifier"], "APT-202")
        mock_sync_single.assert_called_once()
        call_sync_record = mock_sync_single.call_args[1]["sync_record"]
        self.assertEqual(call_sync_record.source_identifier, "APT-202")


class CustomAdminGoogleSheetsViewsTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="admin_staff",
            password="testpassword123",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="regular_user",
            password="testpassword123",
            is_staff=False,
        )
        self.sync_record = GoogleSheetsSyncRecord.objects.create(
            source_type=GoogleSheetsSyncRecord.SourceType.ENQUIRY,
            source_id=999,
            source_identifier="ENQ-999",
            status=GoogleSheetsSyncRecord.SyncStatus.FAILED,
            attempts=1,
            last_error_category="connection_error",
            last_error_message="Network timeout",
        )

    def test_monitor_view_requires_authentication(self):
        response = self.client.get(reverse("custom_admin:google_sheets_sync"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_monitor_view_rejects_non_staff(self):
        self.client.login(username="regular_user", password="testpassword123")
        response = self.client.get(reverse("custom_admin:google_sheets_sync"))
        self.assertEqual(response.status_code, 403)

    def test_monitor_view_accessible_by_staff(self):
        self.client.login(username="admin_staff", password="testpassword123")
        response = self.client.get(reverse("custom_admin:google_sheets_sync"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "custom_admin/google_sheets_sync.html")
        self.assertContains(response, "Google Sheets Synchronization Monitor")
        self.assertContains(response, "ENQ-999")

    def test_retry_view_rejects_get(self):
        self.client.login(username="admin_staff", password="testpassword123")
        response = self.client.get(reverse("custom_admin:google_sheets_retry", args=[self.sync_record.id]))
        self.assertEqual(response.status_code, 405)  # POST only

    @patch("user.google_sheets.sync_single_record")
    def test_retry_view_executes_on_post(self, mock_sync):
        mock_sync.return_value = {"success": True, "action": "synced"}
        self.client.login(username="admin_staff", password="testpassword123")
        response = self.client.post(
            reverse("custom_admin:google_sheets_retry", args=[self.sync_record.id]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        mock_sync.assert_called_once()
