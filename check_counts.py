import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rudra_massage_center.settings")
django.setup()

from user.models import (
    Category,
    Service,
    CustomerNeed,
    BodyPart,
    ServiceType,
    IntendedUse,
    Offer,
    Announcement,
    Enquiry,
    Appointment,
    SiteSettings,
    SupportRequest,
)
from django.contrib.auth.models import User

print("--- Database Counts ---")
print("User (Staff/Admin):", User.objects.count())
print("Category:", Category.objects.count())
print("Service:", Service.objects.count())
print("CustomerNeed:", CustomerNeed.objects.count())
print("BodyPart:", BodyPart.objects.count())
print("ServiceType:", ServiceType.objects.count())
print("IntendedUse:", IntendedUse.objects.count())
print("Offer:", Offer.objects.count())
print("Announcement:", Announcement.objects.count())
print("Enquiry:", Enquiry.objects.count())
print("Appointment:", Appointment.objects.count())
print("SiteSettings:", SiteSettings.objects.count())
print("SupportRequest:", SupportRequest.objects.count())
