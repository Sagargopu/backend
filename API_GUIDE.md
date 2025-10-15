# BuildBuzz Construction Management API Guide - Complete Reference

## Table of Contents
1. [Overview](#overview)
2. [Base URL & Authentication](#base-url--authentication)
3. [Data Models & JSON Structures](#data-models--json-structures)
4. [API Endpoints by Module](#api-endpoints-by-module)
5. [Complete Endpoint Reference](#complete-endpoint-reference)
6. [Usage Examples](#usage-examples)
7. [Error Handling](#error-handling)

---

## Overview

BuildBuzz is a comprehensive construction management system API that provides functionality for managing users, projects, documents, finance, and workforce operations. The API follows RESTful principles and uses JSON for data exchange.

### System Architecture
```
Users → Projects → Components → Tasks
      → Documents
      → Finance (Transactions, Purchase Orders, etc.)
      → Workforce (Workers, Professions, Project History)
```

### Recent Updates (v3.0 - With Workforce Management)
- ✅ **Added**: Complete workforce management system
- ✅ **Enhanced**: Worker details, wages, and project tracking
- ✅ **Integrated**: Profession management and skill ratings
- ✅ **Focus**: Complete construction project lifecycle

---

## Base URL & Authentication

```
Base URL: http://localhost:8000
Production: https://your-domain.com/api
```

**Authentication**: Currently uses placeholder authentication (User ID: 1).
In production, implement JWT tokens or OAuth2.

---

## Data Models & JSON Structures

### User Management Models

#### User Entity
```json
{
  "id": 1,
  "full_name": "John Doe",
  "email": "john.doe@company.com",
  "role": "project_manager",
  "is_active": true,
  "phone_number": "+1-555-0123",
  "address": "123 Main St, City, State",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1-555-0124",
  "invitation_status": "accepted",
  "account_setup_completed": true,
  "invited_by_clerk": 2,
  "invitation_token": null,
  "invitation_sent_date": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Roles**: `clerk`, `project_manager`, `accountant`, `client`, `business_admin`

#### ClerkUserInvite (Request)
```json
{
  "email": "newuser@company.com",
  "full_name": "New User",
  "role": "project_manager",
  "invitation_message": "Welcome to BuildBuzz!"
}
```

#### AccountSetup (Request)
```json
{
  "invitation_token": "abc123def456...",
  "password": "secure_password",
  "phone_number": "+1-555-0123",
  "address": "123 Main St, City, State"
}
```

### Project Management Models

#### Project Entity
```json
{
  "id": 1,
  "name": "Downtown Office Building",
  "description": "Modern 5-story office building construction",
  "start_date": "2024-03-01",
  "end_date": "2024-12-15",
  "budget": 2500000.00,
  "status": "in_progress",
  "client_name": "ABC Corporation",
  "project_manager_id": 3,
  "project_category": "Commercial",
  "project_type": "Office Building",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Status Values**: `planned`, `in_progress`, `completed`, `on_hold`

#### ProjectComponent Entity
```json
{
  "id": 1,
  "project_id": 1,
  "name": "Foundation",
  "description": "Concrete foundation and basement construction",
  "type": "Foundation",
  "budget": 350000.00,
  "status": "completed",
  "details": {"foundation_type": "concrete", "depth": "8_feet"},
  "allocated_budget": 350000.00,
  "spent_budget": 342500.00,
  "committed_budget": 7500.00,
  "remaining_budget": 0.00,
  "budget_variance": -7500.00,
  "budget_variance_percentage": -2.14,
  "completion_percentage": 100,
  "estimated_duration_days": 45,
  "actual_duration_days": 47,
  "component_deadline": "2024-05-15",
  "component_priority": 9,
  "is_critical_path": true,
  "blocks_other_components": true,
  "parent_id": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Task Entity
```json
{
  "id": 1,
  "name": "Install Electrical Wiring",
  "description": "Install main electrical wiring for first floor",
  "status": "in_progress",
  "priority": "high",
  "component_id": 3,
  "project_id": 1,
  "task_type": "Construction",
  "estimated_hours": 40.00,
  "actual_hours": 32.50,
  "completion_percentage": 75,
  "planned_start_date": "2024-06-01",
  "planned_end_date": "2024-06-05",
  "actual_start_date": "2024-06-01",
  "actual_end_date": null,
  "deadline": "2024-06-10",
  "moved_to_backlog_date": null,
  "backlog_reason": null,
  "original_deadline": null,
  "backlog_priority": 0,
  "target_completion_date": null,
  "assigned_to": 5,
  "created_by": 3,
  "supervisor_id": 3,
  "requirements": "Install according to electrical code",
  "deliverables": "Completed wiring inspection ready",
  "acceptance_criteria": "Passes electrical inspection",
  "notes": "Material delay caused 1 day extension",
  "is_milestone": false,
  "blocks_project": false,
  "required_skills": "[\"Electrical\", \"Code Compliance\"]",
  "required_tools": "[\"Wire strippers\", \"Voltage tester\"]",
  "budget_allocation": 3200.00,
  "actual_cost": 2890.00,
  "deadline_status": "on_time",
  "days_overdue": 0,
  "escalation_level": 0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Status Values**: `To Do`, `In Progress`, `Done`, `Blocked`, `Cancelled`, `Backlog`
**Priority Values**: `Low`, `Medium`, `High`, `Critical`

### Finance Management Models

#### Transaction Entity
```json
{
  "id": 1,
  "amount": 15000.00,
  "transaction_type": "expense",
  "description": "Steel beam purchase for framework",
  "status": "approved",
  "project_id": 1,
  "vendor_id": 5,
  "purchase_order_id": 12,
  "invoice_number": "INV-2024-001",
  "transaction_date": "2024-06-15",
  "due_date": "2024-07-15",
  "payment_date": "2024-06-20",
  "created_by": 3,
  "approved_by": 7,
  "category_id": 2,
  "tax_amount": 1200.00,
  "notes": "Urgent delivery for critical path",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Vendor Entity
```json
{
  "id": 1,
  "name": "Steel Solutions Inc",
  "contact_person": "Mike Johnson",
  "email": "mike@steelsolutions.com",
  "phone": "+1-555-0199"
}
```

#### PurchaseOrder Entity
```json
{
  "id": 1,
  "description": "Steel beams for main framework",
  "vendor_id": 1,
  "project_id": 1,
  "amount": 15000.00,
  "status": "approved",
  "created_by_id": 3,
  "approved_by_id": 7,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### ChangeOrder Entity
```json
{
  "id": 1,
  "description": "Add reinforced steel support beams",
  "project_id": 1,
  "amount_change": 25000.00,
  "justification": "Engineering requirements for seismic compliance",
  "status": "pending",
  "requested_by_id": 3,
  "approved_by_id": null,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Document Management Models

#### Document Entity
```json
{
  "id": 1,
  "name": "Blueprint_Floor_1.pdf",
  "description": "Architectural blueprint for first floor layout",
  "storage_path": "/documents/projects/1/blueprints/floor1.pdf",
  "file_type": "pdf",
  "file_size": 2048576,
  "document_type": "blueprint",
  "project_id": 1,
  "component_id": null,
  "task_id": null,
  "uploaded_by_id": 3,
  "is_public": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### DocumentAccess Entity
```json
{
  "id": 1,
  "document_id": 1,
  "user_id": 5,
  "granted_by_id": 3,
  "access_level": "view",
  "granted_at": "2024-01-15T10:30:00Z"
}
```

### Workforce Management Models

#### Profession Entity
```json
{
  "id": 1,
  "name": "Electrician",
  "description": "Licensed electrician for commercial and residential projects",
  "category": "Electrical",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Categories**: `Electrical`, `Plumbing`, `Structural`, `Finishing`, `HVAC`, `Masonry`

#### Worker Entity
```json
{
  "id": 1,
  "worker_id": "ELC001",
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+1-555-0101",
  "email": "john.smith@buildbuzz.com",
  "address": "123 Main St, Detroit, MI 48201",
  "profession_id": 1,
  "skill_rating": 8.5,
  "wage_rate": 35.50,
  "current_project_id": 1,
  "current_project_start_date": "2024-10-01",
  "current_project_end_date": "2024-12-15",
  "availability": "Assigned",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Availability Values**: `Available`, `Assigned`, `Unavailable`, `On Leave`
**Skill Rating**: Scale of 1.0 to 10.0

#### WorkerProjectHistory Entity
```json
{
  "id": 1,
  "worker_id": 1,
  "project_id": 1,
  "start_date": "2024-01-15",
  "end_date": "2024-03-30",
  "role": "Lead Electrician",
  "status": "Completed",
  "performance_rating": 4.5,
  "notes": "Excellent work on main electrical installation. Met all deadlines.",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-03-30T10:30:00Z"
}
```

**Status Values**: `Active`, `Completed`, `Terminated`
**Performance Rating**: Scale of 1.0 to 5.0

#### WorkerWithProfession Entity (Extended View)
```json
{
  "id": 1,
  "worker_id": "ELC001",
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+1-555-0101",
  "email": "john.smith@buildbuzz.com",
  "address": "123 Main St, Detroit, MI 48201",
  "profession_id": 1,
  "skill_rating": 8.5,
  "wage_rate": 35.50,
  "current_project_id": 1,
  "current_project_start_date": "2024-10-01",
  "current_project_end_date": "2024-12-15",
  "availability": "Assigned",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "profession": {
    "id": 1,
    "name": "Electrician",
    "description": "Licensed electrician for commercial and residential projects",
    "category": "Electrical",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### WorkerDetailedView Entity (Complete View with History)
```json
{
  "id": 1,
  "worker_id": "ELC001",
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+1-555-0101",
  "email": "john.smith@buildbuzz.com",
  "address": "123 Main St, Detroit, MI 48201",
  "profession_id": 1,
  "skill_rating": 8.5,
  "wage_rate": 35.50,
  "current_project_id": 1,
  "current_project_start_date": "2024-10-01",
  "current_project_end_date": "2024-12-15",
  "availability": "Assigned",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "profession": {
    "id": 1,
    "name": "Electrician",
    "description": "Licensed electrician for commercial and residential projects",
    "category": "Electrical",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "project_history": [
    {
      "id": 1,
      "worker_id": 1,
      "project_id": 1,
      "start_date": "2024-01-15",
      "end_date": "2024-03-30",
      "role": "Lead Electrician",
      "status": "Completed",
      "performance_rating": 4.5,
      "notes": "Excellent work on main electrical installation. Met all deadlines.",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-03-30T10:30:00Z"
    },
    {
      "id": 2,
      "worker_id": 1,
      "project_id": 2,
      "start_date": "2024-04-01",
      "end_date": "2024-06-15",
      "role": "Senior Electrician",
      "status": "Completed",
      "performance_rating": 4.2,
      "notes": "Good performance, minor delays due to material shortage.",
      "created_at": "2024-04-01T10:30:00Z",
      "updated_at": "2024-06-15T10:30:00Z"
    },
    {
      "id": 3,
      "worker_id": 1,
      "project_id": 1,
      "start_date": "2024-10-01",
      "end_date": null,
      "role": "Lead Electrician",
      "status": "Active",
      "performance_rating": null,
      "notes": "Currently working on new office building electrical systems.",
      "created_at": "2024-10-01T10:30:00Z",
      "updated_at": "2024-10-01T10:30:00Z"
    }
  ]
}
```

### Workforce Sample Data Collections

#### Sample Professions Array
```json
[
  {
    "id": 1,
    "name": "Electrician",
    "description": "Licensed electrician for commercial and residential projects",
    "category": "Electrical",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "name": "Plumber",
    "description": "Licensed plumber for water and sewer systems",
    "category": "Plumbing",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 3,
    "name": "Carpenter",
    "description": "Skilled carpenter for framing and finishing work",
    "category": "Structural",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 4,
    "name": "Mason",
    "description": "Stone and brick mason for foundation and wall work",
    "category": "Structural",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 5,
    "name": "HVAC Technician",
    "description": "Heating, ventilation, and air conditioning specialist",
    "category": "HVAC",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Sample Workers Array (with Professions)
```json
[
  {
    "id": 1,
    "worker_id": "ELC001",
    "first_name": "John",
    "last_name": "Smith",
    "phone_number": "+1-555-0101",
    "email": "john.smith@buildbuzz.com",
    "address": "123 Main St, Detroit, MI 48201",
    "profession_id": 1,
    "skill_rating": 8.5,
    "wage_rate": 35.50,
    "current_project_id": null,
    "current_project_start_date": null,
    "current_project_end_date": null,
    "availability": "Available",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "profession": {
      "id": 1,
      "name": "Electrician",
      "description": "Licensed electrician for commercial and residential projects",
      "category": "Electrical"
    }
  },
  {
    "id": 2,
    "worker_id": "ELC002",
    "first_name": "Sarah",
    "last_name": "Johnson",
    "phone_number": "+1-555-0102",
    "email": "sarah.johnson@buildbuzz.com",
    "address": "456 Oak Ave, Detroit, MI 48202",
    "profession_id": 1,
    "skill_rating": 9.2,
    "wage_rate": 42.00,
    "current_project_id": 1,
    "current_project_start_date": "2024-10-01",
    "current_project_end_date": "2024-12-15",
    "availability": "Assigned",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-10-01T10:30:00Z",
    "profession": {
      "id": 1,
      "name": "Electrician",
      "description": "Licensed electrician for commercial and residential projects",
      "category": "Electrical"
    }
  },
  {
    "id": 3,
    "worker_id": "PLB001",
    "first_name": "Michael",
    "last_name": "Rodriguez",
    "phone_number": "+1-555-0103",
    "email": "michael.rodriguez@buildbuzz.com",
    "address": "789 Pine St, Detroit, MI 48203",
    "profession_id": 2,
    "skill_rating": 7.8,
    "wage_rate": 38.25,
    "current_project_id": null,
    "current_project_start_date": null,
    "current_project_end_date": null,
    "availability": "Available",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "profession": {
      "id": 2,
      "name": "Plumber",
      "description": "Licensed plumber for water and sewer systems",
      "category": "Plumbing"
    }
  },
  {
    "id": 4,
    "worker_id": "CAR001",
    "first_name": "David",
    "last_name": "Wilson",
    "phone_number": "+1-555-0104",
    "email": "david.wilson@buildbuzz.com",
    "address": "321 Elm St, Detroit, MI 48204",
    "profession_id": 3,
    "skill_rating": 9.0,
    "wage_rate": 33.75,
    "current_project_id": 2,
    "current_project_start_date": "2024-09-15",
    "current_project_end_date": "2024-11-30",
    "availability": "Assigned",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-09-15T10:30:00Z",
    "profession": {
      "id": 3,
      "name": "Carpenter",
      "description": "Skilled carpenter for framing and finishing work",
      "category": "Structural"
    }
  },
  {
    "id": 5,
    "worker_id": "MAS001",
    "first_name": "Robert",
    "last_name": "Garcia",
    "phone_number": "+1-555-0105",
    "email": "robert.garcia@buildbuzz.com",
    "address": "654 Maple Dr, Detroit, MI 48205",
    "profession_id": 4,
    "skill_rating": 8.0,
    "wage_rate": 36.00,
    "current_project_id": null,
    "current_project_start_date": null,
    "current_project_end_date": null,
    "availability": "On Leave",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-09-01T10:30:00Z",
    "profession": {
      "id": 4,
      "name": "Mason",
      "description": "Stone and brick mason for foundation and wall work",
      "category": "Structural"
    }
  },
  {
    "id": 6,
    "worker_id": "HVC001",
    "first_name": "Lisa",
    "last_name": "Chen",
    "phone_number": "+1-555-0106",
    "email": "lisa.chen@buildbuzz.com",
    "address": "987 Cedar Ln, Detroit, MI 48206",
    "profession_id": 5,
    "skill_rating": 8.8,
    "wage_rate": 40.50,
    "current_project_id": null,
    "current_project_start_date": null,
    "current_project_end_date": null,
    "availability": "Available",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "profession": {
      "id": 5,
      "name": "HVAC Technician",
      "description": "Heating, ventilation, and air conditioning specialist",
      "category": "HVAC"
    }
  }
]
```

#### Sample Project History Array
```json
[
  {
    "id": 1,
    "worker_id": 1,
    "project_id": 1,
    "start_date": "2024-01-15",
    "end_date": "2024-03-30",
    "role": "Lead Electrician",
    "status": "Completed",
    "performance_rating": 4.5,
    "notes": "Excellent work on main electrical installation. Met all deadlines.",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-03-30T10:30:00Z"
  },
  {
    "id": 2,
    "worker_id": 1,
    "project_id": 2,
    "start_date": "2024-04-01",
    "end_date": "2024-06-15",
    "role": "Senior Electrician",
    "status": "Completed",
    "performance_rating": 4.2,
    "notes": "Good performance, minor delays due to material shortage.",
    "created_at": "2024-04-01T10:30:00Z",
    "updated_at": "2024-06-15T10:30:00Z"
  },
  {
    "id": 3,
    "worker_id": 2,
    "project_id": 1,
    "start_date": "2024-10-01",
    "end_date": null,
    "role": "Lead Electrician",
    "status": "Active",
    "performance_rating": null,
    "notes": "Currently working on new office building electrical systems.",
    "created_at": "2024-10-01T10:30:00Z",
    "updated_at": "2024-10-01T10:30:00Z"
  },
  {
    "id": 4,
    "worker_id": 3,
    "project_id": 1,
    "start_date": "2024-02-01",
    "end_date": "2024-04-10",
    "role": "Senior Plumber",
    "status": "Completed",
    "performance_rating": 4.0,
    "notes": "Solid performance on plumbing installation.",
    "created_at": "2024-02-01T10:30:00Z",
    "updated_at": "2024-04-10T10:30:00Z"
  },
  {
    "id": 5,
    "worker_id": 4,
    "project_id": 2,
    "start_date": "2024-09-15",
    "end_date": null,
    "role": "Lead Carpenter",
    "status": "Active",
    "performance_rating": null,
    "notes": "Working on custom millwork for luxury residential project.",
    "created_at": "2024-09-15T10:30:00Z",
    "updated_at": "2024-09-15T10:30:00Z"
  },
  {
    "id": 6,
    "worker_id": 5,
    "project_id": 3,
    "start_date": "2024-03-01",
    "end_date": "2024-05-20",
    "role": "Master Mason",
    "status": "Completed",
    "performance_rating": 4.8,
    "notes": "Outstanding stonework on building facade. Ahead of schedule.",
    "created_at": "2024-03-01T10:30:00Z",
    "updated_at": "2024-05-20T10:30:00Z"
  }
]
```

### Workforce Statistics Sample Response
```json
{
  "total_workers": 6,
  "available_workers": 3,
  "assigned_workers": 2,
  "on_leave_workers": 1,
  "unavailable_workers": 0,
  "workers_by_profession": {
    "Electrician": 2,
    "Plumber": 1,
    "Carpenter": 1,
    "Mason": 1,
    "HVAC Technician": 1
  },
  "average_skill_rating": 8.55,
  "average_wage_rate": 37.50,
  "highest_skill_rating": 9.2,
  "lowest_skill_rating": 7.8,
  "active_assignments": 2,
  "completed_assignments": 4,
  "total_project_assignments": 6
}
```

---

## API Endpoints by Module

### User Management Module (`/users`)

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| `POST` | `/users/clerk/invite-user/` | Clerk invites new users | `User` |
| `POST` | `/users/setup-account/` | Complete account setup | `User` |
| `GET` | `/users/business-admin/overview/` | Business admin dashboard | `dict` |
| `GET` | `/users/business-admin/users/` | Get all users (admin only) | `List[User]` |
| `GET` | `/users/` | Get all users | `List[User]` |
| `GET` | `/users/{user_id}` | Get specific user | `User` |
| `POST` | `/users/admin/users/{user_id}/activate` | Activate user account | `User` |
| `POST` | `/users/admin/users/{user_id}/deactivate` | Deactivate user account | `User` |

### Project Management Module (`/projects`)

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| `POST` | `/projects/` | Create new project | `Project` |
| `GET` | `/projects/` | Get all projects | `List[Project]` |
| `GET` | `/projects/{project_id}` | Get specific project | `Project` |
| `PUT` | `/projects/{project_id}` | Update project | `Project` |
| `DELETE` | `/projects/{project_id}` | Delete project | `dict` |
| `POST` | `/components/` | Create project component | `ProjectComponent` |
| `GET` | `/components/` | Get all components | `List[ProjectComponent]` |
| `GET` | `/projects/{project_id}/components/` | Get project components | `List[ProjectComponent]` |
| `GET` | `/components/{component_id}` | Get specific component | `ProjectComponent` |
| `PUT` | `/components/{component_id}` | Update component | `ProjectComponent` |
| `DELETE` | `/components/{component_id}` | Delete component | `dict` |
| `POST` | `/tasks/` | Create new task | `Task` |
| `GET` | `/tasks/` | Get all tasks | `List[Task]` |
| `GET` | `/components/{component_id}/tasks/` | Get component tasks | `List[Task]` |
| `GET` | `/projects/{project_id}/tasks/` | Get all project tasks | `List[Task]` |
| `GET` | `/projects/{project_id}/tasks/by-hierarchy/` | Get hierarchical task view | `dict` |

### Finance Management Module (`/finance`)

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| `POST` | `/finance/vendors/` | Create vendor | `Vendor` |
| `GET` | `/finance/vendors/` | Get all vendors | `List[Vendor]` |
| `POST` | `/finance/purchase-orders/` | Create purchase order | `PurchaseOrder` |
| `GET` | `/finance/purchase-orders/` | Get all purchase orders | `List[PurchaseOrder]` |
| `POST` | `/finance/purchase-orders/{po_id}/approve` | Approve purchase order | `PurchaseOrder` |
| `POST` | `/finance/change-orders/` | Create change order | `ChangeOrder` |
| `GET` | `/finance/change-orders/pending/` | Get pending change orders | `List[ChangeOrder]` |
| `POST` | `/finance/change-orders/{co_id}/approve` | Approve change order | `ChangeOrder` |
| `POST` | `/finance/change-orders/{co_id}/reject` | Reject change order | `ChangeOrder` |
| `POST` | `/finance/contracts/` | Create contract | `Contract` |
| `POST` | `/finance/client-invoices/` | Create client invoice | `ClientInvoice` |
| `POST` | `/finance/vendor-invoices/` | Create vendor invoice | `VendorInvoice` |
| `POST` | `/finance/transactions/` | Create transaction | `dict` |
| `GET` | `/finance/projects/{project_id}/transactions/` | Get project transactions | `List[dict]` |

### Document Management Module (`/documents`)

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| `POST` | `/documents/upload` | Upload document | `DocumentResponse` |
| `GET` | `/documents/` | Get all documents | `List[Document]` |
| `GET` | `/documents/{document_id}` | Get specific document | `Document` |
| `PUT` | `/documents/{document_id}` | Update document | `Document` |
| `DELETE` | `/documents/{document_id}` | Delete document | `dict` |
| `GET` | `/documents/{document_id}/download` | Download document file | File |
| `POST` | `/documents/{document_id}/grant-access` | Grant document access | `DocumentAccess` |
| `GET` | `/documents/projects/{project_id}` | Get project documents | `List[Document]` |

### Workforce Management Module (`/workforce`)

| Method | Endpoint | Description | Response Model |
|--------|----------|-------------|----------------|
| `POST` | `/workforce/professions/` | Create profession | `Profession` |
| `GET` | `/workforce/professions/` | Get all professions | `List[Profession]` |
| `GET` | `/workforce/professions/{profession_id}` | Get specific profession | `Profession` |
| `PUT` | `/workforce/professions/{profession_id}` | Update profession | `Profession` |
| `DELETE` | `/workforce/professions/{profession_id}` | Delete profession | `dict` |
| `POST` | `/workforce/workers/` | Create worker | `Worker` |
| `GET` | `/workforce/workers/` | Get all workers (with filters) | `List[WorkerWithProfession]` |
| `GET` | `/workforce/workers/available` | Get available workers | `List[WorkerWithProfession]` |
| `GET` | `/workforce/workers/by-project/{project_id}` | Get workers by project | `List[WorkerWithProfession]` |
| `GET` | `/workforce/workers/{worker_id}` | Get worker details | `WorkerDetailedView` |
| `PUT` | `/workforce/workers/{worker_id}` | Update worker | `Worker` |
| `DELETE` | `/workforce/workers/{worker_id}` | Delete worker | `dict` |
| `POST` | `/workforce/workers/{worker_id}/assign-project` | Assign worker to project | `dict` |
| `POST` | `/workforce/workers/{worker_id}/unassign-project` | Remove worker from project | `dict` |
| `POST` | `/workforce/project-history/` | Create project history | `WorkerProjectHistory` |
| `GET` | `/workforce/project-history/worker/{worker_id}` | Get worker's project history | `List[WorkerProjectHistory]` |
| `GET` | `/workforce/project-history/project/{project_id}` | Get project's worker history | `List[WorkerProjectHistory]` |
| `GET` | `/workforce/project-history/active` | Get active assignments | `List[WorkerProjectHistory]` |
| `PUT` | `/workforce/project-history/{history_id}` | Update project history | `WorkerProjectHistory` |
| `POST` | `/workforce/project-history/{history_id}/complete` | Complete project assignment | `dict` |
| `DELETE` | `/workforce/project-history/{history_id}` | Delete project history | `dict` |

---

## Complete Endpoint Reference

### 1. User Management Endpoints

#### POST `/users/clerk/invite-user/`
**Purpose**: Clerk invites new professional users to the platform

**Request Body**:
```json
{
  "email": "newuser@company.com",
  "full_name": "John Smith",
  "role": "project_manager",
  "invitation_message": "Welcome to BuildBuzz!"
}
```

**Query Parameters**:
- `clerk_id` (int, required): ID of the clerk performing invitation

**Response**: `User` object with `invitation_status: "pending"`

**Usage Example**:
```bash
curl -X POST "http://localhost:8000/users/clerk/invite-user/?clerk_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "manager@company.com",
    "full_name": "John Manager",
    "role": "project_manager"
  }'
```

#### POST `/users/setup-account/`
**Purpose**: User completes account setup using invitation token

**Request Body**:
```json
{
  "invitation_token": "abc123def456...",
  "password": "secure_password",
  "phone_number": "+1-555-0123",
  "address": "123 Main St"
}
```

**Response**: `User` object with `account_setup_completed: true`

#### GET `/users/business-admin/overview/`
**Purpose**: Business admin gets company overview and metrics

**Query Parameters**:
- `admin_id` (int, required): ID of business admin

**Response**:
```json
{
  "total_users": 45,
  "users_by_role": {
    "clerks": 2,
    "project_managers": 8,
    "accountants": 3,
    "clients": 25,
    "business_admins": 1
  },
  "company_metrics": {
    "active_users": 42,
    "pending_invitations": 3
  }
}
```

### 2. Project Management Endpoints

#### POST `/projects/`
**Purpose**: Create a new construction project

**Request Body**:
```json
{
  "name": "Downtown Office Complex",
  "description": "Modern 10-story office building",
  "start_date": "2024-03-01",
  "end_date": "2024-12-31",
  "budget": 5000000.00,
  "status": "planned",
  "client_name": "Metro Corporation",
  "project_manager_id": 3,
  "project_category": "Commercial",
  "project_type": "Office Building"
}
```

**Response**: Complete `Project` object with generated ID and timestamps

#### GET `/projects/{project_id}/components/`
**Purpose**: Get all components for a specific project

**Path Parameters**:
- `project_id` (int, required): Project ID

**Query Parameters**:
- `skip` (int, optional): Pagination offset (default: 0)
- `limit` (int, optional): Items per page (default: 100)

**Response**: Array of `ProjectComponent` objects

#### POST `/tasks/`
**Purpose**: Create a new task within a project component

**Request Body**:
```json
{
  "name": "Install Electrical Panel",
  "description": "Install main electrical distribution panel",
  "status": "To Do",
  "priority": "High",
  "component_id": 5,
  "project_id": 1,
  "task_type": "Construction",
  "estimated_hours": 16.0,
  "planned_start_date": "2024-07-01",
  "planned_end_date": "2024-07-02",
  "deadline": "2024-07-05",
  "assigned_to": 8,
  "created_by": 3,
  "requirements": "Follow electrical code standards",
  "budget_allocation": 2500.00
}
```

### 3. Finance Management Endpoints

#### POST `/finance/transactions/`
**Purpose**: Create a financial transaction for a project

**Request Body**:
```json
{
  "amount": 25000.00,
  "transaction_type": "expense",
  "description": "Steel beam purchase",
  "project_id": 1,
  "vendor_id": 3,
  "category_id": 2,
  "transaction_date": "2024-06-15",
  "due_date": "2024-07-15"
}
```

**Response**: Transaction confirmation with ID and status

#### POST `/finance/purchase-orders/{po_id}/approve`
**Purpose**: Approve a pending purchase order

**Path Parameters**:
- `po_id` (int, required): Purchase order ID

**Query Parameters**:
- `approved_by` (int, required): ID of user approving the order

**Response**: Updated `PurchaseOrder` with `status: "approved"`

### 4. Document Management Endpoints

#### POST `/documents/upload`
**Purpose**: Upload a new document file

**Request Body** (Form Data):
- `name` (string): Document name
- `description` (string, optional): Document description
- `file_type` (string): File extension/type
- `document_type` (string, optional): Category (blueprint, contract, etc.)
- `project_id` (int, optional): Associated project
- `component_id` (int, optional): Associated component
- `task_id` (int, optional): Associated task
- `file` (UploadFile): The actual file

**Response**: `DocumentResponse` with storage path and metadata

#### GET `/documents/{document_id}/download`
**Purpose**: Download a document file

**Path Parameters**:
- `document_id` (int, required): Document ID

**Response**: File stream with appropriate headers

---

### 5. Workforce Management Endpoints

#### POST `/workforce/professions/`
**Purpose**: Create a new construction profession/trade

**Request Body**:
```json
{
  "name": "Electrician",
  "description": "Licensed electrician for commercial and residential projects",
  "category": "Electrical"
}
```

**Response**: Complete `Profession` object with generated ID and timestamps

#### GET `/workforce/workers/`
**Purpose**: Get list of workers with optional filtering

**Query Parameters**:
- `skip` (int, optional): Pagination offset (default: 0)
- `limit` (int, optional): Items per page (default: 100)
- `profession_id` (int, optional): Filter by profession ID
- `availability` (string, optional): Filter by availability status
- `min_skill_rating` (float, optional): Minimum skill rating filter
- `max_skill_rating` (float, optional): Maximum skill rating filter (default: 10.0)

**Response**: Array of `WorkerWithProfession` objects

#### POST `/workforce/workers/`
**Purpose**: Create a new worker

**Request Body**:
```json
{
  "worker_id": "ELC001",
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+1-555-0101",
  "email": "john.smith@buildbuzz.com",
  "address": "123 Main St, Detroit, MI 48201",
  "profession_id": 1,
  "skill_rating": 8.5,
  "wage_rate": 35.50,
  "availability": "Available"
}
```

**Response**: Complete `Worker` object with generated ID

#### GET `/workforce/workers/{worker_id}`
**Purpose**: Get complete worker details including profession and project history

**Path Parameters**:
- `worker_id` (int, required): Worker's database ID

**Response**: `WorkerDetailedView` object with profession and project history

#### POST `/workforce/workers/{worker_id}/assign-project`
**Purpose**: Assign worker to a specific project

**Path Parameters**:
- `worker_id` (int, required): Worker's database ID

**Query Parameters**:
- `project_id` (int, required): Project ID to assign worker to
- `start_date` (date, required): Assignment start date (YYYY-MM-DD)
- `end_date` (date, optional): Assignment end date (YYYY-MM-DD)

**Response**:
```json
{
  "message": "Worker assigned to project successfully",
  "worker": { /* Updated worker object */ }
}
```

#### POST `/workforce/workers/{worker_id}/unassign-project`
**Purpose**: Remove worker from their current project assignment

**Path Parameters**:
- `worker_id` (int, required): Worker's database ID

**Response**:
```json
{
  "message": "Worker unassigned from project successfully",
  "worker": { /* Updated worker object */ }
}
```

#### GET `/workforce/workers/available`
**Purpose**: Get all workers currently available for assignment

**Response**: Array of `WorkerWithProfession` objects with `availability: "Available"`

#### GET `/workforce/workers/by-project/{project_id}`
**Purpose**: Get all workers currently assigned to a specific project

**Path Parameters**:
- `project_id` (int, required): Project ID

**Response**: Array of `WorkerWithProfession` objects assigned to the project

#### POST `/workforce/project-history/`
**Purpose**: Create a new project history entry for a worker

**Request Body**:
```json
{
  "worker_id": 1,
  "project_id": 1,
  "start_date": "2024-01-15",
  "end_date": "2024-03-30",
  "role": "Lead Electrician",
  "status": "Active",
  "performance_rating": 4.5,
  "notes": "Currently working on electrical installation"
}
```

**Response**: Complete `WorkerProjectHistory` object

#### GET `/workforce/project-history/worker/{worker_id}`
**Purpose**: Get complete project history for a specific worker

**Path Parameters**:
- `worker_id` (int, required): Worker's database ID

**Response**: Array of `WorkerProjectHistory` objects

#### POST `/workforce/project-history/{history_id}/complete`
**Purpose**: Mark a project assignment as completed

**Path Parameters**:
- `history_id` (int, required): Project history entry ID

**Query Parameters**:
- `end_date` (date, required): Completion date (YYYY-MM-DD)
- `performance_rating` (float, optional): Performance rating (1.0 to 5.0)
- `notes` (string, optional): Completion notes

**Response**:
```json
{
  "message": "Project assignment completed successfully",
  "history": { /* Updated project history object */ }
}
```

---

## Usage Examples

### Complete Workforce Management Workflow

#### 1. Create Professions
```bash
curl -X POST "http://localhost:8000/workforce/professions/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electrician",
    "description": "Licensed electrician for commercial and residential projects",
    "category": "Electrical"
  }'
```

#### 2. Add Workers
```bash
curl -X POST "http://localhost:8000/workforce/workers/" \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "ELC001",
    "first_name": "John",
    "last_name": "Smith",
    "phone_number": "+1-555-0101",
    "email": "john.smith@buildbuzz.com",
    "address": "123 Main St, Detroit, MI 48201",
    "profession_id": 1,
    "skill_rating": 8.5,
    "wage_rate": 35.50,
    "availability": "Available"
  }'
```

#### 3. Assign Worker to Project
```bash
curl -X POST "http://localhost:8000/workforce/workers/1/assign-project?project_id=1&start_date=2024-10-01&end_date=2024-12-15" \
  -H "Content-Type: application/json"
```

#### 4. Get Available Workers
```bash
curl "http://localhost:8000/workforce/workers/available"
```

#### 5. Get Workers by Skill Rating
```bash
curl "http://localhost:8000/workforce/workers/?min_skill_rating=8.0"
```

#### 6. Get Worker's Project History
```bash
curl "http://localhost:8000/workforce/project-history/worker/1"
```

#### 7. Complete Project Assignment
```bash
curl -X POST "http://localhost:8000/workforce/project-history/1/complete?end_date=2024-12-15&performance_rating=4.5&notes=Excellent work on electrical installation" \
  -H "Content-Type: application/json"
```

### Workforce Query Examples

#### Get All Electricians
```bash
curl "http://localhost:8000/workforce/workers/?profession_id=1"
```

#### Get High-Skilled Available Workers
```bash
curl "http://localhost:8000/workforce/workers/?availability=Available&min_skill_rating=8.5"
```

#### Get Project's Worker History
```bash
curl "http://localhost:8000/workforce/project-history/project/1"
```

#### Get All Active Assignments
```bash
curl "http://localhost:8000/workforce/project-history/active"
```

---

## Complete Project Workflow

#### 1. Create Project
```bash
curl -X POST "http://localhost:8000/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Residential Complex A",
    "description": "50-unit residential development",
    "start_date": "2024-06-01",
    "end_date": "2024-11-30",
    "budget": 3500000.00,
    "client_name": "Housing Solutions LLC",
    "project_manager_id": 3,
    "project_category": "Residential",
    "project_type": "Multi-Family"
  }'
```

#### 2. Add Project Component
```bash
curl -X POST "http://localhost:8000/components/" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "name": "Foundation",
    "description": "Concrete foundation for all units",
    "type": "Foundation",
    "allocated_budget": 450000.00,
    "estimated_duration_days": 30,
    "component_priority": 10,
    "is_critical_path": true
  }'
```

#### 3. Create Tasks
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Excavation",
    "description": "Site excavation for foundation",
    "component_id": 1,
    "project_id": 1,
    "task_type": "Construction",
    "priority": "Critical",
    "estimated_hours": 80.0,
    "planned_start_date": "2024-06-01",
    "planned_end_date": "2024-06-05",
    "budget_allocation": 15000.00,
    "assigned_to": 5
  }'
```

#### 4. Upload Project Documents
```bash
curl -X POST "http://localhost:8000/documents/upload" \
  -F "name=Site_Plan.pdf" \
  -F "description=Official site plan and layout" \
  -F "file_type=pdf" \
  -F "document_type=blueprint" \
  -F "project_id=1" \
  -F "file=@/path/to/site_plan.pdf"
```

#### 5. Create Financial Transaction
```bash
curl -X POST "http://localhost:8000/finance/transactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 35000.00,
    "transaction_type": "expense",
    "description": "Excavation equipment rental",
    "project_id": 1,
    "vendor_id": 2,
    "transaction_date": "2024-06-01"
  }'
```

### User Management Workflow

#### 1. Clerk Invites Project Manager
```bash
curl -X POST "http://localhost:8000/users/clerk/invite-user/?clerk_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "pm@company.com",
    "full_name": "Sarah Project Manager",
    "role": "project_manager",
    "invitation_message": "Welcome to the construction team!"
  }'
```

#### 2. User Completes Setup
```bash
curl -X POST "http://localhost:8000/users/setup-account/" \
  -H "Content-Type: application/json" \
  -d '{
    "invitation_token": "received_token_from_email",
    "password": "SecurePass123!",
    "phone_number": "+1-555-0167",
    "address": "456 Construction Ave"
  }'
```

### Query Examples

#### Get All Project Tasks
```bash
curl "http://localhost:8000/projects/1/tasks/"
```

#### Get Project Financial Summary
```bash
curl "http://localhost:8000/finance/projects/1/transactions/"
```

#### Get Business Overview
```bash
curl "http://localhost:8000/users/business-admin/overview/?admin_id=1"
```

---

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "detail": "Detailed error description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "field_errors": {
    "field_name": ["Field-specific error message"]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Examples

#### Validation Error (422)
```json
{
  "detail": "Validation failed",
  "field_errors": {
    "email": ["Invalid email format"],
    "budget": ["Budget must be positive number"]
  }
}
```

#### Not Found Error (404)
```json
{
  "detail": "Project not found",
  "error_code": "PROJECT_NOT_FOUND"
}
```

#### Permission Error (403)
```json
{
  "detail": "Only clerks can invite users",
  "error_code": "INSUFFICIENT_PERMISSIONS"
}
```

---

*Last Updated: October 14, 2025*
*Version: 2.0 (Complete Reference)*