from datetime import timedelta
from functools import wraps
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from user.models import (
    Announcement,
    Appointment,
    Category,
    CustomerNeed,
    BodyPart,
    Enquiry,
    IntendedUse,
    Offer,
    Service,
    ServiceType,
    SiteSettings,
    SupportRequest,
    GoogleSheetsSyncRecord,
)
from .forms import (
    AdminLoginForm,
    AppointmentStatusForm,
    CategoryAdminForm,
    EnquiryStatusForm,
    ServiceAdminForm,
    SiteSettingsForm,
    SupportRequestStatusForm,
)


def staff_required(view_func):
    """
    Decorator requiring an authenticated staff user.
    Redirects unauthenticated users to the custom admin login with ?next=.
    Rejects authenticated non-staff users with HTTP 403 Forbidden.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse("custom_admin:login")
            return redirect(f"{login_url}?next={request.get_full_path()}")
        if not request.user.is_staff:
            return render(
                request,
                "custom_admin/access_denied.html",
                {
                    "user": request.user,
                    "message": "Staff privileges are required to access the admin portal.",
                },
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def login_view(request):
    """
    Custom admin login view.
    Validates staff credentials and safe redirect destination.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("custom_admin:dashboard")

    redirect_to = request.POST.get("next") or request.GET.get("next") or ""

    if request.method == "POST":
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_staff:
                messages.error(
                    request,
                    "Access denied. Only registered staff members may access this portal.",
                )
                return render(request, "custom_admin/login.html", {"form": form, "next": redirect_to})

            auth_login(request, user)

            # Security: Validate redirect destination to prevent open redirects
            if redirect_to and url_has_allowed_host_and_scheme(
                url=redirect_to,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(redirect_to)
            return redirect("custom_admin:dashboard")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AdminLoginForm(request)

    return render(
        request,
        "custom_admin/login.html",
        {"form": form, "next": redirect_to},
    )


@require_POST
def logout_view(request):
    """
    Custom admin logout view.
    Requires POST with CSRF protection to prevent malicious logout CSRF.
    """
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, "You have been logged out of the admin portal.")
    return redirect("custom_admin:login")


@staff_required
def dashboard(request):
    total_enquiries = Enquiry.objects.count()
    new_enquiries_count = Enquiry.objects.filter(status=Enquiry.Status.NEW).count()
    followup_enquiries_count = Enquiry.objects.filter(
        status__in=[Enquiry.Status.NEW, Enquiry.Status.CONTACTED, Enquiry.Status.IN_DISCUSSION]
    ).count()
    total_appointments = Appointment.objects.count()
    total_services = Service.objects.count()
    active_services_count = Service.objects.filter(is_active=True).count()
    total_categories = Category.objects.count()
    total_offers = Offer.objects.count()
    total_support_requests = SupportRequest.objects.count()
    new_support_requests_count = SupportRequest.objects.filter(status=SupportRequest.Status.NEW).count()

    recent_enquiries = Enquiry.objects.select_related("service").order_by("-created_at")[:5]
    recent_appointments = Appointment.objects.select_related("service").order_by("-created_at")[:5]
    recent_support_requests = SupportRequest.objects.order_by("-created_at")[:5]
    featured_services = Service.objects.select_related("category").order_by("display_order", "name")[:6]

    context = {
        "total_enquiries": total_enquiries,
        "new_enquiries_count": new_enquiries_count,
        "followup_enquiries_count": followup_enquiries_count,
        "total_appointments": total_appointments,
        "total_services": total_services,
        "active_services_count": active_services_count,
        "total_categories": total_categories,
        "total_offers": total_offers,
        "total_support_requests": total_support_requests,
        "new_support_requests_count": new_support_requests_count,
        "recent_enquiries": recent_enquiries,
        "recent_appointments": recent_appointments,
        "recent_support_requests": recent_support_requests,
        "featured_services": featured_services,
    }
    return render(request, "custom_admin/index.html", context)


# =========================================================================
# SERVICES MANAGEMENT
# =========================================================================

