"""
Google Sheets Integration Service for Rudra Massage & Wellness.

Securely initializes the Google Sheets API client using service account
credentials and provides safe configuration diagnostics, idempotent header
initialization, database-first synchronization, exponential backoff retries,
and formula injection protection.
"""

import logging
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

# Scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

READONLY_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

# Approved Worksheet Names (preserved exact spelling)
WORKSHEET_ENQUIRIES = "Enquiries"
WORKSHEET_APPOINTMENTS = "Appoinments"  # Preserved exact existing spelling
WORKSHEET_CONTACTS = "Contacts"

# Approved Schemas (Row 1 Column Headers)
ENQUIRY_HEADERS = [
    "Enquiry ID",
    "Date & Time",
    "Full Name",
    "Phone Number",
    "Email",
    "City",
    "Machine / Service",
    "Enquiry Type",
    "Usage Intention",
    "Preferred Call Time",
    "Contact Method",
    "Message / Notes",
    "Status",
]

APPOINTMENT_HEADERS = [
    "Booking Ref",
    "Booking Date",
    "Client Name",
    "Phone Number",
    "Email",
    "City",
    "Therapy Machine",
    "Appointment Date",
    "Time Slot",
    "Demo Format",
    "Special Notes",
    "Status",
]

SUPPORT_REQUEST_HEADERS = [
    "Ticket Number",
    "Created At",
    "Name",
    "Email",
    "Phone",
    "Request Type",
    "Subject",
    "Product Name",
    "Message",
    "Status",
]

APPROVED_SCHEMAS: Dict[str, List[str]] = {
    WORKSHEET_ENQUIRIES: ENQUIRY_HEADERS,
    WORKSHEET_APPOINTMENTS: APPOINTMENT_HEADERS,
    WORKSHEET_CONTACTS: SUPPORT_REQUEST_HEADERS,
}


def sanitize_cell_value(val: Any) -> Any:
    """
    Prevents spreadsheet formula injection by prepending a single quote (')
    if the string begins with =, +, -, @, tab, carriage return, or %.
    """
    if val is None:
        return ""
    if not isinstance(val, str):
        val = str(val)
    if not val:
        return ""
    # Strip only standard spaces on the left to preserve tab/carriage return detection
    leading = val.lstrip(" ")
    if leading and leading[0] in ("=", "+", "-", "@", "\t", "\r", "%"):
        return f"'{val}"
    return val



def get_sheets_config_diagnostics() -> Dict[str, Any]:
    """
    Returns safe configuration diagnostics for Google Sheets.
    Reports only boolean flags and status summaries.
    Never returns or logs actual credential values, file contents, or private keys.
    """
    enabled = getattr(settings, "GOOGLE_SHEETS_ENABLED", False)
    spreadsheet_id = (
        getattr(settings, "GOOGLE_SHEETS_SPREADSHEET_ID", "") or ""
    ).strip()
    service_account_file = (
        getattr(settings, "GOOGLE_SERVICE_ACCOUNT_FILE", "") or ""
    ).strip()

    file_exists = False
    if service_account_file:
        try:
            file_exists = Path(service_account_file).is_file()
        except Exception:
            file_exists = False

    library_installed = False
    try:
        import google.auth  # noqa: F401
        import googleapiclient.discovery  # noqa: F401

        library_installed = True
    except ImportError:
        library_installed = False

    is_configured = (
        enabled
        and bool(spreadsheet_id)
        and bool(service_account_file)
        and file_exists
        and library_installed
    )

    if not enabled:
        status = "Disabled (GOOGLE_SHEETS_ENABLED is False)"
    elif not library_installed:
        status = "Missing required libraries (google-api-python-client, google-auth)"
    elif not spreadsheet_id:
        status = "Missing GOOGLE_SHEETS_SPREADSHEET_ID"
    elif not service_account_file:
        status = "Missing GOOGLE_SERVICE_ACCOUNT_FILE"
    elif not file_exists:
        status = "Service account credential file not found at configured path"
    else:
        status = "Configured (Ready for operation)"

    return {
        "enabled": bool(enabled),
        "spreadsheet_id_configured": bool(spreadsheet_id),
        "service_account_file_configured": bool(service_account_file),
        "service_account_file_exists": file_exists,
        "library_installed": library_installed,
        "is_configured": is_configured,
        "status": status,
    }


