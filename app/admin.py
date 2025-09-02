from django.contrib import admin
from .models import (
    Disaster, Category, Need, Organization, Resource, 
    Field, Photo, Comment, Report, ChangeLog, Problem, Service
)


@admin.register(Disaster)
class DisasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity', 'start_date', 'end_date', 'created_by', 'created_at']
    list_filter = ['severity', 'start_date', 'created_at']
    search_fields = ['name', 'description', 'affected_areas']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        ('Impact & Severity', {
            'fields': ('severity', 'affected_areas')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Metadata', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        })
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'description']
    list_filter = ['category_type']
    search_fields = ['name', 'description']
    ordering = ['category_type', 'name']


@admin.register(Need)
class NeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'disaster', 'category', 'entry_type', 'status', 'priority', 'is_verified', 'created_at']
    list_filter = ['status', 'priority', 'category__category_type', 'category', 'is_verified', 'is_flagged', 'created_at']
    search_fields = ['title', 'description', 'location']
    raw_id_fields = ['reported_by', 'assigned_to', 'verified_by']
    readonly_fields = ['flag_count']
    
    def entry_type(self, obj):
        return obj.entry_type.title() if obj.category else 'Unknown'
    entry_type.short_description = 'Type'


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization_type', 'is_verified', 'created_at']
    list_filter = ['organization_type', 'is_verified']
    search_fields = ['name', 'description']
    raw_id_fields = ['created_by', 'verified_by']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['need', 'provider_name', 'status', 'is_verified', 'created_at']
    list_filter = ['status', 'is_verified', 'is_flagged']
    search_fields = ['description']
    raw_id_fields = ['provider_user', 'provider_organization', 'verified_by']
    readonly_fields = ['flag_count']


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['need', 'key', 'value', 'field_type']
    list_filter = ['field_type']
    search_fields = ['key', 'value']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['need', 'caption', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_at']
    raw_id_fields = ['uploaded_by']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['need', 'user', 'is_status_update', 'created_at']
    list_filter = ['is_status_update', 'created_at']
    search_fields = ['text']
    raw_id_fields = ['user']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'report_type', 'status', 'reported_by', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['description']
    raw_id_fields = ['reported_by', 'reviewed_by']


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'action', 'user', 'timestamp']
    list_filter = ['action', 'timestamp']
    raw_id_fields = ['user']
    readonly_fields = ['content_type', 'object_id', 'field_changes']


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['need', 'severity', 'affected_population', 'infrastructure_type']
    list_filter = ['severity', 'infrastructure_type']
    search_fields = ['need__title', 'infrastructure_type', 'blocks_access_to']
    raw_id_fields = ['need']
    filter_horizontal = ['dependencies']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['need', 'service_type', 'capacity', 'current_occupancy', 'availability_percentage', 'provider_organization']
    list_filter = ['service_type', 'provider_organization']
    search_fields = ['need__title', 'eligibility_criteria', 'requirements']
    raw_id_fields = ['need', 'provider_organization']
    readonly_fields = ['availability_percentage']
    
    def availability_percentage(self, obj):
        percentage = obj.availability_percentage
        if percentage is None:
            return 'N/A'
        return f'{percentage:.1f}%'
    availability_percentage.short_description = 'Capacity Used'
