
from datetime import timedelta
import logging

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import DatabaseError, transaction
from django.db.models import Count, Prefetch, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .google_sheets import (
    queue_appointment_sync,
    queue_enquiry_sync,
    queue_support_request_sync,
)

from .forms import AppointmentForm, ContactForm, EnquiryForm, SupportTicketForm
from .models import (
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


logger = logging.getLogger(__name__)
SERVICES_PER_PAGE = 9


def home(request):
    featured_services = (
        Service.objects.filter(
            is_active=True,
            category__is_active=True,
            is_featured=True,
        )
        .select_related("category")
        .order_by("display_order", "name")[:4]
    )
    if not featured_services.exists():
        featured_services = (
            Service.objects.filter(
                is_active=True,
                category__is_active=True,
            )
            .select_related("category")
            .order_by("display_order", "name")[:4]
        )

    # Database-driven eligible categories for Featured Categories carousel
    active_services_prefetch = Prefetch(
        "services",
        queryset=Service.objects.filter(is_active=True).order_by("display_order", "name"),
        to_attr="active_services",
    )
    categories_qs = (
        Category.objects.filter(is_active=True)
        .prefetch_related(active_services_prefetch)
        .annotate(
            active_services_count=Count(
                "services",
                filter=Q(services__is_active=True),
            )
        )
        .order_by("display_order", "name")
    )
    categories_list = list(categories_qs)
    categories_count = len(categories_list)

    # Chunk categories into slides (5 items per slide for responsive grid)
    chunk_size = 5
    category_slides = [
        categories_list[i : i + chunk_size]
        for i in range(0, categories_count, chunk_size)
    ]

    return render(
        request,
        "index.html",
        {
            "featured_services": featured_services,
            "category_slides": category_slides,
            "categories_count": categories_count,
            "categories_list": categories_list,
        },
    )


def about(request):
    return render(request, "about.html")


def services(request):
    try:
        search_query = request.GET.get("q", "").strip()
        category_slug = request.GET.get("category", "").strip()
        sort_by = request.GET.get("sort", "featured").strip()

        needs = request.GET.getlist("need")
        body_parts = request.GET.getlist("body")
        service_types = request.GET.getlist("type")
        intended_uses = request.GET.getlist("usage")

        needs = [value.strip() for value in needs if value.strip()]
        body_parts = [
            value.strip() for value in body_parts if value.strip()
        ]
        service_types = [
            value.strip() for value in service_types if value.strip()
        ]
        intended_uses = [
            value.strip() for value in intended_uses if value.strip()
        ]

        service_list = Service.objects.filter(
            is_active=True,
            category__is_active=True,
        ).select_related("category")

        if search_query:
            service_list = service_list.filter(
                Q(name__icontains=search_query)
                | Q(short_description__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(category__name__icontains=search_query)
            )

        if category_slug:
            service_list = service_list.filter(
                Q(category__slug=category_slug) | Q(category__name__iexact=category_slug)
            )

        if needs:
            service_list = service_list.filter(
                customer_needs__slug__in=needs
            )

        if body_parts:
            service_list = service_list.filter(
                body_parts__slug__in=body_parts
            )

        if service_types:
            service_list = service_list.filter(
                service_types__slug__in=service_types
            )

        if intended_uses:
            service_list = service_list.filter(
                intended_uses__slug__in=intended_uses
            )

        service_list = service_list.distinct()

        if sort_by == "name-asc":
            service_list = service_list.order_by("name")
        elif sort_by == "name-desc":
            service_list = service_list.order_by("-name")
        elif sort_by == "newest":
            service_list = service_list.order_by("-created_at")
        else:
            sort_by = "featured"
            service_list = service_list.order_by(
                "-is_featured",
                "display_order",
                "name",
            )

        paginator = Paginator(service_list, SERVICES_PER_PAGE)
        page_obj = paginator.get_page(request.GET.get("page"))

        query_parameters = request.GET.copy()
        query_parameters.pop("page", None)

        active_customer_needs = CustomerNeed.objects.filter(
            is_active=True
        ).order_by("name")

        active_body_parts = BodyPart.objects.filter(
            is_active=True
        ).order_by("name")

        active_service_types = ServiceType.objects.filter(
            is_active=True
        ).order_by("name")

        active_intended_uses = IntendedUse.objects.filter(
            is_active=True
        ).order_by("name")

        active_categories = Category.objects.filter(
            is_active=True
        ).order_by("display_order", "name")

        active_chips = []

        if search_query:
            active_chips.append({
                "label": f'"{search_query}"',
                "type": "q",
                "val": search_query,
            })

        filter_groups = [
            (needs, active_customer_needs, "need"),
            (body_parts, active_body_parts, "body"),
            (service_types, active_service_types, "type"),
            (intended_uses, active_intended_uses, "usage"),
        ]

        for values, options, filter_type in filter_groups:
            for value in values:
                option = options.filter(slug=value).first()

                active_chips.append({
                    "label": option.name if option else value,
                    "type": filter_type,
                    "val": value,
                })

        if category_slug:
            category = active_categories.filter(
                slug=category_slug
            ).first()

            active_chips.append({
                "label": (
                    f"Category: {category.name}"
                    if category
                    else f"Category: {category_slug}"
                ),
                "type": "category",
                "val": category_slug,
            })

        context = {
            "page_obj": page_obj,
            "services": page_obj.object_list,
            "total_results": paginator.count,
            "search_query": search_query,
            "selected_needs": needs,
            "selected_body_parts": body_parts,
            "selected_service_types": service_types,
            "selected_intended_uses": intended_uses,
            "selected_category": category_slug,
            "sort_by": sort_by,
            "pagination_querystring": query_parameters.urlencode(),
            "active_customer_needs": active_customer_needs,
            "active_body_parts": active_body_parts,
            "active_service_types": active_service_types,
            "active_intended_uses": active_intended_uses,
            "active_categories": active_categories,
            "active_chips": active_chips,
            "has_active_filters": bool(
                search_query
                or category_slug
                or needs
                or body_parts
                or service_types
                or intended_uses
            ),
        }

        return render(request, "services.html", context)

    except DatabaseError:
        logger.exception("Failed to load services.")
        raise


def service_detail(request, slug=None):
    service_slug = (slug or request.GET.get("slug", "")).strip()
    service_id = request.GET.get("id", "").strip()

    active_services = (
        Service.objects.select_related("category")
        .prefetch_related(
            "customer_needs",
            "body_parts",
            "service_types",
            "intended_uses",
        )
        .filter(
            is_active=True,
            category__is_active=True,
        )
    )

    if service_slug:
        service = get_object_or_404(
            active_services,
            slug=service_slug,
        )
    elif service_id.isdigit():
        service = get_object_or_404(
            active_services,
            id=int(service_id),
        )
    else:
        raise Http404("Service not found")

    related_services = (
        Service.objects.filter(
            category=service.category,
            is_active=True,
            category__is_active=True,
        )
        .exclude(id=service.id)
        .select_related("category")
        .prefetch_related("customer_needs", "body_parts", "intended_uses")
        .order_by(
            "-is_featured",
            "display_order",
            "name",
        )[:3]
    )

    return render(
        request,
        "service-detail.html",
        {
            "service": service,
            "related_services": related_services,
        },
    )


def appointment(request):
    try:
        active_services = (
            Service.objects.filter(
                is_active=True,
                category__is_active=True,
            )
            .select_related("category")
            .order_by("category__name", "display_order", "name")
        )

        selected_service = None
        service_param = (
            request.GET.get("service") or request.GET.get("id") or ""
        ).strip()
        if service_param:
            if service_param.isdigit():
                selected_service = active_services.filter(
                    id=int(service_param)
                ).first()
            else:
                selected_service = active_services.filter(
                    slug=service_param
                ).first()

        if request.method == "POST":
            form = AppointmentForm(request.POST)
            if form.is_valid():
                cleaned_phone = form.cleaned_data.get("phone")
                cleaned_service = form.cleaned_data.get("service")
                cleaned_date = form.cleaned_data.get("appointment_date")

                # Duplicate submission check within 2 minutes
                recent_cutoff = timezone.now() - timedelta(minutes=2)
                recent_duplicate = Appointment.objects.filter(
                    phone=cleaned_phone,
                    service=cleaned_service,
                    appointment_date=cleaned_date,
                    created_at__gte=recent_cutoff,
                ).first()

                if recent_duplicate:
                    messages.info(
                        request,
                        f"We have already received an appointment request for this date and machine ({recent_duplicate.booking_reference}). Our coordinator will contact you shortly!",
                    )
                    return redirect("user:appointment")

                appointment_obj = form.save()
                transaction.on_commit(lambda: queue_appointment_sync(appointment_obj))
                messages.success(
                    request,
                    f"Thank you, {appointment_obj.name}! Your appointment request ({appointment_obj.booking_reference}) has been received. Our wellness coordinator will contact you shortly to confirm schedule availability.",
                )
                return redirect("user:appointment")
            else:
                messages.error(
                    request,
                    "Please correct the errors in the appointment form before submitting.",
                )
        else:
            initial_data = {}
            if selected_service:
                initial_data["service"] = selected_service.id
            form = AppointmentForm(initial=initial_data)

        context = {
            "form": form,
            "services": active_services,
            "selected_service": selected_service,
            "selected_service_id": (
                selected_service.id if selected_service else None
            ),
            "today_date": timezone.localdate().strftime("%Y-%m-%d"),
        }
        return render(request, "appointment.html", context)

    except DatabaseError as e:
        logger.error(f"Database error loading appointments page: {e}", exc_info=True)
        messages.error(
            request,
            "A temporary database error occurred. Please try again in a few moments.",
        )
        return render(
            request,
            "appointment.html",
            {
                "form": AppointmentForm(),
                "services": Service.objects.none(),
                "selected_service": None,
                "selected_service_id": None,
                "today_date": timezone.localdate().strftime("%Y-%m-%d"),
            },
        )

def blog(request):
    return render(request, "blog.html")


def blog_detail(request):
    return render(request, "blog-detail.html")


def bmi_calculator(request):
    return render(request, "bmi-calculator.html")


def certificates(request):
    return render(request, "certificates.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_phone = form.cleaned_data.get("phone")
            cleaned_message = form.cleaned_data.get("message", "").strip()

            # Duplicate submission check within 2 minutes
            recent_cutoff = timezone.now() - timedelta(minutes=2)
            recent_duplicate = SupportRequest.objects.filter(
                phone=cleaned_phone,
                message=cleaned_message,
                created_at__gte=recent_cutoff,
            ).first()

            if recent_duplicate:
                messages.info(
                    request,
                    f"We have already received your message recently (Ticket: {recent_duplicate.ticket_number}). Our team is reviewing it and will get back to you shortly.",
                )
                return redirect("user:contact")

            support_obj = form.save()
            transaction.on_commit(lambda: queue_support_request_sync(support_obj))
            messages.success(
                request,
                f"Thank you, {support_obj.name}! Your message has been received (Ticket: {support_obj.ticket_number}). Our wellness care advisory team will contact you shortly.",
            )
            return redirect("user:contact")
        else:
            messages.error(
                request,
                "Please correct the errors in the contact form before submitting.",
            )
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})



def digital_profile(request):
    return render(request, "digital-profile.html")


def enquiry(request):
    try:
        active_services = (
            Service.objects.filter(
                is_active=True,
                category__is_active=True,
            )
            .select_related("category")
            .order_by("category__name", "display_order", "name")
        )

        selected_service = None
        service_param = (
            request.GET.get("service") or request.GET.get("id") or ""
        ).strip()
        if service_param:
            if service_param.isdigit():
                selected_service = active_services.filter(
                    id=int(service_param)
                ).first()
            else:
                selected_service = active_services.filter(
                    slug=service_param
                ).first()

        if request.method == "POST":
            form = EnquiryForm(request.POST)
            if form.is_valid():
                cleaned_phone = form.cleaned_data.get("phone")
                cleaned_service = form.cleaned_data.get("service")

                # Duplicate submission check within 2 minutes
                recent_cutoff = timezone.now() - timedelta(minutes=2)
                recent_duplicate = Enquiry.objects.filter(
                    phone=cleaned_phone,
                    service=cleaned_service,
                    created_at__gte=recent_cutoff,
                ).first()

                if recent_duplicate:
                    messages.info(
                        request,
                        "We have already received your enquiry recently. Our therapy advisory team will contact you shortly!",
                    )
                    return redirect("user:enquiry")

                enquiry_obj = form.save()
                transaction.on_commit(lambda: queue_enquiry_sync(enquiry_obj))
                messages.success(
                    request,
                    f"Thank you, {enquiry_obj.name}! Your enquiry has been received. Our wellness specialist will contact you within 24 hours.",
                )
                return redirect("user:enquiry")
            else:
                messages.error(
                    request,
                    "Please correct the errors in the enquiry form before submitting.",
                )
        else:
            initial_data = {}
            if selected_service:
                initial_data["service"] = selected_service.id
            form = EnquiryForm(initial=initial_data)

        context = {
            "form": form,
            "services": active_services,
            "selected_service": selected_service,
            "selected_service_id": (
                selected_service.id if selected_service else None
            ),
        }
        return render(request, "enquiry.html", context)

    except DatabaseError:
        logger.exception(
            "Database error occurred while processing customer enquiry."
        )
        raise


def faq(request):
    return render(request, "faq.html")


def gallery(request):
    return render(request, "gallery.html")


def offers(request):
    try:
        now = timezone.now()
        active_offers = (
            Offer.objects.filter(is_active=True)
            .filter(Q(valid_from__isnull=True) | Q(valid_from__lte=now))
            .filter(Q(valid_until__isnull=True) | Q(valid_until__gte=now))
            .order_by("display_order", "-created_at")
        )
        return render(request, "offers.html", {"offers": active_offers})
    except DatabaseError:
        logger.exception("Failed to load offers.")
        raise


def support(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            cleaned_phone = form.cleaned_data.get("phone")
            cleaned_message = form.cleaned_data.get("message", "").strip()

            # Duplicate submission check within 2 minutes
            recent_cutoff = timezone.now() - timedelta(minutes=2)
            recent_duplicate = SupportRequest.objects.filter(
                phone=cleaned_phone,
                message=cleaned_message,
                created_at__gte=recent_cutoff,
            ).first()

            if recent_duplicate:
                messages.info(
                    request,
                    f"We have already received this support ticket recently (Ticket: {recent_duplicate.ticket_number}). Our technicians are reviewing your issue.",
                )
                return redirect("user:support")

            ticket_obj = form.save()
            transaction.on_commit(lambda: queue_support_request_sync(ticket_obj))
            messages.success(
                request,
                f"Thank you, {ticket_obj.name}! Your support ticket ({ticket_obj.ticket_number}) has been created. Our technical support team reviews all requests within 4 business hours.",
            )
            return redirect("user:support")
        else:
            messages.error(
                request,
                "Please correct the highlighted errors before submitting the support ticket.",
            )
    else:
        form = SupportTicketForm()

    return render(request, "support.html", {"form": form})



def testimonials(request):
    return render(request, "testimonials.html")