def get_sheets_service(readonly: bool = False):
    """
    Initializes and returns the Google Sheets API Resource service if configured.
    Uses readonly=True for read-only operations and readonly=False for write operations.
    Exceptions are caught and logged safely without exposing private key or token details.
    """
    diagnostics = get_sheets_config_diagnostics()
    if not diagnostics["is_configured"]:
        logger.debug(
            "Google Sheets integration is not active: %s",
            diagnostics["status"],
        )
        return None

    service_account_file = getattr(
        settings, "GOOGLE_SERVICE_ACCOUNT_FILE", ""
    ).strip()

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        selected_scopes = READONLY_SCOPES if readonly else SCOPES
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=selected_scopes,
        )
        service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
        return service
    except Exception as e:
        logger.warning(
            "Failed to initialize Google Sheets service client: %s",
            e.__class__.__name__,
        )
        return None


def get_spreadsheet_id() -> Optional[str]:
    """
    Returns the configured spreadsheet ID if non-empty, or None.
    """
    spreadsheet_id = (
        getattr(settings, "GOOGLE_SHEETS_SPREADSHEET_ID", "") or ""
    ).strip()
    return spreadsheet_id or None


def get_spreadsheet_metadata(service=None, spreadsheet_id: Optional[str] = None, readonly: bool = True) -> Dict[str, Any]:
    """
    Safely reads spreadsheet metadata (title and worksheet tab names) only.
    Uses the narrowest required scope by default.
    Does NOT read, export, or write any cell data or customer records.
    """
    target_id = (spreadsheet_id or get_spreadsheet_id() or "").strip()
    if not target_id:
        return {
            "success": False,
            "error_type": "missing_spreadsheet_id",
            "message": "Spreadsheet ID is not configured. Please set GOOGLE_SHEETS_SPREADSHEET_ID.",
        }

    if service is None:
        service = get_sheets_service(readonly=readonly)

    if not service:
        diag = get_sheets_config_diagnostics()
        return {
            "success": False,
            "error_type": "initialization_failed",
            "message": f"Could not initialize Google Sheets service: {diag['status']}",
        }

    try:
        metadata = (
            service.spreadsheets()
            .get(
                spreadsheetId=target_id,
                fields="properties.title,sheets.properties.title,sheets.properties.sheetId",
            )
            .execute()
        )

        title = metadata.get("properties", {}).get("title", "Untitled Spreadsheet")
        sheets = metadata.get("sheets", [])
        sheet_names = [
            sheet.get("properties", {}).get("title", "")
            for sheet in sheets
            if sheet.get("properties", {}).get("title")
        ]

        return {
            "success": True,
            "title": title,
            "worksheets": sheet_names,
            "worksheet_count": len(sheet_names),
            "message": "Connection successful.",
        }

    except Exception as exc:
        err_str = str(exc).lower()
        status_code = getattr(getattr(exc, "resp", None), "status", None)

        if status_code == 403 or "403" in err_str:
            if "has not been used" in err_str or "is not enabled" in err_str or "service_disabled" in err_str:
                msg = (
                    "Google Sheets API is not enabled in your Google Cloud project. "
                    "Please visit Google Cloud Console -> APIs & Services -> Enable 'Google Sheets API'."
                )
                error_type = "api_disabled"
            else:
                msg = (
                    "Permission denied (HTTP 403). The service account does not have permission "
                    "to view this spreadsheet. Please share the spreadsheet with the service account email."
                )
                error_type = "permission_denied"
        elif status_code == 404 or "404" in err_str:
            msg = (
                "Spreadsheet not found (HTTP 404). Verify that GOOGLE_SHEETS_SPREADSHEET_ID is correct "
                "and that the spreadsheet has been shared with your service account."
            )
            error_type = "not_found"
        elif status_code == 400 or "400" in err_str:
            msg = "Bad request (HTTP 400). Please check the format of GOOGLE_SHEETS_SPREADSHEET_ID."
            error_type = "bad_request"
        else:
            msg = f"Connection error ({exc.__class__.__name__}). Check your network connection and configuration."
            error_type = "connection_error"

        return {
            "success": False,
            "error_type": error_type,
            "message": msg,
        }


