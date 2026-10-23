from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Announcement,
    Appointment,
    BodyPart,
    Category,
    CustomerNeed,
    Enquiry,
    IntendedUse,
    Offer,
    Service,
    ServiceType,
    SiteSettings,
    SupportRequest,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "image_preview",
        "is_active",
        "display_order",
        "service_count",
    )
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["display_order", "name"]
    readonly_fields = ("image_preview_detail",)

    fieldsets = (
        (
            "Category Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "image",
                    "image_preview_detail",
                )
            },
        ),
        (
            "Display & Visibility",
            {
                "fields": (
                    "is_active",
                    "display_order",
                )
            },
        ),
    )

    @admin.display(description="Thumbnail")
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            try:
                return format_html(
                    '<img src="{}" alt="{}" style="width: 42px; height: 42px; object-fit: cover; border-radius: 6px; border: 1px solid #dcdcdc;" />',
                    obj.image.url,
                    obj.name,
                )
            except Exception:
                pass
        return "-"

    @admin.display(description="Current Image Preview")
    def image_preview_detail(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            try:
                return format_html(
                    '<img src="{}" alt="{}" style="max-width: 220px; max-height: 150px; object-fit: cover; border-radius: 8px; border: 1px solid #ccc;" />',
                    obj.image.url,
                    obj.name,
                )
            except Exception:
                pass
        return "No image uploaded"

    @admin.display(description="Services")
    def service_count(self, obj):
        return obj.services.count()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "image_preview",
        "is_featured",
        "is_active",
        "display_order",
        "created_at",
    )
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("category", "is_featured", "is_active", "created_at")
    search_fields = (
        "name",
        "slug",
        "short_description",
        "description",
        "category__name",
    )
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["display_order", "name"]
    filter_horizontal = (
        "customer_needs",
        "body_parts",
        "service_types",
        "intended_uses",
    )
    readonly_fields = ("created_at", "updated_at", "image_preview_detail")

    fieldsets = (
        (
            "Core Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "display_order",
                    ("is_active", "is_featured"),
                )
            },
        ),
        (
            "Overview & Visuals",
            {
                "fields": (
                    "short_description",
                    "description",
                    "image",
                    "image_preview_detail",
                )
            },
        ),
        (
            "Clinical & Usage Information",
            {
                "fields": (
                    "benefits",
                    "usage_instructions",
                    "precautions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Filter Classifications",
            {
                "fields": (
                    "customer_needs",
                    "body_parts",
                    "service_types",
                    "intended_uses",
                )
            },
        ),
        (
            "System Audit",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Thumbnail")
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            try:
                return format_html(
                    '<img src="{}" alt="{}" style="width: 42px; height: 42px; object-fit: cover; border-radius: 6px; border: 1px solid #dcdcdc;" />',
                    obj.image.url,
                    obj.name,
                )
            except Exception:
                pass
        return "-"

    @admin.display(description="Current Image Preview")
    def image_preview_detail(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            try:
                return format_html(
                    '<img src="{}" alt="{}" style="max-width: 240px; max-height: 160px; object-fit: cover; border-radius: 8px; border: 1px solid #ccc;" />',
                    obj.image.url,
                    obj.name,
                )
            except Exception:
                pass
        return "No image uploaded"


@admin.register(CustomerNeed)
class CustomerNeedAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "service_count")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Services")
    def service_count(self, obj):
        return obj.services.count()


@admin.register(BodyPart)
class BodyPartAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "service_count")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Services")
    def service_count(self, obj):
        return obj.services.count()


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "service_count")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Services")
    def service_count(self, obj):
        return obj.services.count()


@admin.register(IntendedUse)
class IntendedUseAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "service_count")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Services")
    def service_count(self, obj):
        return obj.services.count()


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "badge_tag",
        "discount_title",
        "promo_code",
        "is_active",
        "status_badge",
        "valid_from",
        "valid_until",
        "display_order",
    )
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active", "valid_from", "valid_until")
    search_fields = (
        "title",
        "badge_tag",
        "discount_title",
        "promo_code",
        "description",
    )
    ordering = ["display_order", "-created_at"]
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Offer Details",
            {
                "fields": (
                    "title",
                    "badge_tag",
                    "discount_title",
                    "promo_code",
                    "description",
                )
            },
        ),
        (
            "Status & Display",
            {
                "fields": (
                    "is_active",
                    "display_order",
                )
            },
        ),
        (
            "Scheduling & Validity Period",
            {
                "fields": (
                    "validity_text",
                    "valid_from",
                    "valid_until",
                )
            },
        ),
        (
            "System Audit",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Status")
    def status_badge(self, obj):
        if not obj.is_active:
            return mark_safe(
                '<span style="color: #b00; font-weight: bold;">Inactive</span>'
            )
        now = timezone.now()
        if obj.valid_from and obj.valid_from > now:
            return mark_safe(
                '<span style="color: #c78500; font-weight: bold;">Scheduled</span>'
            )
        if obj.valid_until and obj.valid_until < now:
            return mark_safe(
                '<span style="color: #666; font-style: italic;">Expired</span>'
            )
        return mark_safe(
            '<span style="color: #080; font-weight: bold;">Active</span>'
        )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "message",
        "badge_text",
        "link_url",
        "is_active",
        "status_badge",
        "valid_from",
        "valid_until",
        "display_order",
    )
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active", "valid_from", "valid_until")
    search_fields = ("message", "badge_text", "link_text", "link_url")
    ordering = ["display_order", "-created_at"]
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Announcement Content",
            {
                "fields": (
                    "message",
                    "badge_text",
                    "link_text",
                    "link_url",
                )
            },
        ),
        (
            "Status & Display",
            {
                "fields": (
                    "is_active",
                    "display_order",
                )
            },
        ),
        (
            "Scheduling & Validity Period",
            {
                "fields": (
                    "valid_from",
                    "valid_until",
                )
            },
        ),
        (
            "System Audit",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Status")
    def status_badge(self, obj):
        if not obj.is_active:
            return mark_safe(
                '<span style="color: #b00; font-weight: bold;">Inactive</span>'
            )
        now = timezone.now()
        if obj.valid_from and obj.valid_from > now:
            return mark_safe(
                '<span style="color: #c78500; font-weight: bold;">Scheduled</span>'
            )
        if obj.valid_until and obj.valid_until < now:
            return mark_safe(
                '<span style="color: #666; font-style: italic;">Expired</span>'
            )
        return mark_safe(
            '<span style="color: #080; font-weight: bold;">Active</span>'
        )


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "city",
        "service",
        "status",
        "created_at",
    )
    list_editable = ("status",)
    list_filter = (
        "status",
        "created_at",
        "usage_intention",
        "callback_time",
        "service",
    )
    search_fields = (
        "name",
        "email",
        "phone",
        "city",
        "message",
        "admin_notes",
        "service_name_snapshot",
    )
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "service_name_snapshot")
    list_per_page = 25

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "name",
                    "phone",
                    "email",
                    "city",
                )
            },
        ),
        (
            "Enquiry Details",
            {
                "fields": (
                    "enquiry_type",
                    "preferred_contact_method",
                    "service",
                    "service_name_snapshot",
                    "usage_intention",
                    "callback_time",
                    "message",
                )
            },
        ),
        (
            "Lead Management",
            {
                "fields": (
                    "status",
                    "admin_notes",
                )
            },
        ),
        (
            "Audit Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "booking_reference",
        "name",
        "phone",
        "city",
        "service_name",
        "appointment_date",
        "time_slot",
        "demo_format",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "demo_format",
        "time_slot",
        "appointment_date",
        "service__category",
    )
    search_fields = (
        "booking_reference",
        "name",
        "email",
        "phone",
        "city",
        "notes",
        "admin_notes",
        "service_name_snapshot",
    )
    ordering = ["-appointment_date", "-created_at"]
    date_hierarchy = "appointment_date"
    readonly_fields = ("booking_reference", "created_at", "updated_at", "service_name_snapshot")
    list_per_page = 25

    fieldsets = (
        (
            "Booking Reference",
            {
                "fields": (
                    "booking_reference",
                )
            },
        ),
        (
            "Customer Details",
            {
                "fields": (
                    "name",
                    "phone",
                    "email",
                    "city",
                )
            },
        ),
        (
            "Appointment Schedule & Selection",
            {
                "fields": (
                    "service",
                    "service_name_snapshot",
                    "appointment_date",
                    "time_slot",
                    "demo_format",
                    "notes",
                )
            },
        ),
        (
            "Staff Management",
            {
                "fields": (
                    "status",
                    "admin_notes",
                )
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Requested Service")
    def service_name(self, obj):
        if obj.service:
            return obj.service.name
        return obj.service_name_snapshot or "—"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("business_name", "primary_phone", "contact_email", "updated_at")

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_number",
        "name",
        "email",
        "phone",
        "request_type",
        "subject",
        "status",
        "created_at",
    )
    list_filter = ("status", "request_type", "created_at")
    search_fields = (
        "ticket_number",
        "name",
        "email",
        "phone",
        "subject",
        "product_name",
        "message",
        "admin_notes",
    )
    ordering = ["-created_at"]
    readonly_fields = ("ticket_number", "created_at", "updated_at")


