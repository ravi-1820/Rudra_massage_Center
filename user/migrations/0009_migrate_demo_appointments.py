# Generated data migration to safely preserve demo appointments in database

from django.db import migrations
from django.utils import timezone
from datetime import date, timedelta


def seed_demo_appointments(apps, schema_editor):
    Appointment = apps.get_model("user", "Appointment")
    Service = apps.get_model("user", "Service")

    today = timezone.localdate()

    demo_data = [
        {
            "booking_reference": "APT-401",
            "name": "Sanjay Solanki",
            "phone": "9825044441",
            "email": "sanjay.s@example.com",
            "city": "Ahmedabad",
            "service_search": "Lumbar",
            "fallback_service_name": "AyurSpine Lumbar Belt",
            "days_offset": 3,
            "time_slot": "morning",
            "demo_format": "home",
            "status": "confirmed",
            "notes": "Doorstep demo requested for chronic lumbar stiffness. Please bring demonstration unit.",
            "admin_notes": "Assigned to field demo specialist. Slot confirmed with client over phone.",
        },
        {
            "booking_reference": "APT-402",
            "name": "Dr. Hemal Bhatt",
            "phone": "9898044442",
            "email": "hemal.b@example.com",
            "city": "Ahmedabad",
            "service_search": "Shirodhara",
            "fallback_service_name": "Shirodhara Automated Console",
            "days_offset": 5,
            "time_slot": "midday",
            "demo_format": "centre",
            "status": "pending",
            "notes": "Centre demonstration requested for wellness clinic evaluation.",
            "admin_notes": "Awaiting final time slot confirmation from client assistant.",
        },
        {
            "booking_reference": "APT-403",
            "name": "Geeta Desai",
            "phone": "9727044443",
            "email": "geeta.d@example.com",
            "city": "Vadodara",
            "service_search": "Knee",
            "fallback_service_name": "OrthoRelief Knee Guard",
            "days_offset": 7,
            "time_slot": "morning",
            "demo_format": "home",
            "status": "confirmed",
            "notes": "Elderly patient suffering from knee arthritis. Home demo requested.",
            "admin_notes": "Confirmed doorstep visit. Son will be present during demonstration.",
        },
    ]

    for item in demo_data:
        if not Appointment.objects.filter(booking_reference=item["booking_reference"]).exists():
            matched_service = (
                Service.objects.filter(name__icontains=item["service_search"]).first()
                or Service.objects.first()
            )
            service_name = matched_service.name if matched_service else item["fallback_service_name"]

            Appointment.objects.create(
                booking_reference=item["booking_reference"],
                name=item["name"],
                phone=item["phone"],
                email=item["email"],
                city=item["city"],
                service=matched_service,
                service_name_snapshot=service_name,
                appointment_date=today + timedelta(days=item["days_offset"]),
                time_slot=item["time_slot"],
                demo_format=item["demo_format"],
                status=item["status"],
                notes=item["notes"],
                admin_notes=item["admin_notes"],
            )


def reverse_seed_demo_appointments(apps, schema_editor):
    Appointment = apps.get_model("user", "Appointment")
    Appointment.objects.filter(booking_reference__in=["APT-401", "APT-402", "APT-403"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0008_enquiry_enquiry_type_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_demo_appointments, reverse_seed_demo_appointments),
    ]
