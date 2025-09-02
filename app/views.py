from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Need, Resource, Category, Disaster, Field
import json


def home(request):
    """Homepage with overview of recent problems and services"""
    # Recent problems (things that need fixing)
    recent_problems = Need.objects.filter(
        status='open', 
        category__category_type='problem'
    ).select_related('category', 'disaster').order_by('-created_at')[:4]
    
    # Recent services (solutions being offered)  
    recent_services = Need.objects.filter(
        status='open',
        category__category_type='service'
    ).select_related('category', 'disaster').order_by('-created_at')[:4]
    
    recent_resources = Resource.objects.filter(status='offered').select_related('need__category').order_by('-created_at')[:6]
    active_disasters = Disaster.objects.filter(end_date__isnull=True).order_by('-start_date')[:3]
    
    context = {
        'recent_problems': recent_problems,
        'recent_services': recent_services, 
        'recent_resources': recent_resources,
        'active_disasters': active_disasters,
        'total_problems': Need.objects.filter(status='open', category__category_type='problem').count(),
        'total_services': Need.objects.filter(status='open', category__category_type='service').count(),
        'total_resources': Resource.objects.filter(status='offered').count(),
    }
    return render(request, 'app/home.html', context)


def needs_list(request):
    """List all needs with filtering by type (problems/services) and other criteria"""
    needs = Need.objects.filter(status='open').select_related('category', 'disaster', 'reported_by')
    
    # Filter by entry type (problems, services, information)
    entry_type = request.GET.get('type', 'all')
    if entry_type in ['problem', 'service', 'information']:
        needs = needs.filter(category__category_type=entry_type)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        needs = needs.filter(category_id=category_id)
    
    # Filter by disaster
    disaster_id = request.GET.get('disaster')
    if disaster_id:
        needs = needs.filter(disaster_id=disaster_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        needs = needs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(needs.order_by('-created_at'), 12)
    page_number = request.GET.get('page')
    needs_page = paginator.get_page(page_number)
    
    # Get categories filtered by type for the dropdown
    if entry_type in ['problem', 'service', 'information']:
        categories = Category.objects.filter(category_type=entry_type)
    else:
        categories = Category.objects.all()
    
    context = {
        'needs': needs_page,
        'categories': categories,
        'disasters': Disaster.objects.filter(end_date__isnull=True),
        'current_category': category_id,
        'current_disaster': disaster_id,
        'current_type': entry_type,
        'search_query': search_query,
        'problem_count': Need.objects.filter(status='open', category__category_type='problem').count(),
        'service_count': Need.objects.filter(status='open', category__category_type='service').count(),
        'info_count': Need.objects.filter(status='open', category__category_type='information').count(),
    }
    return render(request, 'app/needs_list.html', context)


def need_detail(request, need_id):
    """Detailed view of a specific need"""
    need = get_object_or_404(Need.objects.select_related('category', 'disaster', 'reported_by', 'verified_by'), id=need_id)
    info_fields = Field.objects.filter(need=need)
    
    context = {
        'need': need,
        'info_fields': info_fields,
    }
    return render(request, 'app/need_detail.html', context)


def resources_list(request):
    """List all available resources with filtering"""
    resources = Resource.objects.filter(status='offered').select_related('need__category', 'provider_user', 'provider_organization')
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        resources = resources.filter(need__category_id=category_id)
    
    # Filter by resource type
    resource_type = request.GET.get('type')
    if resource_type in ['individual', 'organization']:
        if resource_type == 'individual':
            resources = resources.filter(provider_user__isnull=False)
        else:
            resources = resources.filter(provider_organization__isnull=False)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        resources = resources.filter(
            Q(description__icontains=search_query) |
            Q(need__title__icontains=search_query) |
            Q(need__location__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(resources.order_by('-created_at'), 12)
    page_number = request.GET.get('page')
    resources_page = paginator.get_page(page_number)
    
    context = {
        'resources': resources_page,
        'categories': Category.objects.all(),
        'current_category': category_id,
        'resource_type': resource_type,
        'search_query': search_query,
    }
    return render(request, 'app/resources_list.html', context)


def resource_detail(request, resource_id):
    """Detailed view of a specific resource"""
    resource = get_object_or_404(
        Resource.objects.select_related('need__category', 'provider_user', 'provider_organization'),
        id=resource_id
    )
    
    context = {
        'resource': resource,
    }
    return render(request, 'app/resource_detail.html', context)


def disasters_list(request):
    """List all disasters"""
    disasters = Disaster.objects.all().order_by('-start_date')
    
    context = {
        'disasters': disasters,
    }
    return render(request, 'app/disasters_list.html', context)


def disaster_detail(request, disaster_slug):
    """Detailed view of a specific disaster with related needs and resources"""
    disaster = get_object_or_404(Disaster, slug=disaster_slug)
    
    # Separate problems and services
    problems = Need.objects.filter(
        disaster=disaster, 
        category__category_type='problem'
    ).select_related('category')[:10]
    
    services = Need.objects.filter(
        disaster=disaster,
        category__category_type='service' 
    ).select_related('category')[:10]
    
    context = {
        'disaster': disaster,
        'problems': problems,
        'services': services,
        'problems_count': Need.objects.filter(disaster=disaster, category__category_type='problem').count(),
        'services_count': Need.objects.filter(disaster=disaster, category__category_type='service').count(),
        'total_needs': Need.objects.filter(disaster=disaster).count(),
    }
    return render(request, 'app/disaster_detail.html', context)


def problems_list(request):
    """List all problems/issues that need resolution"""
    problems = Need.objects.filter(
        status='open',
        category__category_type='problem'
    ).select_related('category', 'disaster', 'reported_by')
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        problems = problems.filter(category_id=category_id)
    
    # Filter by disaster
    disaster_id = request.GET.get('disaster')
    if disaster_id:
        problems = problems.filter(disaster_id=disaster_id)
    
    # Filter by priority
    priority = request.GET.get('priority')
    if priority:
        problems = problems.filter(priority=priority)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        problems = problems.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(problems.order_by('-priority', '-created_at'), 12)
    page_number = request.GET.get('page')
    problems_page = paginator.get_page(page_number)
    
    context = {
        'problems': problems_page,
        'categories': Category.objects.filter(category_type='problem'),
        'disasters': Disaster.objects.filter(end_date__isnull=True),
        'current_category': category_id,
        'current_disaster': disaster_id,
        'current_priority': priority,
        'search_query': search_query,
        'priority_choices': Need._meta.get_field('priority').choices,
    }
    return render(request, 'app/problems_list.html', context)


def services_list(request):
    """List all services/solutions being provided"""
    services = Need.objects.filter(
        status='open',
        category__category_type='service'
    ).select_related('category', 'disaster', 'reported_by')
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        services = services.filter(category_id=category_id)
    
    # Filter by disaster
    disaster_id = request.GET.get('disaster')
    if disaster_id:
        services = services.filter(disaster_id=disaster_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        services = services.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Pagination  
    paginator = Paginator(services.order_by('-created_at'), 12)
    page_number = request.GET.get('page')
    services_page = paginator.get_page(page_number)
    
    context = {
        'services': services_page,
        'categories': Category.objects.filter(category_type='service'),
        'disasters': Disaster.objects.filter(end_date__isnull=True),
        'current_category': category_id,
        'current_disaster': disaster_id,
        'search_query': search_query,
    }
    return render(request, 'app/services_list.html', context)


def map_view(request):
    """Interactive map showing all problems and services"""
    # Get all needs with coordinates
    needs = Need.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    ).select_related('category', 'disaster')
    
    # Filter by type if specified
    entry_type = request.GET.get('type', 'all')
    if entry_type in ['problem', 'service', 'information']:
        needs = needs.filter(category__category_type=entry_type)
    
    # Filter by disaster if specified
    disaster_id = request.GET.get('disaster')
    if disaster_id:
        needs = needs.filter(disaster_id=disaster_id)
    
    context = {
        'needs': needs,
        'disasters': Disaster.objects.filter(end_date__isnull=True),
        'current_type': entry_type,
        'current_disaster': disaster_id,
        'problem_count': Need.objects.filter(
            category__category_type='problem',
            latitude__isnull=False, 
            longitude__isnull=False
        ).count(),
        'service_count': Need.objects.filter(
            category__category_type='service',
            latitude__isnull=False, 
            longitude__isnull=False
        ).count(),
    }
    return render(request, 'app/map_view.html', context)


def map_data_api(request):
    """API endpoint to get map data as JSON"""
    # Get all needs with coordinates
    needs = Need.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    ).select_related('category', 'disaster')
    
    # Filter by type if specified
    entry_type = request.GET.get('type', 'all')
    if entry_type in ['problem', 'service', 'information']:
        needs = needs.filter(category__category_type=entry_type)
    
    # Filter by disaster if specified
    disaster_id = request.GET.get('disaster')
    if disaster_id:
        needs = needs.filter(disaster_id=disaster_id)
    
    # Convert to GeoJSON format
    features = []
    for need in needs:
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(need.longitude), float(need.latitude)]
            },
            'properties': {
                'id': need.id,
                'title': need.title,
                'description': need.description[:200] + '...' if len(need.description) > 200 else need.description,
                'category': need.category.name if need.category else 'Unknown',
                'category_type': need.category.category_type if need.category else 'unknown',
                'disaster': need.disaster.name,
                'location': need.location,
                'city': need.city,
                'status': need.status,
                'priority': need.priority,
                'is_verified': need.is_verified,
                'contact_person': need.contact_person,
                'contact_phone': need.contact_phone,
                'created_at': need.created_at.isoformat(),
                'url': f'/needs/{need.id}/'
            }
        }
        features.append(feature)
    
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    return JsonResponse(geojson)
