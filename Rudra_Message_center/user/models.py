from datetime import timedelta
import re
import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def clean(self):
        if self.name and not self.name.strip():
            raise ValidationError({"name": "Category name cannot be only whitespace."})

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def name_translated(self):
        from django.utils import translation
        from user.translation_catalog import translate_taxonomy_term
        return translate_taxonomy_term(self.name, lang=translation.get_language() or "en")

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="services",
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True,
    )

    benefits = models.TextField(blank=True)
    usage_instructions = models.TextField(blank=True)
    precautions = models.TextField(blank=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    customer_needs = models.ManyToManyField(
        "CustomerNeed",
        blank=True,
        related_name="services",
    )

    body_parts = models.ManyToManyField(
        "BodyPart",
        blank=True,
        related_name="services",
    )

    service_types = models.ManyToManyField(
        "ServiceType",
        blank=True,
        related_name="services",
    )

    intended_uses = models.ManyToManyField(
        "IntendedUse",
        blank=True,
        related_name="services",
    )

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Product / Service"
        verbose_name_plural = "Products & Services"

    def clean(self):
        if self.name and not self.name.strip():
            raise ValidationError({"name": "Service name cannot be only whitespace."})
        if self.short_description and not self.short_description.strip():
            raise ValidationError({"short_description": "Short description cannot be only whitespace."})

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CustomerNeed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Customer Need"
        verbose_name_plural = "Customer Needs"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def name_translated(self):
        from django.utils import translation
        from user.translation_catalog import translate_taxonomy_term
        return translate_taxonomy_term(self.name, lang=translation.get_language() or "en")

    def __str__(self):
        return self.name


class BodyPart(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Body Part"
        verbose_name_plural = "Body Parts"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def name_translated(self):
        from django.utils import translation
        from user.translation_catalog import translate_taxonomy_term
        return translate_taxonomy_term(self.name, lang=translation.get_language() or "en")

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Service Type"
        verbose_name_plural = "Service Types"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def name_translated(self):
        from django.utils import translation
        from user.translation_catalog import translate_taxonomy_term
        return translate_taxonomy_term(self.name, lang=translation.get_language() or "en")

    def __str__(self):
        return self.name


class IntendedUse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Intended Use"
        verbose_name_plural = "Intended Uses"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def name_translated(self):
        from django.utils import translation
        from user.translation_catalog import translate_taxonomy_term
        return translate_taxonomy_term(self.name, lang=translation.get_language() or "en")

    def __str__(self):
        return self.name


class Offer(models.Model):
    title = models.CharField(max_length=200)
    badge_tag = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. 'Festive Exclusive', 'Elders First'",
    )
    discount_title = models.CharField(
        max_length=100,
        help_text="e.g. 'Flat 25% OFF', 'Extra ₹1,500 OFF'",
    )
    description = models.TextField()
    promo_code = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. 'FESTIVE25'",
    )
    validity_text = models.CharField(
        max_length=150,
        blank=True,
        help_text="e.g. 'Valid till November 15, 2026' or 'Ongoing Community Senior Offer'",
    )
    valid_from = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Start date/time for scheduled activation (optional)",
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="End date/time for expiration (optional)",
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Special Offer"
        verbose_name_plural = "Special Offers"

    def clean(self):
        if self.valid_from and self.valid_until and self.valid_from > self.valid_until:
            raise ValidationError({"valid_until": "End date/time cannot be earlier than start date/time."})

    @property
    def is_currently_valid(self):
        if not self.is_active:
            return False
        now = timezone.now()
        if self.valid_from and self.valid_from > now:
            return False
        if self.valid_until and self.valid_until < now:
            return False
        return True

    def __str__(self):
        return self.title


class Announcement(models.Model):
    message = models.CharField(
        max_length=300,
        help_text="Primary announcement text displayed in top banner",
    )
    badge_text = models.CharField(
        max_length=50,
        blank=True,
        default="Special Offer",
        help_text="Prefix badge label e.g. 'Special Offer'",
    )
    link_text = models.CharField(
        max_length=100,
        blank=True,
        default="Shop Now →",
    )
    link_url = models.CharField(
        max_length=255,
        blank=True,
        default="/offers/",
    )
    valid_from = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Start date/time for scheduled activation (optional)",
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="End date/time for expiration (optional)",
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Announcement Banner"
        verbose_name_plural = "Announcement Banners"

    def clean(self):
        if self.valid_from and self.valid_until and self.valid_from > self.valid_until:
            raise ValidationError({"valid_until": "End date/time cannot be earlier than start date/time."})

    @property
    def is_currently_valid(self):
        if not self.is_active:
            return False
        now = timezone.now()
        if self.valid_from and self.valid_from > now:
            return False
        if self.valid_until and self.valid_until < now:
            return False
        return True

    def __str__(self):
        return self.message[:50]


class Enquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        IN_DISCUSSION = "in_discussion", "In Discussion"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    class UsageIntention(models.TextChoices):
        PERSONAL = "personal", "Personal / Family Home Use"
        CLINIC = "clinic", "Physiotherapy / Wellness Clinic"
        ELDERLY = "elderly", "Specialized Senior Citizen Care"
        DISTRIBUTION = "distribution", "Bulk Dealership / Reselling"

    class CallbackTime(models.TextChoices):
        MORNING = "morning", "Morning (10:00 AM - 1:00 PM)"
        AFTERNOON = "afternoon", "Afternoon (2:00 PM - 5:00 PM)"
        EVENING = "evening", "Evening (5:00 PM - 8:00 PM)"
        ANYTIME = "anytime", "Anytime"

    class EnquiryType(models.TextChoices):
        THERAPY_MACHINE = "therapy_machine", "Therapy machine / wellness product"
        HOME_SETUP = "home_setup", "Home wellness setup"
        CLINIC_SETUP = "clinic_setup", "Clinic / professional setup"
        BULK_BUSINESS = "bulk_business", "Bulk or business enquiry"
        PRODUCT_SUPPORT = "product_support", "Existing product support"
        GUIDANCE = "guidance", "Not sure — I need guidance"

    class ContactMethod(models.TextChoices):
        PHONE = "phone", "Phone"
        WHATSAPP = "whatsapp", "WhatsApp"
        EMAIL = "email", "Email"

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True)
    city = models.CharField(max_length=100)

    enquiry_type = models.CharField(
        max_length=40,
        choices=EnquiryType.choices,
        default=EnquiryType.THERAPY_MACHINE,
        blank=True,
        help_text="Primary requirement / reason for enquiry",
    )
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=ContactMethod.choices,
        default=ContactMethod.PHONE,
        blank=True,
    )

    service = models.ForeignKey(
        "Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enquiries",
        help_text="Selected therapy service/machine (optional)",
    )
    service_name_snapshot = models.CharField(
        max_length=200,
        blank=True,
        help_text="Archived service name at time of submission",
    )

    usage_intention = models.CharField(
        max_length=30,
        choices=UsageIntention.choices,
        default=UsageIntention.PERSONAL,
        blank=True,
    )
    callback_time = models.CharField(
        max_length=30,
        choices=CallbackTime.choices,
        default=CallbackTime.MORNING,
        blank=True,
    )
    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes added by staff during telephone follow-up",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer Enquiry"
        verbose_name_plural = "Customer Enquiries"

    def clean(self):
        if self.name and not self.name.strip():
            raise ValidationError({"name": "Customer name cannot be only whitespace."})
        if self.city and not self.city.strip():
            raise ValidationError({"city": "City cannot be only whitespace."})

    def save(self, *args, **kwargs):
        if self.service and not self.service_name_snapshot:
            self.service_name_snapshot = self.service.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.phone} ({self.get_status_display()})"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending Confirmation"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class TimeSlot(models.TextChoices):
        MORNING = "morning", "Morning (10:00 AM - 1:00 PM)"
        MIDDAY = "midday", "Midday (1:00 PM - 3:00 PM)"
        AFTERNOON = "afternoon", "Afternoon (3:00 PM - 5:00 PM)"
        EVENING = "evening", "Evening (5:00 PM - 7:30 PM)"

    class DemoFormat(models.TextChoices):
        CENTRE = "centre", "Centre Visit (Ahmedabad Demonstration Facility)"
        HOME = "home", "Home Doorstep Demo (Selected Cities)"
        VIDEO = "video", "Virtual Guided Video Consultation"

    booking_reference = models.CharField(
        max_length=32,
        unique=True,
        blank=True,
        help_text="Unique booking reference code",
    )
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True)
    city = models.CharField(max_length=100)

    service = models.ForeignKey(
        "Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        help_text="Selected therapy machine or solution",
    )
    service_name_snapshot = models.CharField(
        max_length=200,
        blank=True,
        help_text="Archived service name at time of booking request",
    )

    appointment_date = models.DateField(
        help_text="Preferred date requested by the customer",
    )
    time_slot = models.CharField(
        max_length=30,
        choices=TimeSlot.choices,
        default=TimeSlot.MORNING,
    )
    demo_format = models.CharField(
        max_length=30,
        choices=DemoFormat.choices,
        default=DemoFormat.CENTRE,
    )
    notes = models.TextField(
        blank=True,
        help_text="Doorstep address or special discomfort notes",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal staff notes regarding slot confirmation or logistics",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-appointment_date", "-created_at"]
        verbose_name = "Appointment Request"
        verbose_name_plural = "Appointment Requests"

    def clean(self):
        if self.name and not self.name.strip():
            raise ValidationError({"name": "Customer name cannot be only whitespace."})
        if self.city and not self.city.strip():
            raise ValidationError({"city": "City cannot be only whitespace."})
        if self.appointment_date and self.appointment_date < timezone.localdate():
            raise ValidationError({"appointment_date": "Appointment date cannot be in the past."})

    def save(self, *args, **kwargs):
        if self.service and not self.service_name_snapshot:
            self.service_name_snapshot = self.service.name
        if not self.booking_reference:
            import uuid
            self.booking_reference = f"APT-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference}: {self.name} on {self.appointment_date} ({self.get_status_display()})"


