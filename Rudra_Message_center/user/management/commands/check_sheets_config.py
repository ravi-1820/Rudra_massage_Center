"""
Management command to safely check Google Sheets integration status.
Reports only presence of required configuration, never secret contents.
"""

from django.core.management.base import BaseCommand
from user.google_sheets import get_sheets_config_diagnostics


class Command(BaseCommand):
    help = "Safely check Google Sheets integration configuration status without displaying secret contents."

    def handle(self, *args, **options):
        diagnostics = get_sheets_config_diagnostics()

        self.stdout.write(self.style.MIGRATE_HEADING("=== Google Sheets Configuration Diagnostics ==="))
        self.stdout.write(f"Integration Enabled:           {diagnostics['enabled']}")
        self.stdout.write(f"Spreadsheet ID Configured:     {diagnostics['spreadsheet_id_configured']}")
        self.stdout.write(f"Service Account Configured:    {diagnostics['service_account_file_configured']}")
        self.stdout.write(f"Service Account File Exists:   {diagnostics['service_account_file_exists']}")
        self.stdout.write(f"Google API Libraries Ready:    {diagnostics['library_installed']}")
        self.stdout.write(f"Overall Integration Ready:     {diagnostics['is_configured']}")
        self.stdout.write(f"Status Summary:                {diagnostics['status']}")
        self.stdout.write(self.style.MIGRATE_HEADING("=============================================="))