@staff_required
def services(request):
    search_query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    status_filter = request.GET.get("status", "").strip()
    featured_filter = request.GET.get("featured", "").strip()
    sort_by = request.GET.get("sort", "-created_at").strip()

    services_qs = (
        Service.objects.select_related("category")
        .prefetch_related("customer_needs", "body_parts", "service_types", "intended_uses")
    )

    if search_query:
        services_qs = services_qs.filter(
            Q(name__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
        )

    if category_slug:
        services_qs = services_qs.filter(category__slug=category_slug)

    if status_filter == "active":
        services_qs = services_qs.filter(is_active=True)
    elif status_filter == "inactive":
        services_qs = services_qs.filter(is_active=False)

    if featured_filter == "1":
        services_qs = services_qs.filter(is_featured=True)

    if sort_by == "name":
        services_qs = services_qs.order_by("name")
    elif sort_by == "display_order":
        services_qs = services_qs.order_by("display_order", "name")
    elif sort_by == "oldest":
        services_qs = services_qs.order_by("created_at")
    else:
        services_qs = services_qs.order_by("-created_at")

    # Metrics
    total_count = Service.objects.count()
    active_count = Service.objects.filter(is_active=True).count()
    inactive_count = Service.objects.filter(is_active=False).count()

    paginator = Paginator(services_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    categories = Category.objects.all().order_by("name")

    query_params = request.GET.copy()
    query_params.pop("page", None)

    return render(
        request,
        "custom_admin/services.html",
        {
            "page_obj": page_obj,
            "services": page_obj.object_list,
            "categories": categories,
            "total_count": total_count,
            "active_count": active_count,
            "inactive_count": inactive_count,
            "search_query": search_query,
            "selected_category": category_slug,
            "selected_status": status_filter,
            "selected_featured": featured_filter,
            "selected_sort": sort_by,
            "pagination_querystring": query_params.urlencode(),
        },
    )


@staff_required
def service_create(request):
    if request.method == "POST":
        form = ServiceAdminForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            messages.success(
                request,
                f"Therapy solution '{service.name}' was created successfully.",
            )
            return redirect("custom_admin:services")
        else:
            messages.error(
                request,
                "Please review and correct the errors below before submitting.",
            )
    else:
        form = ServiceAdminForm()

    return render(
        request,
        "custom_admin/service_form.html",
        {
            "form": form,
            "title": "Add New Therapy Solution",
            "is_edit": False,
        },
    )


@staff_required
def service_edit(request, service_id):
    service = get_object_or_404(
        Service.objects.select_related("category").prefetch_related(
            "customer_needs", "body_parts", "service_types", "intended_uses"
        ),
        id=service_id,
    )

    if request.method == "POST":
        form = ServiceAdminForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save()
            messages.success(
                request,
                f"Therapy solution '{service.name}' has been updated successfully.",
            )
            return redirect("custom_admin:services")
        else:
            messages.error(
                request,
                "Please review and correct the errors below before saving.",
            )
    else:
        form = ServiceAdminForm(instance=service)

    return render(
        request,
        "custom_admin/service_form.html",
        {
            "form": form,
            "service": service,
            "title": f"Edit Solution: {service.name}",
            "is_edit": True,
        },
    )


@staff_required
@require_POST
def service_toggle_active(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.is_active = not service.is_active
    service.save(update_fields=["is_active"])

    status_str = "activated" if service.is_active else "deactivated"
    messages.success(
        request,
        f"Product '{service.name}' has been {status_str} and visibility updated on the public site.",
    )
    return redirect(request.POST.get("next") or "custom_admin:services")


@staff_required
@require_POST
def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service_name = service.name
    service.delete()
    messages.success(
        request,
        f"Therapy solution '{service_name}' has been permanently deleted.",
    )
    return redirect(request.POST.get("next") or "custom_admin:services")


# =========================================================================
# CATEGORIES MANAGEMENT
# =========================================================================

@staff_required
def categories(request):
    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()

    categories_qs = Category.objects.annotate(
        service_count=Count("services")
    )

    if search_query:
        categories_qs = categories_qs.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if status_filter == "active":
        categories_qs = categories_qs.filter(is_active=True)
    elif status_filter == "inactive":
        categories_qs = categories_qs.filter(is_active=False)

    categories_qs = categories_qs.order_by("display_order", "name")

    total_count = Category.objects.count()
    active_count = Category.objects.filter(is_active=True).count()
    inactive_count = Category.objects.filter(is_active=False).count()

    paginator = Paginator(categories_qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    query_params = request.GET.copy()
    query_params.pop("page", None)

    return render(
        request,
        "custom_admin/categories.html",
        {
            "page_obj": page_obj,
            "categories": page_obj.object_list,
            "total_count": total_count,
            "active_count": active_count,
            "inactive_count": inactive_count,
            "search_query": search_query,
            "selected_status": status_filter,
            "pagination_querystring": query_params.urlencode(),
        },
    )


@staff_required
def category_create(request):
    if request.method == "POST":
        form = CategoryAdminForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(
                request,
                f"Category '{category.name}' created successfully.",
            )
            return redirect("custom_admin:categories")
        else:
            messages.error(
                request,
                "Please correct the errors in the category form below.",
            )
    else:
        form = CategoryAdminForm()

    return render(
        request,
        "custom_admin/category_form.html",
        {
            "form": form,
            "title": "Add New Category",
            "is_edit": False,
        },
    )


@staff_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = CategoryAdminForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(
                request,
                f"Category '{category.name}' updated successfully.",
            )
            return redirect("custom_admin:categories")
        else:
            messages.error(
                request,
                "Please correct the errors in the category form below.",
            )
    else:
        form = CategoryAdminForm(instance=category)

    return render(
        request,
        "custom_admin/category_form.html",
        {
            "form": form,
            "category": category,
            "title": f"Edit Category: {category.name}",
            "is_edit": True,
        },
    )


@staff_required
@require_POST
def category_toggle_active(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.is_active = not category.is_active
    category.save(update_fields=["is_active"])

    status_str = "activated" if category.is_active else "deactivated"
    messages.success(
        request,
        f"Category '{category.name}' is now {status_str}.",
    )
    return redirect(request.POST.get("next") or "custom_admin:categories")


@staff_required
@require_POST
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    services_count = category.services.count()
    if services_count > 0:
        messages.error(
            request,
            f"Cannot delete category '{category.name}' because it contains {services_count} active therapy solution(s). Please reassign or delete these solutions first.",
        )
        return redirect(request.POST.get("next") or "custom_admin:categories")

    category_name = category.name
    category.delete()
    messages.success(
        request,
        f"Category '{category_name}' has been permanently deleted.",
    )
    return redirect(request.POST.get("next") or "custom_admin:categories")


# =========================================================================
# ENQUIRIES, APPOINTMENTS, OFFERS & SETTINGS
# =========================================================================

@staff_required
def enquiries(request):
    status_filter = request.GET.get("status", "").strip()
    search_query = request.GET.get("q", "").strip()
    service_filter = request.GET.get("service", "").strip()
    date_filter = request.GET.get("date_range", "").strip()
    sort_by = request.GET.get("sort", "-created_at").strip()

    enquiries_qs = Enquiry.objects.select_related("service", "service__category")

    if status_filter:
        enquiries_qs = enquiries_qs.filter(status=status_filter)

    if search_query:
        enquiries_qs = enquiries_qs.filter(
            Q(name__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(city__icontains=search_query)
            | Q(message__icontains=search_query)
        )

    if service_filter:
        if service_filter.isdigit():
            enquiries_qs = enquiries_qs.filter(service_id=int(service_filter))
        else:
            enquiries_qs = enquiries_qs.filter(service__slug=service_filter)

    now = timezone.now()
    if date_filter == "today":
        enquiries_qs = enquiries_qs.filter(created_at__date=now.date())
    elif date_filter == "week":
        enquiries_qs = enquiries_qs.filter(created_at__gte=now - timedelta(days=7))
    elif date_filter == "month":
        enquiries_qs = enquiries_qs.filter(created_at__gte=now - timedelta(days=30))

    if sort_by == "oldest":
        enquiries_qs = enquiries_qs.order_by("created_at")
    elif sort_by == "name":
        enquiries_qs = enquiries_qs.order_by("name")
    else:
        enquiries_qs = enquiries_qs.order_by("-created_at")

    total_count = Enquiry.objects.count()
    new_count = Enquiry.objects.filter(status=Enquiry.Status.NEW).count()
    followup_count = Enquiry.objects.filter(
        status__in=[Enquiry.Status.NEW, Enquiry.Status.CONTACTED, Enquiry.Status.IN_DISCUSSION]
    ).count()
    resolved_count = Enquiry.objects.filter(
        status__in=[Enquiry.Status.RESOLVED, Enquiry.Status.CLOSED]
    ).count()

    paginator = Paginator(enquiries_qs, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

    services_list = Service.objects.all().order_by("name")

    query_params = request.GET.copy()
    query_params.pop("page", None)

    return render(
        request,
        "custom_admin/enquiries.html",
        {
            "page_obj": page_obj,
            "enquiries": page_obj.object_list,
            "services": services_list,
            "total_count": total_count,
            "new_count": new_count,
            "followup_count": followup_count,
            "resolved_count": resolved_count,
            "selected_status": status_filter,
            "status_choices": Enquiry.Status.choices,
            "search_query": search_query,
            "selected_service": service_filter,
            "selected_date_range": date_filter,
            "selected_sort": sort_by,
            "pagination_querystring": query_params.urlencode(),
        },
    )


@staff_required
def enquiry_detail(request, enquiry_id):
    enquiry = get_object_or_404(
        Enquiry.objects.select_related("service", "service__category"),
        id=enquiry_id,
    )

    if request.method == "POST":
        form = EnquiryStatusForm(request.POST, instance=enquiry)
        if form.is_valid():
            enquiry = form.save()
            messages.success(
                request,
                f"Enquiry #{enquiry.id} updated successfully. Status is now '{enquiry.get_status_display()}'.",
            )
            return redirect("custom_admin:enquiries")
        else:
            messages.error(
                request,
                "Failed to update enquiry. Please check the submitted fields.",
            )
    else:
        form = EnquiryStatusForm(instance=enquiry)

    return render(
        request,
        "custom_admin/enquiry_detail.html",
        {
            "enquiry": enquiry,
            "form": form,
            "status_choices": Enquiry.Status.choices,
        },
    )


@staff_required
@require_POST
def update_enquiry_status(request, enquiry_id):
    enquiry_obj = get_object_or_404(Enquiry, id=enquiry_id)
    new_status = request.POST.get("status", "").strip()
    admin_notes = request.POST.get("admin_notes")

    if new_status not in dict(Enquiry.Status.choices):
        messages.error(request, f"Invalid status choice '{new_status}' provided.")
        return redirect(request.POST.get("next") or "custom_admin:enquiries")

    enquiry_obj.status = new_status
    if admin_notes is not None:
        enquiry_obj.admin_notes = admin_notes.strip()
    enquiry_obj.save()

    messages.success(
        request,
        f"Enquiry #{enquiry_obj.id} status updated to {enquiry_obj.get_status_display()}.",
    )
    return redirect(request.POST.get("next") or "custom_admin:enquiries")


@staff_required
@require_POST
def enquiry_delete(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    enquiry_id_val = enquiry.id
    # Clean up local sync tracking record without calling external Google Sheets API
    GoogleSheetsSyncRecord.objects.filter(
        source_type=GoogleSheetsSyncRecord.SourceType.ENQUIRY,
        source_id=enquiry_id_val,
    ).delete()
    enquiry.delete()
    messages.success(
        request,
        f"Enquiry #{enquiry_id_val} has been permanently deleted.",
    )
    return redirect(request.POST.get("next") or "custom_admin:enquiries")


@staff_required
def appointments(request):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        new_status = request.POST.get("status", "").strip()
        admin_notes = request.POST.get("admin_notes")
        apt_obj = get_object_or_404(Appointment, id=appointment_id)
        if new_status in dict(Appointment.Status.choices):
            apt_obj.status = new_status
            if admin_notes is not None:
                apt_obj.admin_notes = admin_notes.strip()
            apt_obj.save()
            messages.success(
                request,
                f"Appointment {apt_obj.booking_reference} updated to {apt_obj.get_status_display()}.",
            )
        else:
            messages.error(request, f"Invalid appointment status '{new_status}'.")
        return redirect(request.POST.get("next") or "custom_admin:appointments")

    queryset = (
        Appointment.objects.select_related("service", "service__category")
        .all()
    )

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    service_filter = request.GET.get("service", "").strip()
    date_filter = request.GET.get("date_range", "").strip()
    demo_format_filter = request.GET.get("demo_format", "").strip()
    sort_by = request.GET.get("sort", "-appointment_date").strip()

    if search_query:
        queryset = queryset.filter(
            Q(booking_reference__icontains=search_query)
            | Q(name__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(city__icontains=search_query)
            | Q(service_name_snapshot__icontains=search_query)
            | Q(service__name__icontains=search_query)
        )

    if status_filter and status_filter in dict(Appointment.Status.choices):
        queryset = queryset.filter(status=status_filter)

    if service_filter:
        if service_filter.isdigit():
            queryset = queryset.filter(service_id=int(service_filter))
        else:
            queryset = queryset.filter(service__slug=service_filter)

    today = timezone.localdate()
    if date_filter == "today":
        queryset = queryset.filter(appointment_date=today)
    elif date_filter == "upcoming":
        queryset = queryset.filter(appointment_date__gte=today)
    elif date_filter == "past":
        queryset = queryset.filter(appointment_date__lt=today)
    elif date_filter == "week":
        queryset = queryset.filter(appointment_date__gte=today, appointment_date__lte=today + timedelta(days=7))
    elif date_filter == "month":
        queryset = queryset.filter(appointment_date__gte=today, appointment_date__lte=today + timedelta(days=30))

    if demo_format_filter and demo_format_filter in dict(Appointment.DemoFormat.choices):
        queryset = queryset.filter(demo_format=demo_format_filter)

    if sort_by == "appointment_date":
        queryset = queryset.order_by("appointment_date", "time_slot", "-created_at")
    elif sort_by == "name":
        queryset = queryset.order_by("name")
    elif sort_by == "newest":
        queryset = queryset.order_by("-created_at")
    else:
        queryset = queryset.order_by("-appointment_date", "-created_at")

    total_count = Appointment.objects.count()
    pending_count = Appointment.objects.filter(status=Appointment.Status.PENDING).count()
    confirmed_count = Appointment.objects.filter(status=Appointment.Status.CONFIRMED).count()
    completed_count = Appointment.objects.filter(status=Appointment.Status.COMPLETED).count()
    cancelled_count = Appointment.objects.filter(status=Appointment.Status.CANCELLED).count()

    paginator = Paginator(queryset, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    services_list = Service.objects.all().order_by("name")

    query_params = request.GET.copy()
    query_params.pop("page", None)

    return render(
        request,
        "custom_admin/appointments.html",
        {
            "page_obj": page_obj,
            "appointments": page_obj.object_list,
            "services": services_list,
            "search_query": search_query,
            "status_filter": status_filter,
            "selected_service": service_filter,
            "selected_date_range": date_filter,
            "selected_demo_format": demo_format_filter,
            "selected_sort": sort_by,
            "status_choices": Appointment.Status.choices,
            "demo_format_choices": Appointment.DemoFormat.choices,
            "total_count": total_count,
            "pending_count": pending_count,
            "confirmed_count": confirmed_count,
            "completed_count": completed_count,
            "cancelled_count": cancelled_count,
            "pagination_querystring": query_params.urlencode(),
        },
    )


@staff_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(
        Appointment.objects.select_related("service", "service__category"),
        id=appointment_id,
    )

    if request.method == "POST":
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            apt = form.save()
            messages.success(
                request,
                f"Appointment {apt.booking_reference} updated successfully. Status is now '{apt.get_status_display()}'.",
            )
            return redirect("custom_admin:appointments")
        else:
            messages.error(
                request,
                "Failed to update appointment. Please verify the submitted form.",
            )
    else:
        form = AppointmentStatusForm(instance=appointment)

    return render(
        request,
        "custom_admin/appointment_detail.html",
        {
            "appointment": appointment,
            "form": form,
            "status_choices": Appointment.Status.choices,
        },
    )


@staff_required
@require_POST
def update_appointment_status(request, appointment_id):
    apt_obj = get_object_or_404(Appointment, id=appointment_id)
    new_status = request.POST.get("status", "").strip()
    admin_notes = request.POST.get("admin_notes")

    if new_status not in dict(Appointment.Status.choices):
        messages.error(request, f"Invalid appointment status choice '{new_status}' provided.")
        return redirect(request.POST.get("next") or "custom_admin:appointments")

    apt_obj.status = new_status
    if admin_notes is not None:
        apt_obj.admin_notes = admin_notes.strip()
    apt_obj.save()

    messages.success(
        request,
        f"Appointment {apt_obj.booking_reference} status updated to {apt_obj.get_status_display()}.",
    )
    return redirect(request.POST.get("next") or "custom_admin:appointments")


@staff_required
@require_POST
def appointment_delete(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    booking_ref = appointment.booking_reference
    apt_id_val = appointment.id
    # Clean up local sync tracking record without calling external Google Sheets API
    GoogleSheetsSyncRecord.objects.filter(
        source_type=GoogleSheetsSyncRecord.SourceType.APPOINTMENT,
        source_id=apt_id_val,
    ).delete()
    appointment.delete()
    messages.success(
        request,
        f"Appointment {booking_ref} has been permanently deleted.",
    )
    return redirect(request.POST.get("next") or "custom_admin:appointments")


@staff_required
def offers(request):
    offers_list = Offer.objects.all().order_by("display_order", "-created_at")
    announcements = Announcement.objects.all().order_by("display_order", "-created_at")
    return render(
        request,
        "custom_admin/offers.html",
        {
            "offers": offers_list,
            "announcements": announcements,
        },
    )


@staff_required
@require_POST
def offer_toggle_active(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    offer.is_active = not offer.is_active
    offer.save(update_fields=["is_active"])
    status_str = "activated" if offer.is_active else "deactivated"
    messages.success(
        request,
        f"Promotional offer '{offer.title}' has been {status_str}.",
    )
    return redirect(request.POST.get("next") or "custom_admin:offers")


@staff_required
@require_POST
def offer_delete(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    offer_title = offer.title
    offer.delete()
    messages.success(
        request,
        f"Promotional offer '{offer_title}' has been permanently deleted.",
    )
    return redirect(request.POST.get("next") or "custom_admin:offers")


@staff_required
@require_POST
def announcement_toggle_active(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.is_active = not announcement.is_active
    announcement.save(update_fields=["is_active"])
    status_str = "activated" if announcement.is_active else "deactivated"
    messages.success(
        request,
        f"Top banner announcement has been {status_str}.",
    )
    return redirect(request.POST.get("next") or "custom_admin:offers")


@staff_required
@require_POST
def announcement_delete(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    short_msg = announcement.message[:40]
    announcement.delete()
    messages.success(
        request,
        f"Announcement banner '{short_msg}...' has been permanently deleted.",
    )
    return redirect(request.POST.get("next") or "custom_admin:offers")


@staff_required
def settings_view(request):
    settings_obj = SiteSettings.load()
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Website and business settings saved successfully.")
            return redirect("custom_admin:settings")
        else:
            messages.error(request, "Failed to save settings. Please verify the submitted information.")
    else:
        form = SiteSettingsForm(instance=settings_obj)

    return render(
        request,
        "custom_admin/settings.html",
        {
            "form": form,
            "site_settings": settings_obj,
        },
    )


# =========================================================================
# SUPPORT REQUESTS MANAGEMENT
# =========================================================================

@staff_required
def support_requests(request):
    queryset = SupportRequest.objects.all()

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    type_filter = request.GET.get("type", "").strip()
    sort_by = request.GET.get("sort", "-created_at").strip()

    if search_query:
        queryset = queryset.filter(
            Q(ticket_number__icontains=search_query)
            | Q(name__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(subject__icontains=search_query)
            | Q(product_name__icontains=search_query)
            | Q(message__icontains=search_query)
        )

    if status_filter and status_filter in dict(SupportRequest.Status.choices):
        queryset = queryset.filter(status=status_filter)

    if type_filter and type_filter in dict(SupportRequest.RequestType.choices):
        queryset = queryset.filter(request_type=type_filter)

    if sort_by == "oldest":
        queryset = queryset.order_by("created_at")
    elif sort_by == "name":
        queryset = queryset.order_by("name")
    else:
        queryset = queryset.order_by("-created_at")

    total_count = SupportRequest.objects.count()
    new_count = SupportRequest.objects.filter(status=SupportRequest.Status.NEW).count()
    in_progress_count = SupportRequest.objects.filter(status=SupportRequest.Status.IN_PROGRESS).count()
    resolved_count = SupportRequest.objects.filter(status=SupportRequest.Status.RESOLVED).count()
    closed_count = SupportRequest.objects.filter(status=SupportRequest.Status.CLOSED).count()

    paginator = Paginator(queryset, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)

    return render(
        request,
        "custom_admin/support_requests.html",
        {
            "page_obj": page_obj,
            "support_requests": page_obj.object_list,
            "search_query": search_query,
            "status_filter": status_filter,
            "selected_type": type_filter,
            "selected_sort": sort_by,
            "status_choices": SupportRequest.Status.choices,
            "type_choices": SupportRequest.RequestType.choices,
            "total_count": total_count,
            "new_count": new_count,
            "in_progress_count": in_progress_count,
            "resolved_count": resolved_count,
            "closed_count": closed_count,
            "pagination_querystring": query_params.urlencode(),
        },
    )


@staff_required
def support_request_detail(request, request_id):
    req_obj = get_object_or_404(SupportRequest, id=request_id)

    if request.method == "POST":
        form = SupportRequestStatusForm(request.POST, instance=req_obj)
        if form.is_valid():
            saved_obj = form.save()
            messages.success(
                request,
                f"Support Request {saved_obj.ticket_number} updated successfully. Status is now '{saved_obj.get_status_display()}'.",
            )
            return redirect("custom_admin:support_requests")
        else:
            messages.error(
                request,
                "Failed to update support request. Please verify the submitted form.",
            )
    else:
        form = SupportRequestStatusForm(instance=req_obj)

    return render(
        request,
        "custom_admin/support_request_detail.html",
        {
            "support_request": req_obj,
            "form": form,
            "status_choices": SupportRequest.Status.choices,
        },
    )


@staff_required
@require_POST
def update_support_request_status(request, request_id):
    req_obj = get_object_or_404(SupportRequest, id=request_id)
    new_status = request.POST.get("status", "").strip()
    admin_notes = request.POST.get("admin_notes")

    if new_status not in dict(SupportRequest.Status.choices):
        messages.error(request, f"Invalid support request status choice '{new_status}' provided.")
        return redirect(request.POST.get("next") or "custom_admin:support_requests")

    req_obj.status = new_status
    if admin_notes is not None:
        req_obj.admin_notes = admin_notes.strip()
    req_obj.save()

    messages.success(
        request,
        f"Support request {req_obj.ticket_number} status updated to {req_obj.get_status_display()}.",
    )
    return redirect(request.POST.get("next") or "custom_admin:support_requests")


@staff_required
@require_POST
def support_request_delete(request, request_id):
    req_obj = get_object_or_404(SupportRequest, id=request_id)
    ticket_num = req_obj.ticket_number
    req_id_val = req_obj.id
    # Clean up local sync tracking record without calling external Google Sheets API
    GoogleSheetsSyncRecord.objects.filter(
        source_type=GoogleSheetsSyncRecord.SourceType.SUPPORT_REQUEST,
        source_id=req_id_val,
    ).delete()
    req_obj.delete()
    messages.success(
        request,
        f"Support request {ticket_num} has been permanently deleted.",
    )
    return redirect(request.POST.get("next") or "custom_admin:support_requests")


@staff_required
def google_sheets_sync_monitor(request):
    """
    Staff-only monitoring view for Google Sheets synchronization.
    Displays queue statistics, sync state, and recent sync records.
    Never exposes credentials, raw payloads, or private customer data.
    """
    from user.google_sheets import get_sheets_config_diagnostics

    diagnostics = get_sheets_config_diagnostics()

    status_filter = request.GET.get("status", "").strip()
    source_filter = request.GET.get("source_type", "").strip()

    records_qs = GoogleSheetsSyncRecord.objects.all().order_by("-updated_at")

    if status_filter:
        records_qs = records_qs.filter(status=status_filter)
    if source_filter:
        records_qs = records_qs.filter(source_type=source_filter)

    counts = {
        "total": GoogleSheetsSyncRecord.objects.count(),
        "pending": GoogleSheetsSyncRecord.objects.filter(status=GoogleSheetsSyncRecord.SyncStatus.PENDING).count(),
        "synced": GoogleSheetsSyncRecord.objects.filter(status=GoogleSheetsSyncRecord.SyncStatus.SYNCED).count(),
        "failed": GoogleSheetsSyncRecord.objects.filter(status=GoogleSheetsSyncRecord.SyncStatus.FAILED).count(),
        "in_progress": GoogleSheetsSyncRecord.objects.filter(status=GoogleSheetsSyncRecord.SyncStatus.IN_PROGRESS).count(),
    }

    paginator = Paginator(records_qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "custom_admin/google_sheets_sync.html",
        {
            "diagnostics": diagnostics,
            "counts": counts,
            "page_obj": page_obj,
            "status_filter": status_filter,
            "source_filter": source_filter,
            "status_choices": GoogleSheetsSyncRecord.SyncStatus.choices,
            "source_choices": GoogleSheetsSyncRecord.SourceType.choices,
        },
    )


@staff_required
@require_POST
def google_sheets_retry_action(request, sync_id):
    """
    Staff-authorized, POST-only manual retry action for an individual sync record.
    """
    from user.google_sheets import sync_single_record

    sync_record = get_object_or_404(GoogleSheetsSyncRecord, id=sync_id)

    # Trigger single record sync
    result = sync_single_record(sync_record)
    if result.get("success"):
        messages.success(
            request,
            f"Successfully synchronized {sync_record.get_source_type_display()} [{sync_record.source_identifier}] to '{sync_record.sheet_name}' (row {sync_record.row_index}).",
        )
    else:
        messages.error(
            request,
            f"Retry failed for [{sync_record.source_identifier}]: {result.get('message', 'Sync error')}",
        )

    return redirect(request.POST.get("next") or reverse("custom_admin:google_sheets_sync"))


@staff_required
@require_POST
def google_sheets_retry_all_failed(request):
    """
    Staff-authorized, POST-only batch retry action for all failed eligible records.
    """
    from user.google_sheets import process_pending_syncs

    failed_records = GoogleSheetsSyncRecord.objects.filter(status=GoogleSheetsSyncRecord.SyncStatus.FAILED)
    count = failed_records.count()
    if count == 0:
        messages.info(request, "No failed sync records to retry.")
        return redirect("custom_admin:google_sheets_sync")

    # Reset failed records to pending so process_pending_syncs will pick them up
    failed_records.update(status=GoogleSheetsSyncRecord.SyncStatus.PENDING, next_retry_at=timezone.now())

    results = process_pending_syncs(limit=50)
    messages.success(
        request,
        f"Batch retry completed: {results['succeeded']} succeeded, {results['failed']} failed out of {results['processed']} processed.",
    )

    return redirect("custom_admin:google_sheets_sync")


@staff_required
def notifications_api(request):
    """
    Staff-authorized JSON endpoint returning live unread notifications for
    appointments, customer enquiries, and support tickets.
    """
    from django.utils.timesince import timesince

    pending_appointments = list(
        Appointment.objects.filter(status='pending').select_related('service').order_by('-created_at')[:8]
    )
    new_enquiries = list(
        Enquiry.objects.filter(status='new').select_related('service').order_by('-created_at')[:8]
    )
    new_support_requests = list(
        SupportRequest.objects.filter(status='new').order_by('-created_at')[:8]
    )

    pending_count = Appointment.objects.filter(status='pending').count()
    enquiry_count = Enquiry.objects.filter(status='new').count()
    support_count = SupportRequest.objects.filter(status='new').count()
    total_count = pending_count + enquiry_count + support_count

    items = []

    for appt in pending_appointments:
        service_title = appt.service.name if appt.service else "General Booking"
        items.append({
            "type": "appointment",
            "title": "New Booking Request",
            "name": appt.name,
            "detail": f"{service_title} • {appt.appointment_date}",
            "time_ago": f"{timesince(appt.created_at)} ago" if appt.created_at else "",
            "url": reverse("custom_admin:appointment_detail", args=[appt.id]),
            "status": "Pending",
            "is_unread": True,
            "icon": "bi-calendar-check",
            "badge_color": "warning",
            "timestamp": appt.created_at.isoformat() if appt.created_at else "",
        })

    for enq in new_enquiries:
        enq_sub = (
            enq.service.name
            if enq.service
            else (enq.get_enquiry_type_display() if hasattr(enq, "get_enquiry_type_display") else "Enquiry")
        )
        items.append({
            "type": "enquiry",
            "title": "New Customer Enquiry",
            "name": enq.name,
            "detail": f"{enq_sub} • {enq.phone}",
            "time_ago": f"{timesince(enq.created_at)} ago" if enq.created_at else "",
            "url": reverse("custom_admin:enquiry_detail", args=[enq.id]),
            "status": "New",
            "is_unread": True,
            "icon": "bi-envelope-paper",
            "badge_color": "primary",
            "timestamp": enq.created_at.isoformat() if enq.created_at else "",
        })

    for sup in new_support_requests:
        items.append({
            "type": "support",
            "title": f"Support Ticket #{sup.ticket_number}",
            "name": sup.name,
            "detail": f"{sup.subject} • {sup.phone}",
            "time_ago": f"{timesince(sup.created_at)} ago" if sup.created_at else "",
            "url": reverse("custom_admin:support_request_detail", args=[sup.id]),
            "status": "New",
            "is_unread": True,
            "icon": "bi-headset",
            "badge_color": "info",
            "timestamp": sup.created_at.isoformat() if sup.created_at else "",
        })

    # If unread count is less than 5, backfill with most recent records for quick access
    if len(items) < 5:
        recent_appts = Appointment.objects.exclude(status='pending').select_related('service').order_by('-created_at')[:3]
        for appt in recent_appts:
            service_title = appt.service.name if appt.service else "General Booking"
            items.append({
                "type": "appointment",
                "title": "Booking Record",
                "name": appt.name,
                "detail": f"{service_title} • {appt.appointment_date}",
                "time_ago": f"{timesince(appt.created_at)} ago" if appt.created_at else "",
                "url": reverse("custom_admin:appointment_detail", args=[appt.id]),
                "status": appt.status.title(),
                "is_unread": False,
                "icon": "bi-calendar-check",
                "badge_color": "secondary",
                "timestamp": appt.created_at.isoformat() if appt.created_at else "",
            })

        recent_enqs = Enquiry.objects.exclude(status='new').select_related('service').order_by('-created_at')[:3]
        for enq in recent_enqs:
            items.append({
                "type": "enquiry",
                "title": "Customer Enquiry",
                "name": enq.name,
                "detail": enq.phone,
                "time_ago": f"{timesince(enq.created_at)} ago" if enq.created_at else "",
                "url": reverse("custom_admin:enquiry_detail", args=[enq.id]),
                "status": enq.status.title(),
                "is_unread": False,
                "icon": "bi-envelope-paper",
                "badge_color": "secondary",
                "timestamp": enq.created_at.isoformat() if enq.created_at else "",
            })

        recent_sups = SupportRequest.objects.exclude(status='new').order_by('-created_at')[:3]
        for sup in recent_sups:
            items.append({
                "type": "support",
                "title": f"Support Ticket #{sup.ticket_number}",
                "name": sup.name,
                "detail": sup.subject,
                "time_ago": f"{timesince(sup.created_at)} ago" if sup.created_at else "",
                "url": reverse("custom_admin:support_request_detail", args=[sup.id]),
                "status": sup.status.title(),
                "is_unread": False,
                "icon": "bi-headset",
                "badge_color": "secondary",
                "timestamp": sup.created_at.isoformat() if sup.created_at else "",
            })

    items.sort(key=lambda x: x["timestamp"], reverse=True)

    return JsonResponse({
        "success": True,
        "total_count": total_count,
        "pending_count": pending_count,
        "enquiry_count": enquiry_count,
        "support_count": support_count,
        "notifications": items[:10],
    })


