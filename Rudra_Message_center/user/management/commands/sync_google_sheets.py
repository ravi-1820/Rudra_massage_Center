"""
Management command to process pending Google Sheets synchronization records.

- Bounded batch processing (--limit 20 default).
- Safe retry behavior with capped exponential backoff.
- Dry-run mode (--dry-run).
- Optional deliberate backfill of historical un-synced database records (--backfill).
- Never leaks customer messages or sensitive credentials.
"""

from django.core.management.base import BaseCommand
from user.google_sheets import (
    get_sheets_config_diagnostics,
    get_sheets_service,
    get_spreadsheet_id,
    process_pending_syncs,
    queue_backfill_records,
)
from user.models import GoogleSheetsSyncRecord


class Command(BaseCommand):
    help = "Process pending Google Sheets synchronization records with bounded limit and retry backoff."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=20,
            help="Maximum number of records to process in this batch (default: 20).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate synchronization without performing any write to Google Sheets.",
        )
        parser.add_argument(
            "--init-headers",
            action="store_true",
            default=True,
            help="Initialize empty worksheet headers automatically if needed (default: True).",
        )
        parser.add_argument(
            "--no-init-headers",
            action="store_false",
            dest="init_headers",
            help="Do not auto-initialize empty worksheet headers.",
        )
        parser.add_argument(
            "--backfill",
            action="store_true",
            help="Explicitly queue historical database records that have not been synced yet.",
        )
        parser.add_argument(
            "--source-type",
            type=str,
            choices=["enquiry", "appointment", "support_request"],
            default=None,
            help="Filter pending sync records by source type (enquiry, appointment, support_request).",
        )
        parser.add_argument(
            "--identifier",
            type=str,
            default=None,
            help="Filter pending sync records by specific source identifier (e.g. APT-20261023-XXXXXX).",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        dry_run = options["dry_run"]
        init_headers = options["init_headers"]
        do_backfill = options["backfill"]
        source_type = options.get("source_type")
        identifier = options.get("identifier")

        self.stdout.write(self.style.MIGRATE_HEADING("=== Google Sheets Synchronization Engine ==="))

        diagnostics = get_sheets_config_diagnostics()
        if not diagnostics["is_configured"]:
            self.stdout.write(self.style.ERROR(f"Configuration check failed: {diagnostics['status']}"))
            return

        if do_backfill:
            self.stdout.write("Operator requested historical backfill queueing...")
            queued = queue_backfill_records(limit=limit)
            self.stdout.write(self.style.SUCCESS(f"Queued {queued} historical record(s) for synchronization."))

        total_pending = GoogleSheetsSyncRecord.objects.filter(
            status=GoogleSheetsSyncRecord.SyncStatus.PENDING
        ).count()
        total_failed = GoogleSheetsSyncRecord.objects.filter(
            status=GoogleSheetsSyncRecord.SyncStatus.FAILED
        ).count()
        total_synced = GoogleSheetsSyncRecord.objects.filter(
            status=GoogleSheetsSyncRecord.SyncStatus.SYNCED
        ).count()

        self.stdout.write(
            f"Queue Status: {total_pending} Pending | {total_failed} Failed / Backoff | {total_synced} Synced"
        )

        if dry_run:
            self.stdout.write(self.style.WARNING("Running in DRY-RUN mode (zero writes will be performed)."))

        self.stdout.write(f"Processing up to {limit} eligible record(s)...")

        target_id = get_spreadsheet_id()
        service = get_sheets_service(readonly=False)
        if not service:
            self.stdout.write(self.style.ERROR("Could not initialize Google Sheets service client."))
            return

        results = process_pending_syncs(
            limit=limit,
            dry_run=dry_run,
            init_headers=init_headers,
            service=service,
            spreadsheet_id=target_id,
            source_type=source_type,
            identifier=identifier,
        )

        self.stdout.write("\nBatch Results Summary:")
        self.stdout.write(f"  Processed: {results['processed']}")
        self.stdout.write(f"  Succeeded: {results['succeeded']}")
        self.stdout.write(f"  Failed:    {results['failed']}")

        for item in results["records"]:
            res = item["result"]
            src = f"[{item['source_type']}:{item['source_identifier']}]"
            if res.get("success"):
                action = res.get("action", "synced")
                sheet = res.get("sheet_name", "")
                row = res.get("row_index", "")
                self.stdout.write(self.style.SUCCESS(f"  OK {src} -> {action} in '{sheet}' (row {row})"))
            else:
                err_type = res.get("error_type", "error")
                msg = res.get("message", "Sync failed.")
                self.stdout.write(self.style.ERROR(f"  FAIL {src} -> {err_type}: {msg}"))

        self.stdout.write(self.style.MIGRATE_HEADING("============================================"))
