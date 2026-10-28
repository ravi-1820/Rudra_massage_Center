"""
Management command to test live Google Sheets connection in a safe, read-only manner.

Reads spreadsheet metadata only (spreadsheet title and worksheet tab names).
Uses the narrowest required scope (https://www.googleapis.com/auth/spreadsheets.readonly).
Never reads, writes, modifies, or exports customer records or cell data.
Never displays sensitive credentials, file paths, private keys, or tokens.
"""

from django.core.management.base import BaseCommand
from user.google_sheets import get_sheets_config_diagnostics, get_spreadsheet_metadata


class Command(BaseCommand):
    help = (
        "Perform a safe, read-only live diagnostic connection test against the configured Google Spreadsheet. "
        "Fetches spreadsheet title and worksheet names only; never reads or modifies cell data."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--headers",
            action="store_true",
            help="Audit and display the first-row column headers of each worksheet (read-only).",
        )

    def handle(self, *args, **options):
        show_headers = options.get("headers", False)
        self.stdout.write(self.style.MIGRATE_HEADING("=== Google Sheets Read-Only Connection Diagnostic ==="))

        # First check configuration readiness
        diagnostics = get_sheets_config_diagnostics()
        if not diagnostics["is_configured"]:
            self.stdout.write(self.style.ERROR(f"Configuration check failed: {diagnostics['status']}"))
            self.stdout.write(
                "Run 'python manage.py check_sheets_config' for configuration details."
            )
            return

        self.stdout.write("Connecting to Google Sheets API using read-only scope...")

        if show_headers:
            from user.google_sheets import get_worksheet_headers

            result = get_worksheet_headers(readonly=True)
            if result["success"]:
                self.stdout.write(self.style.SUCCESS("Connection Status: SUCCESS"))
                self.stdout.write(f"Spreadsheet Title: {result['spreadsheet_title']}")
                self.stdout.write("\nWorksheet Column Headers (Row 1):")
                for sheet_name, cols in result["headers"].items():
                    self.stdout.write(self.style.MIGRATE_LABEL(f"  [{sheet_name}]"))
                    if cols:
                        for col_idx, col_name in enumerate(cols, start=1):
                            self.stdout.write(f"    Col {col_idx}: '{col_name}'")
                    else:
                        self.stdout.write(self.style.WARNING("    (No header row detected / empty sheet)"))
                self.stdout.write(
                    self.style.SUCCESS("\nHeader audit verified. Strictly row 1 queried; no customer data read.")
                )
            else:
                self.stdout.write(self.style.ERROR("Connection Status: FAILED"))
                self.stdout.write(f"Error Category:    {result.get('error_type', 'unknown')}")
                self.stdout.write(f"Diagnostic Reason: {result.get('message', 'Unknown error')}")
        else:
            result = get_spreadsheet_metadata(readonly=True)
            if result["success"]:
                self.stdout.write(self.style.SUCCESS("Connection Status: SUCCESS"))
                self.stdout.write(f"Spreadsheet Title: {result['title']}")
                self.stdout.write(f"Worksheets Found ({result['worksheet_count']}):")
                for idx, sheet_name in enumerate(result["worksheets"], start=1):
                    self.stdout.write(f"  {idx}. {sheet_name}")
                self.stdout.write(
                    self.style.SUCCESS("\nRead-only connection verified. No spreadsheet data was modified.")
                )
            else:
                self.stdout.write(self.style.ERROR("Connection Status: FAILED"))
                self.stdout.write(f"Error Category:    {result.get('error_type', 'unknown')}")
                self.stdout.write(f"Diagnostic Reason: {result.get('message', 'Unknown error')}")

            self.stdout.write(
                self.style.WARNING(
                    "\nTroubleshooting tips:\n"
                    "- Ensure the service account email has Viewer or Editor access on the Google Sheet.\n"
                    "- Ensure the Google Sheets API is enabled in your Google Cloud Console project.\n"
                    "- Verify that GOOGLE_SHEETS_SPREADSHEET_ID is accurate."
                )
            )

        self.stdout.write(self.style.MIGRATE_HEADING("====================================================="))