def get_worksheet_headers(
    service=None,
    spreadsheet_id: Optional[str] = None,
    readonly: bool = True,
) -> Dict[str, Any]:
    """
    Safely reads ONLY the first row (headers) of each worksheet in the spreadsheet.
    Strictly requests range 1:1 for each worksheet, ensuring no customer records,
    data rows, or values beyond the header row are ever fetched.
    """
    metadata_result = get_spreadsheet_metadata(
        service=service,
        spreadsheet_id=spreadsheet_id,
        readonly=readonly,
    )
    if not metadata_result["success"]:
        return metadata_result

    target_id = (spreadsheet_id or get_spreadsheet_id() or "").strip()
    if service is None:
        service = get_sheets_service(readonly=readonly)

    if not service:
        return {
            "success": False,
            "error_type": "service_unavailable",
            "message": "Google Sheets service client could not be initialized.",
        }

    headers_by_sheet = {}
    try:
        for sheet_name in metadata_result["worksheets"]:
            range_header_only = f"'{sheet_name}'!1:1"
            response = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=target_id,
                    range=range_header_only,
                )
                .execute()
            )
            rows = response.get("values", [])
            if rows and len(rows) > 0:
                headers_by_sheet[sheet_name] = [str(c).strip() for c in rows[0]]
            else:
                headers_by_sheet[sheet_name] = []

        return {
            "success": True,
            "spreadsheet_title": metadata_result["title"],
            "headers": headers_by_sheet,
            "message": "Headers retrieved successfully.",
        }

    except Exception as exc:
        err_str = str(exc).lower()
        status_code = getattr(getattr(exc, "resp", None), "status", None)

        if status_code == 403 or "403" in err_str:
            msg = "Permission denied while reading header row (HTTP 403)."
            error_type = "permission_denied"
        elif status_code == 404 or "404" in err_str:
            msg = "Spreadsheet or worksheet not found (HTTP 404)."
            error_type = "not_found"
        else:
            msg = f"Failed to retrieve headers: {exc.__class__.__name__}."
            error_type = "connection_error"

        return {
            "success": False,
            "error_type": error_type,
            "message": msg,
        }


