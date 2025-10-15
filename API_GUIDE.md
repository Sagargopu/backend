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

BuildBuzz is a simplified construction management system API that provides core functionality for managing users, projects, documents, and financial operations. The API follows RESTful principles and uses JSON for data exchange.

### System Architecture
```
Users → Projects → Components → Tasks
      → Documents
      → Finance (Transactions, Purchase Orders, etc.)
```

### Recent Updates (v2.0 - Simplified)
- ✅ **Removed**: Payroll and worker management features
- ✅ **Simplified**: User management to basic roles only
- ✅ **Focus**: Core project management workflow

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

## Usage Examples

### Complete Project Workflow

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