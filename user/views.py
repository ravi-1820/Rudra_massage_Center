import logging
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Service, CustomerNeed, BodyPart, ServiceType, IntendedUse

logger = logging.getLogger(__name__)

SERVICES_PER_PAGE = 9


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    """
    Dynamic services catalogue view with keyword search, combined multi-dimensional
    filters (Customer Need, Body Part, Service Type, Intended Use, Category),
    sorting, and pagination.
    """
    try:
        search_query = request.GET.get('q', '').strip()
        selected_needs = [n.strip() for n in request.GET.getlist('need') if n.strip()]
        selected_body_parts = [b.strip() for b in request.GET.getlist('body') if b.strip()]
        selected_service_types = [t.strip() for t in request.GET.getlist('type') if t.strip()]
        selected_intended_uses = [u.strip() for u in request.GET.getlist('usage') if u.strip()]
        selected_category = request.GET.get('category', '').strip()
        sort_by = request.GET.get('sort', 'featured').strip()

        # Base queryset: only active services under active categories
        queryset = Service.objects.filter(
            is_active=True,
            category__is_active=True,
        ).select_related('category').prefetch_related(
            'customer_needs',
            'body_parts',
            'service_types',
            'intended_uses',
        )

        # A. Keyword Search
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

        # B. Customer Need Filter (matches slug, name, or numeric id)
        if selected_needs:
            need_q = Q(customer_needs__slug__in=selected_needs) | Q(customer_needs__name__in=selected_needs)
            numeric_ids = [n for n in selected_needs if n.isdigit()]
            if numeric_ids:
                need_q |= Q(customer_needs__id__in=numeric_ids)
            queryset = queryset.filter(need_q)

        # C. Body Part Filter
        if selected_body_parts:
            body_q = Q(body_parts__slug__in=selected_body_parts) | Q(body_parts__name__in=selected_body_parts)
            numeric_ids = [b for b in selected_body_parts if b.isdigit()]
            if numeric_ids:
                body_q |= Q(body_parts__id__in=numeric_ids)
            queryset = queryset.filter(body_q)

        # D. Service Type Filter
        if selected_service_types:
            type_q = Q(service_types__slug__in=selected_service_types) | Q(service_types__name__in=selected_service_types)
            numeric_ids = [t for t in selected_service_types if t.isdigit()]
            if numeric_ids:
                type_q |= Q(service_types__id__in=numeric_ids)
            queryset = queryset.filter(type_q)

        # E. Intended Use Filter
        if selected_intended_uses:
            usage_q = Q(intended_uses__slug__in=selected_intended_uses) | Q(intended_uses__name__in=selected_intended_uses)
            numeric_ids = [u for u in selected_intended_uses if u.isdigit()]
            if numeric_ids:
                usage_q |= Q(intended_uses__id__in=numeric_ids)
            queryset = queryset.filter(usage_q)

        # Category Filter (e.g. from header dropdown or category parameter)
        if selected_category:
            queryset = queryset.filter(
                Q(category__slug=selected_category) | Q(category__name__iexact=selected_category)
            )

        # Avoid duplicate services resulting from multiple many-to-many joins
        queryset = queryset.distinct()

        # Sorting logic
        if sort_by == 'name-asc':
            queryset = queryset.order_by('name')
        elif sort_by == 'name-desc':
            queryset = queryset.order_by('-name')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            # Default: Featured first, then display order, then name
            queryset = queryset.order_by('-is_featured', 'display_order', 'name')

        # Pagination
        paginator = Paginator(queryset, SERVICES_PER_PAGE)
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Query string for preserving filters across pagination links
        query_dict = request.GET.copy()
        if 'page' in query_dict:
            del query_dict['page']
        pagination_querystring = query_dict.urlencode()

        # Load active filter options from database
        active_customer_needs = CustomerNeed.objects.filter(is_active=True).order_by('name')
        active_body_parts = BodyPart.objects.filter(is_active=True).order_by('name')
        active_service_types = ServiceType.objects.filter(is_active=True).order_by('name')
        active_intended_uses = IntendedUse.objects.filter(is_active=True).order_by('name')
        active_categories = Category.objects.filter(is_active=True).order_by('display_order', 'name')

        # Active filter chips for display and easy removal
        active_chips = []
        if search_query:
            active_chips.append({'label': f'"{search_query}"', 'type': 'q', 'val': search_query})

        need_name_map = {n.slug: n.name for n in active_customer_needs}
        for n in selected_needs:
            active_chips.append({'label': need_name_map.get(n, n), 'type': 'need', 'val': n})

        body_name_map = {b.slug: b.name for b in active_body_parts}
        for b in selected_body_parts:
            active_chips.append({'label': body_name_map.get(b, b), 'type': 'body', 'val': b})

        type_name_map = {t.slug: t.name for t in active_service_types}
        for t in selected_service_types:
            active_chips.append({'label': type_name_map.get(t, t), 'type': 'type', 'val': t})

        usage_name_map = {u.slug: u.name for u in active_intended_uses}
        for u in selected_intended_uses:
            active_chips.append({'label': usage_name_map.get(u, u), 'type': 'usage', 'val': u})

        if selected_category:
            active_chips.append({'label': f'Category: {selected_category}', 'type': 'category', 'val': selected_category})

        context = {
            'page_obj': page_obj,
            'services': page_obj.object_list,
            'total_results': paginator.count,
            'search_query': search_query,
            'selected_needs': selected_needs,
            'selected_body_parts': selected_body_parts,
            'selected_service_types': selected_service_types,
            'selected_intended_uses': selected_intended_uses,
            'selected_category': selected_category,
            'sort_by': sort_by,
            'pagination_querystring': pagination_querystring,
            'active_customer_needs': active_customer_needs,
            'active_body_parts': active_body_parts,
            'active_service_types': active_service_types,
            'active_intended_uses': active_intended_uses,
            'active_categories': active_categories,
            'active_chips': active_chips,
            'has_active_filters': bool(
                search_query or selected_needs or selected_body_parts or
                selected_service_types or selected_intended_uses or selected_category
            ),
        }
        return render(request, 'services.html', context)
    except Exception:
        logger.exception("Error occurred while filtering services catalogue")
        return render(request, 'services.html', {
            'page_obj': None,
            'services': [],
            'total_results': 0,
            'search_query': '',
            'active_customer_needs': [],
            'active_body_parts': [],
            'active_service_types': [],
            'active_intended_uses': [],
            'active_chips': [],
            'has_active_filters': False,
            'error_message': 'An unexpected error occurred while loading services. Please try again.',
        })