def validate_or_init_header(
    service,
    spreadsheet_id: str,
    sheet_name: str,
    init_if_empty: bool = True,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Validates or idempotently initializes the header row (Row 1) for a specific worksheet.
    - If worksheet is completely empty and init_if_empty=True: writes approved headers (unless dry_run).
    - If worksheet has non-empty row 1: verifies it strictly matches the approved schema.
    - If headers differ: halts and returns schema_mismatch without overwriting.
    """
    expected_headers = APPROVED_SCHEMAS.get(sheet_name)
    if not expected_headers:
        return {
            "valid": False,
            "error_type": "unknown_worksheet",
            "message": f"No approved schema defined for worksheet '{sheet_name}'.",
        }

    range_header_only = f"'{sheet_name}'!1:1"
    try:
        response = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=spreadsheet_id,
                range=range_header_only,
            )
            .execute()
        )
        rows = response.get("values", [])
        existing_headers = [str(c).strip() for c in rows[0]] if rows and len(rows) > 0 else []

        # Empty worksheet header
        if not existing_headers:
            if not init_if_empty:
                return {
                    "valid": False,
                    "error_type": "empty_headers",
                    "message": f"Worksheet '{sheet_name}' has no header row. Initialization required.",
                }

            if dry_run:
                return {
                    "valid": True,
                    "initialized": False,
                    "would_initialize": True,
                    "headers": expected_headers,
                    "message": f"[DRY-RUN] Would initialize Row 1 of '{sheet_name}' with {len(expected_headers)} headers.",
                }

            # Initialize row 1 with approved headers
            last_col_letter = chr(ord("A") + len(expected_headers) - 1)
            target_range = f"'{sheet_name}'!A1:{last_col_letter}1"
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=target_range,
                valueInputOption="USER_ENTERED",
                body={"values": [expected_headers]},
            ).execute()

            return {
                "valid": True,
                "initialized": True,
                "headers": expected_headers,
                "message": f"Successfully initialized Row 1 of '{sheet_name}' with approved schema.",
            }

        # Check existing headers against approved schema
        if existing_headers == expected_headers:
            return {
                "valid": True,
                "initialized": False,
                "headers": existing_headers,
                "message": f"Headers in '{sheet_name}' match approved schema.",
            }
        else:
            return {
                "valid": False,
                "error_type": "schema_mismatch",
                "message": (
                    f"Schema mismatch in worksheet '{sheet_name}'. "
                    f"Expected {len(expected_headers)} columns, found {len(existing_headers)}. "
                    "Halting synchronization to prevent data corruption."
                ),
                "expected": expected_headers,
                "found": existing_headers,
            }

    except Exception as exc:
        err_str = str(exc).lower()
        status_code = getattr(getattr(exc, "resp", None), "status", None)
        if status_code == 403 or "403" in err_str:
            msg = f"Permission denied accessing '{sheet_name}' (HTTP 403)."
            error_type = "permission_denied"
        else:
            msg = f"Failed to inspect headers in '{sheet_name}': {exc.__class__.__name__}."
            error_type = "connection_error"

        return {
            "valid": False,
            "error_type": error_type,
            "message": msg,
        }


# =========================================================================
# Row Formatting Functions
# =========================================================================

def format_enquiry_row(enquiry) -> List[Any]:
    """Formats an Enquiry model instance into an ordered, sanitized row list."""
    dt_str = (
        timezone.localtime(enquiry.created_at).strftime("%Y-%m-%d %H:%M")
        if enquiry.created_at
        else ""
    )
    svc_name = (
        enquiry.service_name_snapshot
        or (enquiry.service.name if enquiry.service else "")
    )
    raw_values = [
        f"ENQ-{enquiry.id}",
        dt_str,
        enquiry.name or "",
        enquiry.phone or "",
        enquiry.email or "",
        enquiry.city or "",
        svc_name,
        enquiry.get_enquiry_type_display() if hasattr(enquiry, "get_enquiry_type_display") else (enquiry.enquiry_type or ""),
        enquiry.get_usage_intention_display() if hasattr(enquiry, "get_usage_intention_display") else (enquiry.usage_intention or ""),
        enquiry.get_callback_time_display() if hasattr(enquiry, "get_callback_time_display") else (enquiry.callback_time or ""),
        enquiry.get_preferred_contact_method_display() if hasattr(enquiry, "get_preferred_contact_method_display") else (enquiry.preferred_contact_method or ""),
        enquiry.message or "",
        enquiry.get_status_display() if hasattr(enquiry, "get_status_display") else (enquiry.status or ""),
    ]
    return [sanitize_cell_value(val) for val in raw_values]


def format_appointment_row(appointment) -> List[Any]:
    """Formats an Appointment model instance into an ordered, sanitized row list."""
    created_str = (
        timezone.localtime(appointment.created_at).strftime("%Y-%m-%d %H:%M")
        if appointment.created_at
        else ""
    )
    apt_date_str = (
        appointment.appointment_date.strftime("%Y-%m-%d")
        if appointment.appointment_date
        else ""
    )
    svc_name = (
        appointment.service_name_snapshot
        or (appointment.service.name if appointment.service else "")
    )
    raw_values = [
        appointment.booking_reference or f"APT-{appointment.id}",
        created_str,
        appointment.name or "",
        appointment.phone or "",
        appointment.email or "",
        appointment.city or "",
        svc_name,
        apt_date_str,
        appointment.get_time_slot_display() if hasattr(appointment, "get_time_slot_display") else (appointment.time_slot or ""),
        appointment.get_demo_format_display() if hasattr(appointment, "get_demo_format_display") else (appointment.demo_format or ""),
        appointment.notes or "",
        appointment.get_status_display() if hasattr(appointment, "get_status_display") else (appointment.status or ""),
    ]
    return [sanitize_cell_value(val) for val in raw_values]


def format_support_request_row(support_request) -> List[Any]:
    """Formats a SupportRequest model instance into an ordered, sanitized row list."""
    created_str = (
        timezone.localtime(support_request.created_at).strftime("%Y-%m-%d %H:%M")
        if support_request.created_at
        else ""
    )
    raw_values = [
        support_request.ticket_number or f"SR-{support_request.id}",
        created_str,
        support_request.name or "",
        support_request.email or "",
        support_request.phone or "",
        support_request.get_request_type_display() if hasattr(support_request, "get_request_type_display") else (support_request.request_type or ""),
        support_request.subject or "",
        support_request.product_name or "",
        support_request.message or "",
        support_request.get_status_display() if hasattr(support_request, "get_status_display") else (support_request.status or ""),
    ]
    return [sanitize_cell_value(val) for val in raw_values]


# =========================================================================
# Durable Synchronization Engine
# =========================================================================

def enqueue_sync_record(source_type: str, source_id: int, source_identifier: str):
    """
    Creates or re-enqueues a durable database sync tracking record.
    Database-first: returns the GoogleSheetsSyncRecord instance.
    """
    from user.models import GoogleSheetsSyncRecord

    sync_record, created = GoogleSheetsSyncRecord.objects.get_or_create(
        source_type=source_type,
        source_id=source_id,
        defaults={
            "source_identifier": source_identifier,
            "status": GoogleSheetsSyncRecord.SyncStatus.PENDING,
            "next_retry_at": timezone.now(),
        },
    )
    if not created and sync_record.status != GoogleSheetsSyncRecord.SyncStatus.SYNCED:
        sync_record.source_identifier = source_identifier
        sync_record.status = GoogleSheetsSyncRecord.SyncStatus.PENDING
        sync_record.next_retry_at = timezone.now()
        sync_record.save(update_fields=["source_identifier", "status", "next_retry_at", "updated_at"])

    return sync_record


def queue_enquiry_sync(enquiry):
    """Convenience helper to enqueue an Enquiry after database commit."""
    from user.models import GoogleSheetsSyncRecord
    source_identifier = f"ENQ-{enquiry.id}"
    return enqueue_sync_record(GoogleSheetsSyncRecord.SourceType.ENQUIRY, enquiry.id, source_identifier)


def queue_appointment_sync(appointment):
    """Convenience helper to enqueue an Appointment after database commit."""
    from user.models import GoogleSheetsSyncRecord
    source_identifier = appointment.booking_reference or f"APT-{appointment.id}"
    return enqueue_sync_record(GoogleSheetsSyncRecord.SourceType.APPOINTMENT, appointment.id, source_identifier)


def queue_support_request_sync(support_request):
    """Convenience helper to enqueue a SupportRequest after database commit."""
    from user.models import GoogleSheetsSyncRecord
    source_identifier = support_request.ticket_number or f"SR-{support_request.id}"
    return enqueue_sync_record(GoogleSheetsSyncRecord.SourceType.SUPPORT_REQUEST, support_request.id, source_identifier)


def sync_single_record(
    sync_record,
    service=None,
    spreadsheet_id: Optional[str] = None,
    dry_run: bool = False,
    init_headers: bool = True,
) -> Dict[str, Any]:
    """
    Synchronizes a single GoogleSheetsSyncRecord to its destination worksheet.
    - Verifies headers first (halts on schema mismatch).
    - Checks Column A for existing source_identifier:
      * 0 matches: appends new row.
      * 1 match: updates existing row.
      * >1 matches: halts with duplicate_identifier error.
    - Marks sync_record status in database accordingly.
    """
    from user.models import Appointment, Enquiry, GoogleSheetsSyncRecord, SupportRequest

    target_id = (spreadsheet_id or get_spreadsheet_id() or "").strip()
    if not target_id:
        sync_record.mark_failed("missing_spreadsheet_id", "GOOGLE_SHEETS_SPREADSHEET_ID is not configured.")
        return {"success": False, "error_type": "missing_spreadsheet_id"}

    if service is None:
        service = get_sheets_service(readonly=False)

    if not service:
        sync_record.mark_failed("service_unavailable", "Could not initialize Google Sheets service client.")
        return {"success": False, "error_type": "service_unavailable"}

    # Resolve destination worksheet and format row data from source model
    sheet_name = ""
    row_values = []
    try:
        if sync_record.source_type == GoogleSheetsSyncRecord.SourceType.ENQUIRY:
            sheet_name = WORKSHEET_ENQUIRIES
            enquiry = Enquiry.objects.get(id=sync_record.source_id)
            row_values = format_enquiry_row(enquiry)
        elif sync_record.source_type == GoogleSheetsSyncRecord.SourceType.APPOINTMENT:
            sheet_name = WORKSHEET_APPOINTMENTS
            appointment = Appointment.objects.get(id=sync_record.source_id)
            row_values = format_appointment_row(appointment)
        elif sync_record.source_type == GoogleSheetsSyncRecord.SourceType.SUPPORT_REQUEST:
            sheet_name = WORKSHEET_CONTACTS
            support_request = SupportRequest.objects.get(id=sync_record.source_id)
            row_values = format_support_request_row(support_request)
        else:
            sync_record.mark_failed("unknown_source_type", f"Unknown source type: {sync_record.source_type}", is_terminal=True)
            return {"success": False, "error_type": "unknown_source_type"}
    except Exception as exc:
        sync_record.mark_failed("source_record_missing", f"Originating record {sync_record.source_id} not found in database.", is_terminal=True)
        return {"success": False, "error_type": "source_record_missing"}

    # Step 1: Validate or initialize header row
    header_check = validate_or_init_header(
        service=service,
        spreadsheet_id=target_id,
        sheet_name=sheet_name,
        init_if_empty=init_headers,
        dry_run=dry_run,
    )
    if not header_check["valid"]:
        sync_record.mark_failed(header_check.get("error_type", "schema_mismatch"), header_check.get("message", "Schema validation failed."))
        return {"success": False, "error_type": header_check.get("error_type"), "message": header_check.get("message")}

    # Step 2: Query Column A to locate any existing row with this stable identifier
    try:
        col_a_res = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=target_id,
                range=f"'{sheet_name}'!A:A",
            )
            .execute()
        )
        col_a_rows = col_a_res.get("values", [])
        matching_rows = []
        for idx, row in enumerate(col_a_rows, start=1):
            if row and str(row[0]).strip() == sync_record.source_identifier:
                matching_rows.append(idx)

        # Check duplicate identifier safety rule
        if len(matching_rows) > 1:
            err_msg = f"Duplicate identifier found in '{sheet_name}' at rows {matching_rows}."
            sync_record.mark_failed("duplicate_identifier", err_msg, is_terminal=True)
            return {"success": False, "error_type": "duplicate_identifier", "message": err_msg}

        last_col_letter = chr(ord("A") + len(row_values) - 1)

        # Step 3: Insert or Update
        if len(matching_rows) == 1:
            # Update existing row
            target_row = matching_rows[0]
            if dry_run:
                return {
                    "success": True,
                    "action": "would_update",
                    "sheet_name": sheet_name,
                    "row_index": target_row,
                    "identifier": sync_record.source_identifier,
                }

            update_range = f"'{sheet_name}'!A{target_row}:{last_col_letter}{target_row}"
            service.spreadsheets().values().update(
                spreadsheetId=target_id,
                range=update_range,
                valueInputOption="USER_ENTERED",
                body={"values": [row_values]},
            ).execute()

            sync_record.mark_synced(sheet_name=sheet_name, row_index=target_row)
            return {
                "success": True,
                "action": "updated",
                "sheet_name": sheet_name,
                "row_index": target_row,
                "identifier": sync_record.source_identifier,
            }

        else:
            # Append new row
            if dry_run:
                would_row = len(col_a_rows) + 1
                return {
                    "success": True,
                    "action": "would_append",
                    "sheet_name": sheet_name,
                    "row_index": would_row,
                    "identifier": sync_record.source_identifier,
                }

            append_range = f"'{sheet_name}'!A:A"
            append_res = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=target_id,
                    range=append_range,
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body={"values": [row_values]},
                )
                .execute()
            )

            # Determine updated row index if available
            appended_row_idx = len(col_a_rows) + 1
            sync_record.mark_synced(sheet_name=sheet_name, row_index=appended_row_idx)
            return {
                "success": True,
                "action": "appended",
                "sheet_name": sheet_name,
                "row_index": appended_row_idx,
                "identifier": sync_record.source_identifier,
            }

    except Exception as exc:
        err_str = str(exc).lower()
        status_code = getattr(getattr(exc, "resp", None), "status", None)
        if status_code == 403 or "403" in err_str:
            category = "permission_denied"
            msg = "Permission denied writing to spreadsheet (HTTP 403)."
        elif status_code == 404 or "404" in err_str:
            category = "not_found"
            msg = "Target spreadsheet or worksheet not found (HTTP 404)."
        elif status_code == 429 or "quota" in err_str or "rate" in err_str:
            category = "rate_limited"
            msg = "Google Sheets API quota or rate limit exceeded."
        else:
            category = "api_error"
            msg = f"Google Sheets API error: {exc.__class__.__name__}."

        sync_record.mark_failed(category, msg)
        return {"success": False, "error_type": category, "message": msg}


def process_pending_syncs(
    limit: int = 20,
    dry_run: bool = False,
    init_headers: bool = True,
    service=None,
    spreadsheet_id: Optional[str] = None,
    source_type: Optional[str] = None,
    identifier: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Processes bounded batch of eligible pending or retry-ready sync records.
    - Selects records with status PENDING, or FAILED with next_retry_at <= now.
    - Supports filtering by source_type (enquiry, appointment, support_request)
      and/or specific source_identifier for isolated controlled sync execution.
    - Limits to `limit` records per batch.
    - Respects dry_run.
    """
    from django.db.models import Q
    from user.models import GoogleSheetsSyncRecord

    now = timezone.now()
    records_filter = (
        Q(status=GoogleSheetsSyncRecord.SyncStatus.PENDING)
        | (
            Q(status=GoogleSheetsSyncRecord.SyncStatus.FAILED)
            & Q(next_retry_at__isnull=False)
            & Q(next_retry_at__lte=now)
        )
    )

    if source_type:
        records_filter = records_filter & Q(source_type=source_type)
    if identifier:
        records_filter = records_filter & Q(source_identifier=identifier)

    eligible_records = GoogleSheetsSyncRecord.objects.filter(records_filter).order_by("created_at")[:limit]

    results = {
        "processed": 0,
        "succeeded": 0,
        "failed": 0,
        "dry_run": dry_run,
        "records": [],
    }


    if not eligible_records.exists():
        return results

    target_id = (spreadsheet_id or get_spreadsheet_id() or "").strip()
    if service is None:
        service = get_sheets_service(readonly=False)

    for record in eligible_records:
        if not dry_run:
            record.mark_in_progress()

        res = sync_single_record(
            sync_record=record,
            service=service,
            spreadsheet_id=target_id,
            dry_run=dry_run,
            init_headers=init_headers,
        )

        results["processed"] += 1
        if res.get("success"):
            results["succeeded"] += 1
        else:
            results["failed"] += 1

        results["records"].append({
            "id": record.id,
            "source_type": record.source_type,
            "source_identifier": record.source_identifier,
            "result": res,
        })

    return results


def queue_backfill_records(source_type: Optional[str] = None, limit: Optional[int] = None) -> int:
    """
    Deliberately enqueues historical database records that have no sync record yet.
    Requires deliberate operator invocation.
    """
    from user.models import Appointment, Enquiry, GoogleSheetsSyncRecord, SupportRequest

    queued_count = 0

    # Backfill Enquiries
    if source_type in (None, GoogleSheetsSyncRecord.SourceType.ENQUIRY):
        existing_enq_ids = set(
            GoogleSheetsSyncRecord.objects.filter(
                source_type=GoogleSheetsSyncRecord.SourceType.ENQUIRY
            ).values_list("source_id", flat=True)
        )
        enqs_to_backfill = Enquiry.objects.exclude(id__in=existing_enq_ids).order_by("created_at")
        if limit:
            enqs_to_backfill = enqs_to_backfill[:limit]
        for enq in enqs_to_backfill:
            queue_enquiry_sync(enq)
            queued_count += 1

    # Backfill Appointments
    if source_type in (None, GoogleSheetsSyncRecord.SourceType.APPOINTMENT):
        remaining_limit = (limit - queued_count) if limit else None
        if remaining_limit is None or remaining_limit > 0:
            existing_apt_ids = set(
                GoogleSheetsSyncRecord.objects.filter(
                    source_type=GoogleSheetsSyncRecord.SourceType.APPOINTMENT
                ).values_list("source_id", flat=True)
            )
            apts_to_backfill = Appointment.objects.exclude(id__in=existing_apt_ids).order_by("created_at")
            if remaining_limit:
                apts_to_backfill = apts_to_backfill[:remaining_limit]
            for apt in apts_to_backfill:
                queue_appointment_sync(apt)
                queued_count += 1

    # Backfill Support Requests
    if source_type in (None, GoogleSheetsSyncRecord.SourceType.SUPPORT_REQUEST):
        remaining_limit = (limit - queued_count) if limit else None
        if remaining_limit is None or remaining_limit > 0:
            existing_sr_ids = set(
                GoogleSheetsSyncRecord.objects.filter(
                    source_type=GoogleSheetsSyncRecord.SourceType.SUPPORT_REQUEST
                ).values_list("source_id", flat=True)
            )
            srs_to_backfill = SupportRequest.objects.exclude(id__in=existing_sr_ids).order_by("created_at")
            if remaining_limit:
                srs_to_backfill = srs_to_backfill[:remaining_limit]
            for sr in srs_to_backfill:
                queue_support_request_sync(sr)
                queued_count += 1

    return queued_count
