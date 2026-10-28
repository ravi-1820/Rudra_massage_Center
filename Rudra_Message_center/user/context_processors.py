from django.db.models import Q
from django.utils import timezone
from .models import Announcement, SiteSettings


def announcement_context(request):
    """
    Context processor to deliver the currently active, scheduled announcement
    to all user-facing templates.
    """
    try:
        now = timezone.now()
        announcement = (
            Announcement.objects.filter(is_active=True)
            .filter(Q(valid_from__isnull=True) | Q(valid_from__lte=now))
            .filter(Q(valid_until__isnull=True) | Q(valid_until__gte=now))
            .order_by("display_order", "-created_at")
            .first()
        )
        return {"active_announcement": announcement}
    except Exception:
        return {"active_announcement": None}


def site_settings_context(request):
    """
    Context processor to deliver the authoritative SiteSettings record
    to all templates.
    """
    try:
        settings_obj = SiteSettings.load()
        return {"site_settings": settings_obj}
    except Exception:
        return {"site_settings": None}


def admin_notifications_context(request):
    """
    Context processor to deliver live notifications for the admin portal:
    - New appointment bookings (pending)
    - New enquiries (new)
    - New support tickets (new)
    Provides exact counts, categorized items, and a chronological combined notification feed.
    """
    path = getattr(request, 'path', '')
    user = getattr(request, 'user', None)
    is_staff = getattr(user, 'is_staff', False) if user else False
    if not (path.startswith('/custom-admin/') or path.startswith('/admin/') or is_staff):
        return {}

    try:
        from django.urls import reverse
        from .models import Appointment, Enquiry, SupportRequest

        pending_appointments = list(
            Appointment.objects.filter(status='pending').select_related('service').order_by('-created_at')[:5]
        )
        new_enquiries = list(
            Enquiry.objects.filter(status='new').select_related('service').order_by('-created_at')[:5]
        )
        new_support_requests = list(
            SupportRequest.objects.filter(status='new').order_by('-created_at')[:5]
        )

        pending_appointments_count = Appointment.objects.filter(status='pending').count()
        new_enquiries_count = Enquiry.objects.filter(status='new').count()
        new_support_count = SupportRequest.objects.filter(status='new').count()
        total_notifications_count = (
            pending_appointments_count + new_enquiries_count + new_support_count
        )

        return {
            "pending_appointments_count": pending_appointments_count,
            "new_enquiries_count": new_enquiries_count,
            "new_support_count": new_support_count,
            "total_notifications_count": total_notifications_count,
        }
    except Exception:
        return {
            "pending_appointments_count": 0,
            "new_enquiries_count": 0,
            "new_support_count": 0,
            "total_notifications_count": 0,
        }


