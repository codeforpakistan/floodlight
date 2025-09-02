# Floodlight

Floodlight is a crowd-sourcing platform for disaster response, hosted on the floods.pk domain. Inspired by Ushahidi, it is designed to coordinate relief efforts during disasters by tracking needs, resources, and fulfillment activities. The platform supports transparent reporting, matching, and monitoring of relief actions for each disaster event.

## Architecture Overview
- Django-based web application
- Modular app structure (main project: `floodlight/`, apps: e.g., `core/`)
- Database: SQLite for development, PostgreSQL for production
- RESTful API endpoints for reporting, searching, and fulfilling needs
- Role-based access for admins, volunteers, organizations, and the public
- Data flows: Needs and resources are reported, matched, and tracked through the system

## Core Workflows
1. **Disaster Tracking:** Each disaster is registered and tracked as a unique event.
2. **Needs Reporting:** Users can report specific needs (e.g., shelter, medical aid, food) for each disaster.
3. **Resource Matching:** Volunteers, organizations, or donors can offer resources to fulfill reported needs.
4. **Fulfillment Logging:** All actions to fulfill needs are logged, creating a transparent history.
5. **Status Updates:** Needs and resources are updated as they are fulfilled or change over time.
6. **Data Visualization:** Map and dashboard views show locations of needs, resources, and relief activities.


## Purpose
Floodlight aims to coordinate relief efforts by connecting affected communities, volunteers, organizations, and donors. It tracks each disaster, the needs reported, and the fulfillment status, supporting rapid and organized response.

## Key Features
- Track individual disasters and their specific needs
- Allow users to report needs and others to fulfill them
- Maintain a transparent log of all relief activities
- Customizable categories for needs and resources

- Map-based reporting and visualization
- Role-based permissions and workflows
- Integration with external data sources (e.g., government water flow data)


## Initial Disaster/Needs Categories
Floodlight will support tracking and reporting for the following categories (based on https://pak-flood.ushahidi.io/map):

- Relief Camps / Shelters
    - Lat, Lng, Name, Contact Persons, Capcity, Pictures
- Relief Needed
    - Shelter, type of relief needed including water, medicines, medical kits, medical supplies, tents, food, transportation, clothes, money, rations, mosquito nets, boats, kitchenware, gas cylinders, blankets, lamps, fans, hygiene kits, sanitizers, birthing kits, doctors, tarpaulins, other, pictures
- Flooded/Affected Areas
    - Location, address, picture, affected households, notes, focal person
- Relief Collection Points
    - Location, contact person, address, city
- Fundraisers / Charities
    - Name of orgnization or person, locations covered, items needed (from the list above), contact person, account details, urls if any, photos, 
- Govt. Data on the Water Flow
    - location, disharge in cusecs, timestamp
- Medical Camps
    - organization, contact person, city, address, location, doctors with specialization, photos, start date, end date, status (active or not)
- Damaged Roads / Railways
    - name of highway or track, location, cureent status, location, 
- Disease Outbreaks / Medical Cases
    - name of disease, address, location, photos, risk of spreading (low/high)
- Kitchens
    - organization, city, address, location, contact person, photo, start time, end time, contact person
- Destroyed Buildings
    - Name, location, type (house, school, ofgfice, shoip, hospital, resturant)
- Schools for Flood Affected    
    - school name, address, location, contact person, timings, photo
- Water Filtration Plant
    - address, lcoation, photo

## Data Models

Floodlight uses a comprehensive set of Django models to support disaster response coordination:

### Core Models

**`Disaster`** - Represents disaster events
- Tracks disaster name, description, start/end dates
- Uses slug for URL-friendly references
- Links to creating user for accountability

**`Category`** - Types of needs (Relief Camps, Medical Camps, etc.)
- Predefined categories for organizing different types of relief needs
- Extensible system for adding new categories

**`Need`** - Issue tracker-style needs requiring resolution
- Core entity representing reported needs during disasters
- Status workflow: Open → In Progress → Resolved → Verified → Closed
- Priority levels: Low, Medium, High, Urgent
- Location data: coordinates, address, city
- Contact information for coordination
- Assignment system for volunteers/organizations

**`Resource`** - Relief offerings to fulfill needs
- Can be provided by individual users or organizations
- Status tracking: Offered → Confirmed → Delivered
- Quantity and availability date tracking
- Contact information for coordination

**`Organization`** - Relief organizations (NGOs, Government, etc.)
- Different organization types for categorization
- Contact details, website, address
- Verification system for credibility

### Supporting Models

**`Field`** - Extensible category-specific data
- Key-value pairs for storing category-specific information
- Field types: text, number, date, URL, email
- Examples: capacity for relief camps, discharge rate for water flow data

**`Photo`** - Visual documentation
- Multiple photos per need for evidence/documentation
- Caption and uploader tracking

**`Comment`** - Discussion and updates
- Community discussion on needs
- Status update notifications
- Chronological conversation tracking

### Quality Control Models

**`Report`** - Community moderation system
- Report types: misleading, false, spam, inappropriate, duplicate, outdated
- Anonymous and logged-in user reporting
- Moderation workflow with admin review
- Evidence tracking and action logging

**`ChangeLog`** - Audit trail
- Generic change tracking for all models
- Action types: created, updated, deleted, status_changed, assigned, resolved
- Field-level change tracking with JSON storage
- User attribution and timestamps

### Verification System

All major content models include verification features:
- `is_verified` flag for trusted content
- `verified_by` user reference
- `verified_at` timestamp
- Verification notes for context

### Community Flagging

Content can be flagged by the community:
- `flag_count` tracks number of reports
- `is_flagged` marks content under review
- Prevents misuse through duplicate prevention

This model structure supports transparent, accountable, and scalable disaster response coordination while maintaining data quality through community moderation and official verification.

## Roles & Permissions
- **Admin:** Manage disasters, categories, users, and system settings
- **Volunteer/Organization:** Report, fulfill, and update needs/resources
- **Public:** View map, report needs, track fulfillment


## Next Steps
Detailed specifications for each need and workflow will be defined as the project evolves. For now, the above categories serve as the foundation for data modeling and feature development.

---

For architecture, developer workflows, and integration details, see `.github/copilot-instructions.md`.