class SiteSettings(models.Model):
    business_name = models.CharField(
        max_length=200,
        default="Rudra Massage & Wellness",
        help_text="Official business / brand display name",
    )
    primary_phone = models.CharField(
        max_length=30,
        default="+91 98250 00000",
        help_text="Primary customer care / helpline phone number",
    )
    contact_email = models.EmailField(
        max_length=254,
        default="care@rudrawellness.com",
        help_text="Primary support / inquiries email address",
    )
    whatsapp_number = models.CharField(
        max_length=30,
        default="+91 98250 00000",
        help_text="WhatsApp support number (with country code)",
    )
    business_address = models.TextField(
        default="Rudra Massage & Wellness Centre, S.G. Highway, Bodakdev, Ahmedabad, Gujarat 380054",
        help_text="Physical experience centre address",
    )
    google_maps_url = models.URLField(
        max_length=500,
        blank=True,
        default="https://maps.google.com/maps?q=Bodakdev,%20Ahmedabad,%20Gujarat&t=&z=13&ie=UTF8&iwloc=&output=embed",
        help_text="Google Maps embed or location URL",
    )
    business_hours = models.CharField(
        max_length=255,
        default="Mon - Sat: 9:30 AM - 7:00 PM | Sun: By Prior Appointment",
        help_text="Operating / consultation hours",
    )
    enable_announcement_banner = models.BooleanField(
        default=True,
        help_text="Enable top announcement banner across site",
    )
    enable_whatsapp_floating = models.BooleanField(
        default=True,
        help_text="Display floating WhatsApp contact button",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def clean(self):
        if self.business_name and not self.business_name.strip():
            raise ValidationError({"business_name": "Business name cannot be only whitespace."})
        if self.primary_phone and not self.primary_phone.strip():
            raise ValidationError({"primary_phone": "Primary phone cannot be only whitespace."})
        if self.contact_email and not self.contact_email.strip():
            raise ValidationError({"contact_email": "Contact email cannot be only whitespace."})
        if self.business_address and not self.business_address.strip():
            raise ValidationError({"business_address": "Business address cannot be only whitespace."})

    def save(self, *args, **kwargs):
        # Enforce singleton pattern: single authoritative record at pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Protect the singleton settings record from accidental deletion
        pass

    @classmethod
    def load(cls):
        """
        Safely fetch the singleton settings record or initialize with default values.
        """
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                "business_name": "Rudra Massage & Wellness",
                "primary_phone": "+91 98250 00000",
                "contact_email": "care@rudrawellness.com",
                "whatsapp_number": "+91 98250 00000",
                "business_address": "Rudra Massage & Wellness Centre, S.G. Highway, Bodakdev, Ahmedabad, Gujarat 380054",
                "google_maps_url": "https://maps.google.com/maps?q=Bodakdev,%20Ahmedabad,%20Gujarat&t=&z=13&ie=UTF8&iwloc=&output=embed",
                "business_hours": "Mon - Sat: 9:30 AM - 7:00 PM | Sun: By Prior Appointment",
                "enable_announcement_banner": True,
                "enable_whatsapp_floating": True,
            },
        )
        return obj

    @property
    def phone_digits(self):
        cleaned = re.sub(r"[^\d+]", "", self.primary_phone or "")
        return cleaned

    @property
    def whatsapp_digits(self):
        cleaned = re.sub(r"\D", "", self.whatsapp_number or "")
        return cleaned

    def __str__(self):
        return f"Site Settings ({self.business_name})"


class SupportRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    class RequestType(models.TextChoices):
        CONTACT = "contact", "Contact / General Inquiry"
        PRODUCT_SUPPORT = "product_support", "Product / Warranty Support"
        DEMO_REQUEST = "demo_request", "Demo Request"
        CLINIC_SETUP = "clinic_setup", "Clinic / Bulk Setup"
        FEEDBACK = "feedback", "Feedback / Other"

    ticket_number = models.CharField(
        max_length=32,
        unique=True,
        blank=True,
        help_text="Unique reference ticket number",
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)

    request_type = models.CharField(
        max_length=30,
        choices=RequestType.choices,
        default=RequestType.CONTACT,
        blank=True,
    )
    subject = models.CharField(
        max_length=200,
        blank=True,
        help_text="User selected subject or request category",
    )
    product_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Relevant equipment or device model (if applicable)",
    )
    message = models.TextField(
        help_text="Customer message or issue description",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Private internal staff follow-up and resolution notes",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Support Request"
        verbose_name_plural = "Support Requests"

    def clean(self):
        if self.name and not self.name.strip():
            raise ValidationError({"name": "Name cannot be only whitespace."})
        if self.message and not self.message.strip():
            raise ValidationError({"message": "Message cannot be only whitespace."})

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"SR-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_number}: {self.name} - {self.subject or self.get_request_type_display()} ({self.get_status_display()})"


class GoogleSheetsSyncRecord(models.Model):
    """
    Durable database-backed tracking record for Google Sheets synchronization.
    Maintains sync status, attempt count, retry timestamps, and sanitized error categories
    without storing customer messages, credentials, or sensitive payloads.
    """

    class SourceType(models.TextChoices):
        ENQUIRY = "enquiry", "Enquiry"
        APPOINTMENT = "appointment", "Appointment"
        SUPPORT_REQUEST = "support_request", "Support Request"

    class SyncStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        SYNCED = "synced", "Synced"
        FAILED = "failed", "Failed"

    # Exponential backoff schedule in minutes: attempt 1 -> 1m, 2 -> 5m, 3 -> 15m, 4 -> 60m, 5+ -> 240m
    BACKOFF_MINUTES = [1, 5, 15, 60, 240]
    MAX_ATTEMPTS = 5

    source_type = models.CharField(
        max_length=50,
        choices=SourceType.choices,
        help_text="Originating Django model",
    )
    source_id = models.PositiveIntegerField(
        help_text="Primary key of originating database record",
    )
    source_identifier = models.CharField(
        max_length=64,
        db_index=True,
        help_text="Stable canonical identifier (e.g. Booking Ref, Ticket No, or ENQ-ID)",
    )
    sheet_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Target Google Sheet worksheet title",
    )
    row_index = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Matched or inserted 1-indexed row number in the worksheet",
    )
    status = models.CharField(
        max_length=20,
        choices=SyncStatus.choices,
        default=SyncStatus.PENDING,
        db_index=True,
    )
    attempts = models.PositiveIntegerField(
        default=0,
        help_text="Number of synchronization attempts made",
    )
    last_attempt_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of most recent synchronization attempt",
    )
    next_retry_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Timestamp when next retry is eligible to run",
    )
    synced_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of successful synchronization",
    )
    last_error_category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Sanitized error category (e.g. permission_denied, schema_mismatch)",
    )
    last_error_message = models.CharField(
        max_length=255,
        blank=True,
        help_text="Safe, truncated error summary (no personal data or secrets)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Google Sheets Sync Record"
        verbose_name_plural = "Google Sheets Sync Records"
        constraints = [
            models.UniqueConstraint(
                fields=["source_type", "source_id"],
                name="unique_source_sync_record",
            )
        ]

    def __str__(self):
        return f"[{self.get_source_type_display()}:{self.source_identifier}] -> {self.get_status_display()} ({self.attempts} attempts)"

    def mark_in_progress(self):
        self.status = self.SyncStatus.IN_PROGRESS
        self.attempts += 1
        self.last_attempt_at = timezone.now()
        self.save(update_fields=["status", "attempts", "last_attempt_at", "updated_at"])

    def mark_synced(self, sheet_name: str, row_index: int = None):
        self.status = self.SyncStatus.SYNCED
        self.sheet_name = sheet_name
        if row_index is not None:
            self.row_index = row_index
        self.synced_at = timezone.now()
        self.next_retry_at = None
        self.last_error_category = ""
        self.last_error_message = ""
        self.save(
            update_fields=[
                "status",
                "sheet_name",
                "row_index",
                "synced_at",
                "next_retry_at",
                "last_error_category",
                "last_error_message",
                "updated_at",
            ]
        )

    def mark_failed(self, error_category: str, error_message: str, is_terminal: bool = False):
        self.status = self.SyncStatus.FAILED
        self.last_error_category = str(error_category)[:100]
        self.last_error_message = str(error_message)[:255]

        if is_terminal or self.attempts >= self.MAX_ATTEMPTS:
            self.next_retry_at = None
        else:
            delay_idx = min(max(self.attempts - 1, 0), len(self.BACKOFF_MINUTES) - 1)
            backoff_delay = timedelta(minutes=self.BACKOFF_MINUTES[delay_idx])
            self.next_retry_at = timezone.now() + backoff_delay

        self.save(
            update_fields=[
                "status",
                "last_error_category",
                "last_error_message",
                "next_retry_at",
                "updated_at",
            ]
        )


