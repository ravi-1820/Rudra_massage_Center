# Generated manually to establish initial authoritative SiteSettings record

from django.db import migrations


def create_default_settings(apps, schema_editor):
    SiteSettings = apps.get_model('user', 'SiteSettings')
    if not SiteSettings.objects.exists():
        SiteSettings.objects.create(
            id=1,
            business_name="Rudra Massage & Wellness",
            primary_phone="+91 98250 00000",
            contact_email="care@rudrawellness.com",
            whatsapp_number="+91 98250 00000",
            business_address="Rudra Massage & Wellness Centre, S.G. Highway, Bodakdev, Ahmedabad, Gujarat 380054",
            google_maps_url="https://maps.google.com/maps?q=Bodakdev,%20Ahmedabad,%20Gujarat&t=&z=13&ie=UTF8&iwloc=&output=embed",
            business_hours="Mon - Sat: 9:30 AM - 7:00 PM | Sun: By Prior Appointment",
            enable_announcement_banner=True,
            enable_whatsapp_floating=True,
        )


def remove_default_settings(apps, schema_editor):
    SiteSettings = apps.get_model('user', 'SiteSettings')
    SiteSettings.objects.filter(id=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_sitesettings_supportrequest'),
    ]

    operations = [
        migrations.RunPython(create_default_settings, reverse_code=remove_default_settings),
    ]
