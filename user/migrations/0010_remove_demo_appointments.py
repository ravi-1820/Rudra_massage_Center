# Generated data migration to safely remove migrated demo appointments from active databases

from django.db import migrations


def remove_demo_appointments(apps, schema_editor):
    Appointment = apps.get_model("user", "Appointment")
    demo_booking_references = ["APT-401", "APT-402", "APT-403"]
    Appointment.objects.filter(booking_reference__in=demo_booking_references).delete()


def noop_reverse(apps, schema_editor):
    # No-op reverse to prevent re-introducing fake demo bookings
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0009_migrate_demo_appointments"),
    ]

    operations = [
        migrations.RunPython(remove_demo_appointments, noop_reverse),
    ]
