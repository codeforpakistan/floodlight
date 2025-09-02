from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Disaster, Category, Need, Organization, Resource, Field, Comment
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Seed the database with sample disaster response data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        # Create test users
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'user{i+1}',
                defaults={
                    'email': f'user{i+1}@example.com',
                    'first_name': f'User{i+1}',
                    'last_name': 'Test'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        
        # Create categories
        categories_data = [
            ('Relief Camps / Shelters', 'Temporary shelters and accommodation facilities'),
            ('Relief Needed', 'General relief requirements including water, medicines, food, etc.'),
            ('Flooded/Affected Areas', 'Areas affected by flooding requiring assessment'),
            ('Relief Collection Points', 'Locations for collecting and distributing relief materials'),
            ('Fundraisers / Charities', 'Organizations and individuals raising funds for relief'),
            ('Govt. Data on the Water Flow', 'Government water level and discharge monitoring'),
            ('Medical Camps', 'Healthcare facilities and medical assistance points'),
            ('Damaged Roads / Railways', 'Transportation infrastructure damage reports'),
            ('Disease Outbreaks/Medical Cases', 'Public health concerns and medical emergencies'),
            ('Kitchens', 'Community kitchens and food preparation facilities'),
            ('Destroyed Buildings', 'Structural damage assessment and reporting'),
            ('Schools for Flood Affected', 'Educational facilities for displaced children'),
            ('Water Filtration Plant', 'Water treatment and purification facilities'),
        ]
        
        categories = []
        for name, desc in categories_data:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            categories.append(category)
        
        # Create disasters
        disasters = []
        disaster_data = [
            ('Pakistan Floods 2024', 'pakistan-floods-2024', 'Severe flooding across Pakistan', date.today() - timedelta(days=30)),
            ('Karachi Urban Flooding', 'karachi-floods-2024', 'Urban flooding in Karachi metropolitan area', date.today() - timedelta(days=15)),
        ]
        
        for name, slug, desc, start_date in disaster_data:
            disaster, created = Disaster.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': desc,
                    'start_date': start_date,
                    'created_by': users[0]
                }
            )
            disasters.append(disaster)
        
        # Create organizations
        org_data = [
            ('Pakistan Red Crescent', 'ngo', 'National humanitarian organization'),
            ('Edhi Foundation', 'charity', 'Charitable organization providing relief'),
            ('Al-Khidmat Foundation', 'charity', 'Islamic welfare organization'),
            ('PDMA Punjab', 'government', 'Provincial Disaster Management Authority'),
        ]
        
        organizations = []
        for name, org_type, desc in org_data:
            org, created = Organization.objects.get_or_create(
                name=name,
                defaults={
                    'organization_type': org_type,
                    'description': desc,
                    'contact_person': 'Contact Person',
                    'phone': '+92-300-1234567',
                    'email': f'contact@{name.lower().replace(" ", "")}.org',
                    'created_by': users[0],
                    'is_verified': True,
                    'verified_by': users[0]
                }
            )
            organizations.append(org)
        
        # Create needs
        needs_data = [
            ('Emergency Shelter Needed in Thatta', 'Urgent shelter required for 200 families displaced by flooding', 'Relief Camps / Shelters', 'high', 24.7461, 67.9214, 'Thatta, Sindh'),
            ('Medical Camp Required in Jacobabad', 'Medical assistance needed for flood victims', 'Medical Camps', 'urgent', 28.2820, 68.4375, 'Jacobabad, Sindh'),
            ('Food and Medicine Distribution - Sukkur', 'Food packages, clean water, and basic medicines needed', 'Relief Needed', 'medium', 27.7052, 68.8574, 'Sukkur, Sindh'),
            ('Flooded Village Assessment - Badin', 'Village completely submerged, 150 households affected', 'Flooded/Affected Areas', 'high', 24.6550, 68.8378, 'Badin, Sindh'),
            ('Relief Collection Point Setup', 'Need volunteers to organize relief collection center', 'Relief Collection Points', 'medium', 25.3960, 68.3578, 'Hyderabad'),
            ('Emergency Fund Drive - Karachi Floods', 'Fundraising for immediate flood relief operations', 'Fundraisers / Charities', 'high', 24.8607, 67.0011, 'Karachi'),
            ('Water Level Monitoring - Kotri Barrage', 'Current water discharge monitoring and early warning', 'Govt. Data on the Water Flow', 'medium', 25.3728, 68.3081, 'Kotri Barrage'),
            ('Damaged Highway N5 - Traffic Disrupted', 'Major highway damaged between Hyderabad and Karachi', 'Damaged Roads / Railways', 'urgent', 25.3960, 68.3578, 'N5 Highway'),
            ('Cholera Outbreak Alert - Sanghar', 'Multiple cases reported, immediate medical intervention needed', 'Disease Outbreaks/Medical Cases', 'urgent', 26.0500, 68.9500, 'Sanghar, Sindh'),
            ('Community Kitchen - Larkana', 'Serving hot meals to 500 families daily', 'Kitchens', 'medium', 27.5590, 68.2120, 'Larkana, Sindh'),
            ('School Building Collapsed - Mirpurkhas', 'Primary school building destroyed, 300 students affected', 'Destroyed Buildings', 'high', 25.5266, 69.0142, 'Mirpurkhas'),
            ('Temporary School for Displaced Children', 'Educational facility needed for flood-affected children', 'Schools for Flood Affected', 'medium', 26.2442, 68.3708, 'Nawabshah'),
            ('Water Purification Plant Damaged', 'Main water treatment facility needs immediate repair', 'Water Filtration Plant', 'urgent', 25.3968, 68.3731, 'Hyderabad'),
        ]
        
        needs = []
        for i, (title, desc, cat_name, priority, lat, lng, location) in enumerate(needs_data):
            category = next((c for c in categories if c.name == cat_name), categories[0])
            need, created = Need.objects.get_or_create(
                title=title,
                disaster=disasters[0],
                defaults={
                    'category': category,
                    'description': desc,
                    'location': location,
                    'latitude': lat,
                    'longitude': lng,
                    'priority': priority,
                    'status': 'open' if i % 3 != 0 else 'resolved',
                    'reported_by': users[i % len(users)],
                    'contact_person': f'Local Coordinator {i+1}',
                    'contact_phone': f'+92-300-{1000000 + i}',
                    'is_verified': i % 2 == 0,
                    'verified_by': users[0] if i % 2 == 0 else None
                }
            )
            needs.append(need)
        
        # Add specific info fields for different categories
        for need in needs:
            if need.category.name == 'Relief Camps / Shelters':
                Field.objects.get_or_create(
                    need=need,
                    key='capacity',
                    defaults={'value': '200 families', 'field_type': 'text'}
                )
                Field.objects.get_or_create(
                    need=need,
                    key='contact_persons',
                    defaults={'value': 'Local Coordinator, Camp Manager', 'field_type': 'text'}
                )
            elif need.category.name == 'Medical Camps':
                Field.objects.get_or_create(
                    need=need,
                    key='specializations',
                    defaults={'value': 'General Medicine, Pediatrics, Emergency Care', 'field_type': 'text'}
                )
                Field.objects.get_or_create(
                    need=need,
                    key='doctors_available',
                    defaults={'value': '3 doctors, 5 nurses', 'field_type': 'text'}
                )
            elif need.category.name == 'Govt. Data on the Water Flow':
                Field.objects.get_or_create(
                    need=need,
                    key='discharge_cusecs',
                    defaults={'value': '850000', 'field_type': 'number'}
                )
                Field.objects.get_or_create(
                    need=need,
                    key='timestamp',
                    defaults={'value': '2024-09-02 15:30:00', 'field_type': 'text'}
                )
            elif need.category.name == 'Flooded/Affected Areas':
                Field.objects.get_or_create(
                    need=need,
                    key='affected_households',
                    defaults={'value': '150', 'field_type': 'number'}
                )
                Field.objects.get_or_create(
                    need=need,
                    key='focal_person',
                    defaults={'value': 'Village Head - Muhammad Ali', 'field_type': 'text'}
                )
            elif need.category.name == 'Fundraisers / Charities':
                Field.objects.get_or_create(
                    need=need,
                    key='account_details',
                    defaults={'value': 'Account: 1234567890, Bank: HBL', 'field_type': 'text'}
                )
                Field.objects.get_or_create(
                    need=need,
                    key='target_amount',
                    defaults={'value': '500000 PKR', 'field_type': 'text'}
                )
            elif need.category.name == 'Disease Outbreaks/Medical Cases':
                Field.objects.get_or_create(
                    need=need,
                    key='disease_name',
                    defaults={'value': 'Cholera', 'field_type': 'text'}
                )
                Field.objects.get_or_create(
                    need=need,
                    key='risk_spreading',
                    defaults={'value': 'High', 'field_type': 'text'}
                )
            elif need.category.name == 'Destroyed Buildings':
                Field.objects.get_or_create(
                    need=need,
                    key='building_type',
                    defaults={'value': 'School', 'field_type': 'text'}
                )
                Field.objects.get_or_create(
                    need=need,
                    key='damage_extent',
                    defaults={'value': 'Complete collapse', 'field_type': 'text'}
                )
        
        # Create resources
        resource_data = [
            ('Tents and Blankets Available', '100 tents and 500 blankets ready for distribution', '100 units'),
            ('Medical Supplies Donation', 'First aid kits, medicines, and medical equipment', '50 kits'),
            ('Food Packages Ready', 'Cooked meals and dry rations for families', '500 packages'),
            ('Transport Vehicles', 'Trucks available for relief material transport', '5 vehicles'),
        ]
        
        for i, (desc, details, quantity) in enumerate(resource_data):
            if i < len(needs):
                Resource.objects.get_or_create(
                    need=needs[i],
                    description=desc,
                    defaults={
                        'provider_organization': organizations[i % len(organizations)] if i % 2 == 0 else None,
                        'provider_user': users[i % len(users)] if i % 2 == 1 else None,
                        'quantity': quantity,
                        'contact_info': f'Contact: +92-300-{2000000 + i}',
                        'status': 'offered' if i % 3 != 0 else 'delivered',
                        'is_verified': i % 2 == 0,
                        'verified_by': users[0] if i % 2 == 0 else None
                    }
                )
        
        # Create comments
        comment_data = [
            'Situation assessment completed. Immediate action required.',
            'Local authorities have been notified.',
            'Relief materials are being prepared for dispatch.',
            'Weather conditions are improving, access roads clearing.',
            'Additional volunteers needed for distribution.',
        ]
        
        for i, text in enumerate(comment_data):
            if i < len(needs):
                Comment.objects.get_or_create(
                    need=needs[i],
                    text=text,
                    defaults={
                        'user': users[i % len(users)],
                        'is_status_update': i % 2 == 0
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded data:'))
        self.stdout.write(f'- {len(users)} users')
        self.stdout.write(f'- {len(categories)} categories')
        self.stdout.write(f'- {len(disasters)} disasters')
        self.stdout.write(f'- {len(organizations)} organizations')
        self.stdout.write(f'- {len(needs)} needs')
        self.stdout.write(f'- {Resource.objects.count()} resources')
        self.stdout.write(f'- {Field.objects.count()} info fields')
        self.stdout.write(f'- {Comment.objects.count()} comments')
