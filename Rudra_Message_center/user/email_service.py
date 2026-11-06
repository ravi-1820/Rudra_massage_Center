"""
Rudra Massage & Wellness - Email Notification Service.

Provides automatic, reliable, professional transactional email notifications for:
1. Customer submission confirmations (Appointment, Enquiry, Support Request)
2. Custom admin responses, status updates, and rescheduling

Features:
- Dual-format HTML and Plain-Text rendering using reusable templates
- English & Gujarati language support with clean fallback
- Idempotency and duplicate prevention
- Safe error handling: never crashes user submission on mail backend issues
- Audit logging via EmailNotificationLog
- Safe sanitization: zero credentials, internal notes, or raw exceptions exposed
"""

import hashlib
import logging
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from user.models import Appointment, EmailNotificationLog, Enquiry, SiteSettings, SupportRequest

logger = logging.getLogger(__name__)


def _is_valid_email(email: Optional[str]) -> bool:
    """Basic check for valid email address presence."""
    if not email:
        return False
    email = str(email).strip()
    return bool("@" in email and "." in email.split("@")[-1] and len(email) >= 5)


def send_notification_email(
    recipient_email: Optional[str],
    subject: str,
    template_prefix: str,
    context: Dict[str, Any],
    source_type: str,
    source_id: int,
    source_identifier: str = "",
    notification_type: str = "",
    idempotency_key: Optional[str] = None,
    language: str = "en",
) -> bool:
    """
    Core reusable email dispatcher with idempotency and audit tracking.
    """
    recipient_name = context.get("customer_name", "")
    lang = (language or "en").lower().strip()
    if lang not in ("en", "gu"):
        lang = "en"

    # Normalize email
    clean_email = (recipient_email or "").strip()

    # Safe fallback if recipient email is missing or malformed
    if not _is_valid_email(clean_email):
        logger.warning(
            "Email notification skipped for %s #%s (%s): recipient email missing or invalid (%r).",
            source_type,
            source_id,
            source_identifier,
            clean_email,
        )
        try:
            EmailNotificationLog.objects.create(
                notification_type=notification_type or "general",
                source_type=source_type,
                source_id=source_id,
                source_identifier=source_identifier,
                recipient_email=clean_email,
                recipient_name=recipient_name,
                subject=subject,
                status=EmailNotificationLog.Status.SKIPPED,
                error_message="Customer email address missing or invalid format.",
                idempotency_key=idempotency_key or "",
                language=lang,
            )
        except Exception as log_err:
            logger.debug("Failed to record skipped email log: %s", log_err)
        return False

    # Idempotency check: avoid duplicate email on refresh / duplicate invocation
    if idempotency_key:
        existing = EmailNotificationLog.objects.filter(
            idempotency_key=idempotency_key,
            status=EmailNotificationLog.Status.SENT,
        ).first()
        if existing:
            logger.info(
                "Duplicate email notification suppressed for %s #%s (Key: %s).",
                source_type,
                source_id,
                idempotency_key,
            )
            return True

    # Prepare context with site branding & settings
    try:
        site_settings = SiteSettings.load()
    except Exception:
        site_settings = None
    render_context = {
        **context,
        "site_settings": site_settings,
        "language": lang,
        "current_year": timezone.now().year,
    }

    html_template = f"emails/{template_prefix}.html"
    text_template = f"emails/{template_prefix}.txt"

    try:
        html_body = render_to_string(html_template, render_context)
        text_body = render_to_string(text_template, render_context)
    except Exception as render_err:
        logger.error(
            "Failed to render email templates for %s (%s): %s",
            template_prefix,
            source_identifier,
            render_err,
        )
        try:
            EmailNotificationLog.objects.create(
                notification_type=notification_type or "general",
                source_type=source_type,
                source_id=source_id,
                source_identifier=source_identifier,
                recipient_email=clean_email,
                recipient_name=recipient_name,
                subject=subject,
                status=EmailNotificationLog.Status.FAILED,
                error_message=f"Template render error: {render_err.__class__.__name__}",
                idempotency_key=idempotency_key or "",
                language=lang,
            )
        except Exception:
            pass
        return False

    # Send message via Django email framework
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "care@rudrawellness.com")

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=[clean_email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        EmailNotificationLog.objects.create(
            notification_type=notification_type or "general",
            source_type=source_type,
            source_id=source_id,
            source_identifier=source_identifier,
            recipient_email=clean_email,
            recipient_name=recipient_name,
            subject=subject,
            status=EmailNotificationLog.Status.SENT,
            sent_at=timezone.now(),
            idempotency_key=idempotency_key or "",
            language=lang,
        )
        logger.info(
            "Email notification successfully sent: [%s] to %s (%s)",
            notification_type,
            clean_email,
            source_identifier,
        )
        return True

    except Exception as send_err:
        err_msg = str(send_err)[:250]
        logger.warning(
            "Failed to send email notification to %s for %s (%s): %s",
            clean_email,
            source_type,
            source_identifier,
            send_err.__class__.__name__,
        )
        try:
            EmailNotificationLog.objects.create(
                notification_type=notification_type or "general",
                source_type=source_type,
                source_id=source_id,
                source_identifier=source_identifier,
                recipient_email=clean_email,
                recipient_name=recipient_name,
                subject=subject,
                status=EmailNotificationLog.Status.FAILED,
                error_message=f"{send_err.__class__.__name__}: {err_msg}",
                idempotency_key=idempotency_key or "",
                language=lang,
            )
        except Exception:
            pass
        return False


# =========================================================================
# 1. Customer Submission Confirmation Emails
# =========================================================================

def send_appointment_received_email(appointment: Appointment) -> bool:
    """
    Sends customer booking acknowledgement for an appointment request.
    Subject: Appointment Booking Received – Rudra Massage & Wellness
    """
    lang = (appointment.language or "en").lower()
    subject = (
        "એપોઇન્ટમેન્ટ બુકિંગ વિનંતી પ્રાપ્ત થઈ – રુદ્ર મસાજ અને વેલનેસ"
        if lang == "gu"
        else "Appointment Booking Received – Rudra Massage & Wellness"
    )

    svc_name = (
        appointment.service.name
        if appointment.service
        else (appointment.service_name_snapshot or "General Wellness Consultation")
    )

    context = {
        "customer_name": appointment.name,
        "booking_reference": appointment.booking_reference,
        "service_name": svc_name,
        "appointment_date": appointment.appointment_date,
        "time_slot_display": appointment.get_time_slot_display(),
        "demo_format_display": appointment.get_demo_format_display(),
        "status_display": appointment.get_status_display(),
        "city": appointment.city,
        "notes": appointment.notes,
    }

    idempotency_key = f"sub_apt_{appointment.id}"

    return send_notification_email(
        recipient_email=appointment.email,
        subject=subject,
        template_prefix="appointment_received",
        context=context,
        source_type=EmailNotificationLog.SourceType.APPOINTMENT,
        source_id=appointment.id,
        source_identifier=appointment.booking_reference,
        notification_type=EmailNotificationLog.NotificationType.APPOINTMENT_RECEIVED,
        idempotency_key=idempotency_key,
        language=lang,
    )


def send_enquiry_received_email(enquiry: Enquiry) -> bool:
    """
    Sends customer acknowledgement for an online therapy enquiry.
    Subject: We Have Received Your Enquiry – Rudra Massage & Wellness
    """
    lang = (enquiry.language or "en").lower()
    subject = (
        "અમે તમારી પૂછપરછ પ્રાપ્ત કરી છે – રુદ્ર મસાજ અને વેલનેસ"
        if lang == "gu"
        else "We Have Received Your Enquiry – Rudra Massage & Wellness"
    )

    svc_name = (
        enquiry.service.name
        if enquiry.service
        else (enquiry.service_name_snapshot or "General Therapy & Wellness Guidance")
    )

    context = {
        "customer_name": enquiry.name,
        "enquiry_id": f"ENQ-{enquiry.id}",
        "service_name": svc_name,
        "enquiry_type_display": enquiry.get_enquiry_type_display(),
        "usage_intention_display": enquiry.get_usage_intention_display(),
        "callback_time_display": enquiry.get_callback_time_display(),
        "preferred_contact_method": enquiry.get_preferred_contact_method_display(),
        "city": enquiry.city,
        "status_display": enquiry.get_status_display(),
        "message": enquiry.message,
    }

    idempotency_key = f"sub_enq_{enquiry.id}"

    return send_notification_email(
        recipient_email=enquiry.email,
        subject=subject,
        template_prefix="enquiry_received",
        context=context,
        source_type=EmailNotificationLog.SourceType.ENQUIRY,
        source_id=enquiry.id,
        source_identifier=f"ENQ-{enquiry.id}",
        notification_type=EmailNotificationLog.NotificationType.ENQUIRY_RECEIVED,
        idempotency_key=idempotency_key,
        language=lang,
    )


def send_support_request_received_email(support_request: SupportRequest) -> bool:
    """
    Sends customer acknowledgement for a contact or support ticket request.
    Subject: Your Support Request Has Been Received – Rudra Massage & Wellness
    """
    lang = (support_request.language or "en").lower()
    subject = (
        "તમારી સપોર્ટ વિનંતી પ્રાપ્ત થઈ છે – રુદ્ર મસાજ અને વેલનેસ"
        if lang == "gu"
        else "Your Support Request Has Been Received – Rudra Massage & Wellness"
    )

    context = {
        "customer_name": support_request.name,
        "ticket_number": support_request.ticket_number,
        "request_type_display": support_request.get_request_type_display(),
        "subject": support_request.subject,
        "product_name": support_request.product_name,
        "status_display": support_request.get_status_display(),
        "message": support_request.message,
    }

    idempotency_key = f"sub_sr_{support_request.id}"

    return send_notification_email(
        recipient_email=support_request.email,
        subject=subject,
        template_prefix="support_received",
        context=context,
        source_type=EmailNotificationLog.SourceType.SUPPORT_REQUEST,
        source_id=support_request.id,
        source_identifier=support_request.ticket_number,
        notification_type=EmailNotificationLog.NotificationType.SUPPORT_RECEIVED,
        idempotency_key=idempotency_key,
        language=lang,
    )


# =========================================================================
# 2. Admin Response Emails
# =========================================================================

def send_appointment_response_email(
    appointment: Appointment,
    response_message: Optional[str] = None,
    previous_status: Optional[str] = None,
    rescheduled: bool = False,
) -> bool:
    """
    Sends appointment update email when an admin responds, updates status,
    or reschedules date/time.
    """
    lang = (appointment.language or "en").lower()
    clean_response = (response_message or "").strip()

    # Dynamic status-specific subject lines
    if appointment.status == Appointment.Status.CONFIRMED:
        subject = (
            f"એપોઇન્ટમેન્ટ કન્ફર્મ થઈ: {appointment.booking_reference} – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Appointment Confirmed: {appointment.booking_reference} – Rudra Massage & Wellness"
        )
    elif appointment.status == Appointment.Status.COMPLETED:
        subject = (
            f"એપોઇન્ટમેન્ટ પૂર્ણ થઈ: {appointment.booking_reference} – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Appointment Completed: {appointment.booking_reference} – Rudra Massage & Wellness"
        )
    elif appointment.status == Appointment.Status.CANCELLED:
        subject = (
            f"એપોઇન્ટમેન્ટ રદ થઈ: {appointment.booking_reference} – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Appointment Cancelled: {appointment.booking_reference} – Rudra Massage & Wellness"
        )
    elif rescheduled:
        subject = (
            f"એપોઇન્ટમેન્ટ પુનઃ સુનિશ્ચિત: {appointment.booking_reference} – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Appointment Rescheduled: {appointment.booking_reference} – Rudra Massage & Wellness"
        )
    else:
        subject = (
            f"એપોઇન્ટમેન્ટ અપડેટ: {appointment.booking_reference} – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Appointment Update: {appointment.booking_reference} – Rudra Massage & Wellness"
        )

    svc_name = (
        appointment.service.name
        if appointment.service
        else (appointment.service_name_snapshot or "General Wellness Consultation")
    )

    context = {
        "customer_name": appointment.name,
        "booking_reference": appointment.booking_reference,
        "service_name": svc_name,
        "appointment_date": appointment.appointment_date,
        "time_slot_display": appointment.get_time_slot_display(),
        "demo_format_display": appointment.get_demo_format_display(),
        "status": appointment.status,
        "status_display": appointment.get_status_display(),
        "previous_status_display": (
            dict(Appointment.Status.choices).get(previous_status, "") if previous_status else ""
        ),
        "rescheduled": rescheduled,
        "response_message": clean_response,
        "city": appointment.city,
    }

    # Hash response and status to prevent accidental double-submit while allowing subsequent updates
    msg_hash = hashlib.md5((clean_response + str(appointment.status) + str(appointment.appointment_date) + str(appointment.time_slot)).encode("utf-8")).hexdigest()[:10]
    idempotency_key = f"resp_apt_{appointment.id}_{msg_hash}_{timezone.now().strftime('%Y%m%d%H%M%S')}"

    return send_notification_email(
        recipient_email=appointment.email,
        subject=subject,
        template_prefix="appointment_response",
        context=context,
        source_type=EmailNotificationLog.SourceType.APPOINTMENT,
        source_id=appointment.id,
        source_identifier=appointment.booking_reference,
        notification_type=EmailNotificationLog.NotificationType.APPOINTMENT_RESPONSE,
        idempotency_key=idempotency_key,
        language=lang,
    )


def send_enquiry_response_email(
    enquiry: Enquiry,
    response_message: Optional[str] = None,
    previous_status: Optional[str] = None,
) -> bool:
    """
    Sends enquiry response email when an admin writes a reply or updates status.
    """
    lang = (enquiry.language or "en").lower()
    clean_response = (response_message or "").strip()
    if clean_response:
        subject = (
            f"તમારી પૂછપરછ ENQ-{enquiry.id} નો પ્રત્યુત્તર – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Response to Your Enquiry ENQ-{enquiry.id} – Rudra Massage & Wellness"
        )
    else:
        subject = (
            f"તમારી પૂછપરછ ENQ-{enquiry.id} અંગે અપડેટ – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Update Regarding Your Enquiry ENQ-{enquiry.id} – Rudra Massage & Wellness"
        )

    svc_name = (
        enquiry.service.name
        if enquiry.service
        else (enquiry.service_name_snapshot or "General Therapy & Wellness Guidance")
    )

    context = {
        "customer_name": enquiry.name,
        "enquiry_id": f"ENQ-{enquiry.id}",
        "service_name": svc_name,
        "status": enquiry.status,
        "status_display": enquiry.get_status_display(),
        "previous_status_display": (
            dict(Enquiry.Status.choices).get(previous_status, "") if previous_status else ""
        ),
        "response_message": clean_response,
        "enquiry_type_display": enquiry.get_enquiry_type_display(),
    }

    msg_hash = hashlib.md5((clean_response + str(enquiry.status)).encode("utf-8")).hexdigest()[:10]
    idempotency_key = f"resp_enq_{enquiry.id}_{msg_hash}_{timezone.now().strftime('%Y%m%d%H%M%S')}"

    return send_notification_email(
        recipient_email=enquiry.email,
        subject=subject,
        template_prefix="enquiry_response",
        context=context,
        source_type=EmailNotificationLog.SourceType.ENQUIRY,
        source_id=enquiry.id,
        source_identifier=f"ENQ-{enquiry.id}",
        notification_type=EmailNotificationLog.NotificationType.ENQUIRY_RESPONSE,
        idempotency_key=idempotency_key,
        language=lang,
    )


def send_support_response_email(
    support_request: SupportRequest,
    response_message: Optional[str] = None,
    previous_status: Optional[str] = None,
) -> bool:
    """
    Sends support request response email when an admin writes a resolution/reply.
    """
    lang = (support_request.language or "en").lower()
    clean_response = (response_message or "").strip()

    if support_request.status == SupportRequest.Status.RESOLVED:
        subject = (
            f"સપોર્ટ વિનંતી પૂર્ણ થઈ: {support_request.ticket_number} – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Support Ticket Resolved: {support_request.ticket_number} – Rudra Massage & Wellness"
        )
    elif support_request.status == SupportRequest.Status.IN_PROGRESS:
        subject = (
            f"સપોર્ટ વિનંતી પ્રક્રિયામાં છે: {support_request.ticket_number} – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Support Ticket In Progress: {support_request.ticket_number} – Rudra Massage & Wellness"
        )
    elif clean_response:
        subject = (
            f"તમારી સપોર્ટ વિનંતી {support_request.ticket_number} નો પ્રત્યુત્તર – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Response to Your Support Request {support_request.ticket_number} – Rudra Massage & Wellness"
        )
    else:
        subject = (
            f"સપોર્ટ વિનંતી અપડેટ: {support_request.ticket_number} – રુદ્ર મસાજ અને વેલનેસ"
            if lang == "gu"
            else f"Support Request Update: {support_request.ticket_number} – Rudra Massage & Wellness"
        )

    context = {
        "customer_name": support_request.name,
        "ticket_number": support_request.ticket_number,
        "request_type_display": support_request.get_request_type_display(),
        "subject": support_request.subject,
        "product_name": support_request.product_name,
        "status": support_request.status,
        "status_display": support_request.get_status_display(),
        "previous_status_display": (
            dict(SupportRequest.Status.choices).get(previous_status, "") if previous_status else ""
        ),
        "response_message": clean_response,
    }

    msg_hash = hashlib.md5((clean_response + str(support_request.status)).encode("utf-8")).hexdigest()[:10]
    idempotency_key = f"resp_sr_{support_request.id}_{msg_hash}_{timezone.now().strftime('%Y%m%d%H%M')}"

    return send_notification_email(
        recipient_email=support_request.email,
        subject=subject,
        template_prefix="support_response",
        context=context,
        source_type=EmailNotificationLog.SourceType.SUPPORT_REQUEST,
        source_id=support_request.id,
        source_identifier=support_request.ticket_number,
        notification_type=EmailNotificationLog.NotificationType.SUPPORT_RESPONSE,
        idempotency_key=idempotency_key,
        language=lang,
    )

