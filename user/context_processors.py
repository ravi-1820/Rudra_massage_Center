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

