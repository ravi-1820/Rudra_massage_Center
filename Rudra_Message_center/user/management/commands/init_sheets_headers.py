"""
Management command to safely initialize or validate Google Sheet worksheet headers.

- Idempotently writes approved Row 1 headers to empty worksheets.
- Validates non-empty worksheets against the approved schema.
- Halts and reports schema mismatches without overwriting or clearing existing data.
"""

from django.core.management.base import BaseCommand
from user.google_sheets import (
    APPROVED_SCHEMAS,
    get_sheets_config_diagnostics,
    get_sheets_service,
    get_spreadsheet_id,
    validate_or_init_header,
)


class Command(BaseCommand):
    help = "Idempotently initialize or validate Google Sheets worksheet column headers."

    def add_arguments(self, parser):
        parser.add_argument(
            "--check-only",
            action="store_true",
            help="Check header schema validity without writing any headers.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate header initialization without performing any API write.",
        )

    def handle(self, *args, **options):
        check_only = options.get("check_only", False)
        dry_run = options.get("dry_run", False)

        self.stdout.write(self.style.MIGRATE_HEADING("=== Google Sheets Header Management ==="))

        diagnostics = get_sheets_config_diagnostics()
        if not diagnostics["is_configured"]:
            self.stdout.write(self.style.ERROR(f"Configuration check failed: {diagnostics['status']}"))
            return

        target_id = get_spreadsheet_id()
        # If check_only, use read-only scope; otherwise standard write scope
        service = get_sheets_service(readonly=check_only)
        if not service:
            self.stdout.write(self.style.ERROR("Could not initialize Google Sheets service client."))
            return

        init_if_empty = not check_only

        for sheet_name in APPROVED_SCHEMAS.keys():
            self.stdout.write(self.style.MIGRATE_LABEL(f"\nChecking Worksheet: [{sheet_name}]"))
            res = validate_or_init_header(
                service=service,
                spreadsheet_id=target_id,
                sheet_name=sheet_name,
                init_if_empty=init_if_empty,
                dry_run=dry_run,
            )

            if res["valid"]:
                if res.get("initialized"):
                    self.stdout.write(self.style.SUCCESS(f"  Status: INITIALIZED -> {res['message']}"))
                elif res.get("would_initialize"):
                    self.stdout.write(self.style.WARNING(f"  Status: DRY-RUN -> {res['message']}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"  Status: VALID -> {res['message']}"))
            else:
                self.stdout.write(self.style.ERROR(f"  Status: INVALID -> {res['message']}"))
                if "expected" in res and "found" in res:
                    self.stdout.write(f"    Expected: {res['expected']}")
                    self.stdout.write(f"    Found:    {res['found']}")

        self.stdout.write(self.style.MIGRATE_HEADING("\n======================================="))
