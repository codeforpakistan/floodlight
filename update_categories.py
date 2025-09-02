#!/usr/bin/env python
"""
Script to update category types for existing categories
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'floodlight.settings')
django.setup()

from app.models import Category

# Define category mappings
PROBLEM_CATEGORIES = [
    'Damaged Infrastructure',
    'Damaged Roads / Railways', 
    'Destroyed Buildings',
    'Disease Outbreaks/Medical Cases',
    'Flooded Areas',
    'Flooded/Affected Areas',
    'Relief Needed'
]

SERVICE_CATEGORIES = [
    'Food Distribution',
    'Fundraisers / Charities',
    'Kitchens', 
    'Medical Camps',
    'Relief Camps',
    'Relief Camps / Shelters',
    'Relief Collection Points',
    'Schools for Flood Affected',
    'Water Filtration Plant'
]

INFORMATION_CATEGORIES = [
    'Govt. Data on the Water Flow',
    'Water Flow Data'
]

def update_categories():
    """Update category types for existing categories"""
    
    # Update problem categories
    for cat_name in PROBLEM_CATEGORIES:
        try:
            category = Category.objects.get(name=cat_name)
            category.category_type = 'problem'
            category.save()
            print(f"✓ Updated '{cat_name}' as PROBLEM")
        except Category.DoesNotExist:
            print(f"✗ Category '{cat_name}' not found")
    
    # Update service categories  
    for cat_name in SERVICE_CATEGORIES:
        try:
            category = Category.objects.get(name=cat_name)
            category.category_type = 'service'
            category.save()
            print(f"✓ Updated '{cat_name}' as SERVICE")
        except Category.DoesNotExist:
            print(f"✗ Category '{cat_name}' not found")
    
    # Update information categories
    for cat_name in INFORMATION_CATEGORIES:
        try:
            category = Category.objects.get(name=cat_name)
            category.category_type = 'information'
            category.save()
            print(f"✓ Updated '{cat_name}' as INFORMATION")
        except Category.DoesNotExist:
            print(f"✗ Category '{cat_name}' not found")
    
    # Show summary
    print(f"\n=== SUMMARY ===")
    for cat_type, display_name in Category.CATEGORY_TYPES:
        count = Category.objects.filter(category_type=cat_type).count()
        print(f"{display_name}: {count} categories")
    
    # Show categorized list
    print(f"\n=== PROBLEMS ===")
    for cat in Category.objects.filter(category_type='problem'):
        print(f"- {cat.name}")
    
    print(f"\n=== SERVICES ===") 
    for cat in Category.objects.filter(category_type='service'):
        print(f"- {cat.name}")
        
    print(f"\n=== INFORMATION ===")
    for cat in Category.objects.filter(category_type='information'):
        print(f"- {cat.name}")

if __name__ == '__main__':
    update_categories()
