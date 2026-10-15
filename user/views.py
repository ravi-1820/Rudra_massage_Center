
import logging

from django.core.paginator import Paginator
from django.db import DatabaseError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import (
    Category,
    Service,
    CustomerNeed,
    BodyPart,
    ServiceType,
    IntendedUse,
)


logger = logging.getLogger(__name__)
SERVICES_PER_PAGE = 9


def home(request):
    return render(request, "index.html")


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
                category__slug=category_slug
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


def service_detail(request):
    service_slug = request.GET.get("slug", "").strip()
    service_id = request.GET.get("id", "").strip()

    active_services = Service.objects.select_related(
        "category"
    ).filter(
        is_active=True,
        category__is_active=True,
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

    related_services = Service.objects.filter(
        category=service.category,
        is_active=True,
        category__is_active=True,
    ).exclude(
        id=service.id
    ).order_by(
        "-is_featured",
        "display_order",
        "name",
    )[:4]

    return render(
        request,
        "service-detail.html",
        {
            "service": service,
            "related_services": related_services,
        },
    )


def appointment(request):
    return render(request, "appointment.html")


def blog(request):
    return render(request, "blog.html")


def blog_detail(request):
    return render(request, "blog-detail.html")


def bmi_calculator(request):
    return render(request, "bmi-calculator.html")


def certificates(request):
    return render(request, "certificates.html")


def contact(request):
    return render(request, "contact.html")


def digital_profile(request):
    return render(request, "digital-profile.html")


def enquiry(request):
    return render(request, "enquiry.html")


def faq(request):
    return render(request, "faq.html")


def gallery(request):
    return render(request, "gallery.html")


def offers(request):
    return render(request, "offers.html")


def support(request):
    return render(request, "support.html")


def testimonials(request):
    return render(request, "testimonials.html")
