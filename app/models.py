from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Disaster(models.Model):
    """A disaster event that needs tracking and response coordination."""
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    affected_areas = models.TextField(help_text="Geographic areas affected by this disaster")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_date']


class Category(models.Model):
    """Categories for different types of needs and services"""
    CATEGORY_TYPES = [
        ('problem', 'Problem/Issue'),
        ('service', 'Service/Solution'), 
        ('information', 'Information/Data'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='problem')
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or emoji")

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_type', 'name']


class Need(models.Model):
    """An issue/need reported for a disaster that requires resolution."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('verified', 'Verified'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    ]

    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE, related_name='needs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Location fields
    location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Contact information
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    
    # User tracking
    reported_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_needs')
    
    # Verification for crowdsourced reliability
    is_verified = models.BooleanField(default=False, help_text="Has this need been verified by a trusted source")
    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='verified_needs', help_text="User who verified this need")
    verified_at = models.DateTimeField(null=True, blank=True, help_text="When this need was verified")
    verification_notes = models.TextField(blank=True, help_text="Notes from the verification process")
    
    # Community flagging
    flag_count = models.PositiveIntegerField(default=0, help_text="Number of times this need has been reported")
    is_flagged = models.BooleanField(default=False, help_text="Is this need under review due to reports")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    @property 
    def entry_type(self):
        """Returns the type based on category"""
        return self.category.category_type if self.category else 'problem'

    @property
    def is_problem(self):
        """Check if this is a problem/issue"""
        return self.entry_type == 'problem'
    
    @property 
    def is_service(self):
        """Check if this is a service/solution"""
        return self.entry_type == 'service'

    def __str__(self):
        return f"{self.category} - {self.title}"

    class Meta:
        ordering = ['-created_at']


class Problem(models.Model):
    """Specific model for problems/issues that need to be resolved"""
    need = models.OneToOneField(Need, on_delete=models.CASCADE, related_name='problem_details')
    
    # Problem-specific fields
    severity = models.CharField(max_length=20, choices=[
        ('minor', 'Minor'),
        ('moderate', 'Moderate'), 
        ('major', 'Major'),
        ('critical', 'Critical'),
        ('catastrophic', 'Catastrophic')
    ], default='moderate')
    
    affected_population = models.PositiveIntegerField(null=True, blank=True, 
                                                    help_text="Estimated number of people affected")
    infrastructure_type = models.CharField(max_length=50, blank=True,
                                         help_text="Type of infrastructure affected (road, bridge, building, etc.)")
    estimated_repair_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    repair_time_estimate = models.CharField(max_length=100, blank=True,
                                          help_text="Estimated time to repair (e.g., '2 weeks', '3 months')")
    
    # Dependencies 
    blocks_access_to = models.TextField(blank=True, help_text="What areas/services this problem blocks access to")
    dependencies = models.ManyToManyField('self', blank=True, symmetrical=False,
                                        help_text="Other problems that must be solved first")

    def __str__(self):
        return f"Problem: {self.need.title}"


class Service(models.Model):
    """Specific model for services/solutions being provided"""
    need = models.OneToOneField(Need, on_delete=models.CASCADE, related_name='service_details')
    
    # Service-specific fields  
    service_type = models.CharField(max_length=50, choices=[
        ('shelter', 'Shelter/Accommodation'),
        ('food', 'Food Distribution'),
        ('medical', 'Medical Services'),
        ('education', 'Educational Services'), 
        ('water', 'Water/Sanitation'),
        ('rescue', 'Rescue Operations'),
        ('transport', 'Transportation'),
        ('communication', 'Communication'),
        ('financial', 'Financial Aid'),
        ('other', 'Other Services')
    ])
    
    capacity = models.PositiveIntegerField(null=True, blank=True,
                                         help_text="Maximum number of people that can be served")
    current_occupancy = models.PositiveIntegerField(default=0,
                                                  help_text="Current number of people being served")
    
    # Operating hours
    operating_hours = models.CharField(max_length=100, blank=True,
                                     help_text="e.g., '24/7', 'Mon-Fri 9AM-6PM'")
    start_date = models.DateField(null=True, blank=True, help_text="When service started operating")
    end_date = models.DateField(null=True, blank=True, help_text="When service will stop (if known)")
    
    # Requirements
    eligibility_criteria = models.TextField(blank=True,
                                          help_text="Who is eligible for this service")
    requirements = models.TextField(blank=True,
                                  help_text="What people need to bring/have to access service")
    
    # Provider information (extends the contact info from Need)
    provider_organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_at_capacity(self):
        """Check if service is at full capacity"""
        return self.capacity and self.current_occupancy >= self.capacity
    
    @property
    def availability_percentage(self):
        """Calculate how full the service is"""
        if not self.capacity:
            return None
        return (self.current_occupancy / self.capacity) * 100

    def __str__(self):
        return f"Service: {self.need.title}"


class Field(models.Model):
    """Extensible key-value fields for category-specific information."""
    need = models.ForeignKey(Need, on_delete=models.CASCADE, related_name='fields')
    key = models.CharField(max_length=100)
    value = models.TextField(blank=True)
    field_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('url', 'URL'),
        ('email', 'Email'),
    ], default='text')

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"

    class Meta:
        unique_together = ['need', 'key']


class Organization(models.Model):
    """Organizations that can provide relief (NGOs, Government agencies, etc.)"""
    name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=50, choices=[
        ('ngo', 'NGO'),
        ('government', 'Government Agency'),
        ('private', 'Private Company'),
        ('charity', 'Charity'),
        ('international', 'International Organization'),
        ('other', 'Other')
    ])
    description = models.TextField(blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    
    # Verification for organizational credibility
    is_verified = models.BooleanField(default=False, help_text="Has this organization been verified")
    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='verified_organizations', help_text="Admin who verified this organization")
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    """Resources offered to fulfill needs by individuals or organizations."""
    need = models.ForeignKey(Need, on_delete=models.CASCADE, related_name='resources')
    
    # Provider can be either an individual user or an organization
    provider_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, 
                                    help_text="Individual provider")
    provider_organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True,
                                            help_text="Organization provider")
    
    description = models.TextField()
    quantity = models.CharField(max_length=100, blank=True)
    availability_date = models.DateField(null=True, blank=True)
    contact_info = models.CharField(max_length=200, blank=True)
    
    # Verification for crowdsourced reliability
    is_verified = models.BooleanField(default=False, help_text="Has this resource been verified")
    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='verified_resources', help_text="User who verified this resource")
    verified_at = models.DateTimeField(null=True, blank=True, help_text="When this resource was verified")
    
    # Community flagging
    flag_count = models.PositiveIntegerField(default=0, help_text="Number of times this resource has been reported")
    is_flagged = models.BooleanField(default=False, help_text="Is this resource under review due to reports")
    
    status = models.CharField(max_length=15, choices=[
        ('offered', 'Offered'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='offered')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def provider_name(self):
        """Return the name of the provider (user or organization)"""
        if self.provider_organization:
            return self.provider_organization.name
        elif self.provider_user:
            return f"{self.provider_user.first_name} {self.provider_user.last_name}".strip() or self.provider_user.username
        return "Anonymous"

    def __str__(self):
        return f"Resource from {self.provider_name} for {self.need.title}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.provider_user and not self.provider_organization:
            raise ValidationError("Either provider_user or provider_organization must be specified")
        if self.provider_user and self.provider_organization:
            raise ValidationError("Cannot specify both provider_user and provider_organization")


class Photo(models.Model):
    """Photos attached to needs for documentation."""
    need = models.ForeignKey(Need, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='needs/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.need.title}"


class Comment(models.Model):
    """Comments/updates on needs for discussion and status updates."""
    need = models.ForeignKey(Need, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    is_status_update = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.need.title}"

    class Meta:
        ordering = ['created_at']


class Report(models.Model):
    """Community reports for misleading or false content."""
    REPORT_TYPES = [
        ('misleading', 'Misleading Information'),
        ('false', 'False/Fake Content'),
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('duplicate', 'Duplicate Entry'),
        ('outdated', 'Outdated Information'),
        ('other', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('investigating', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
        ('action_taken', 'Action Taken')
    ]
    
    # Generic relation to report any content type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Report details
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(help_text="Explain why this content is problematic")
    evidence = models.TextField(blank=True, help_text="Any additional evidence or links")
    
    # Reporter information
    reported_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    reporter_email = models.EmailField(blank=True, help_text="For anonymous reports")
    
    # Moderation
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='reviewed_reports')
    review_notes = models.TextField(blank=True)
    action_taken = models.TextField(blank=True, help_text="What action was taken based on this report")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        reporter = self.reported_by.username if self.reported_by else "Anonymous"
        return f"{self.report_type.title()} report by {reporter} on {self.content_object}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['content_type', 'object_id', 'reported_by']  # Prevent duplicate reports from same user


class ChangeLog(models.Model):
    """Generic change log for tracking modifications to any model."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=[
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('status_changed', 'Status Changed'),
        ('assigned', 'Assigned'),
        ('resolved', 'Resolved'),
    ])
    field_changes = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action.title()} {self.content_object} by {self.user}"

    class Meta:
        ordering = ['-timestamp']