def service_detail(request):
    """
    Renders service detail page with dynamic database lookup by slug or id.
    """
    service_id = request.GET.get('id', '').strip()
    service_slug = request.GET.get('slug', '').strip()

    service = None
    if service_slug:
        service = Service.objects.filter(slug=service_slug, is_active=True).select_related('category').first()
    elif service_id and service_id.isdigit():
        service = Service.objects.filter(id=service_id, is_active=True).select_related('category').first()

    if not service:
        service = Service.objects.filter(is_active=True).select_related('category').first()

    return render(request, 'service-detail.html', {'service': service})


def appointment(request):
    return render(request, 'appointment.html')

def blog(request):
    return render(request, 'blog.html')

def blog_detail(request):
    return render(request, 'blog-detail.html')

def bmi_calculator(request):
    return render(request, 'bmi-calculator.html')

def certificates(request):
    return render(request, 'certificates.html')

def contact(request):
    return render(request, 'contact.html')

def digital_profile(request):
    return render(request, 'digital-profile.html')

def enquiry(request):
    return render(request, 'enquiry.html')

def faq(request):
    return render(request, 'faq.html')

def gallery(request):
    return render(request, 'gallery.html')

def offers(request):
    return render(request, 'offers.html')

def support(request):
    return render(request, 'support.html')

def testimonials(request):
    return render(request, 'testimonials.html')
