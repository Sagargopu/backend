# BuildBuzz API Guide

## Overview
This is a comprehensive guide for the BuildBuzz Construction Management API, detailing all available models, endpoints, HTTP methods, and JSON samples.

## Base URL
```
http://localhost:8000
```

---

# 📊 Data Models

## 👤 User Management

### User Model
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "role": "project_manager",
  "is_active": true,
  "phone_number": "+1-555-0123",
  "address": "123 Main St, City, State 12345",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1-555-0124",
  "last_login_at": "2025-10-15T10:30:00Z",
  "invitation_status": "accepted",
  "account_setup_completed": true,
  "created_at": "2025-01-15T08:00:00Z"
}
```

**Roles Available:**
- `superadmin` - Full system access
- `business_admin` - Business-level administration
- `project_manager` - Project management capabilities
- `accountant` - Financial management
- `clerk` - Basic data entry
- `client` - Client-specific access

---

## 🏗️ Project Management

### ProjectType Model
```json
{
  "id": 1,
  "category": "Residential",
  "type_name": "Single Family Home",
  "description": "Construction of single-family residential homes",
  "created_at": "2025-01-15T08:00:00Z"
}
```

### Project Model
```json
{
  "id": 1,
  "name": "Sunset Villa Construction",
  "description": "3-bedroom luxury home construction",
  "start_date": "2025-02-01",
  "end_date": "2025-08-30",
  "planned_budget": 450000.00,
  "actual_budget": 45000.00,
  "status": "in_progress",
  "client_id": 5,
  "project_manager_id": 2,
  "project_type_id": 1,
  "created_at": "2025-01-15T08:00:00Z",
  "updated_at": "2025-10-15T10:30:00Z"
}
```

**Project Status Options:**
- `planned` - Project in planning phase
- `in_progress` - Active construction
- `completed` - Project finished
- `on_hold` - Temporarily suspended

### ProjectComponent Model
```json
{
  "id": 1,
  "project_id": 1,
  "name": "Foundation",
  "description": "Concrete foundation and basement",
  "budget": 75000.00,
  "status": "completed",
  "start_date": "2025-02-01",
  "end_date": "2025-03-15",
  "parent_id": null,
  "created_at": "2025-01-15T08:00:00Z",
  "updated_at": "2025-03-16T09:00:00Z"
}
```

### Task Model
```json
{
  "id": 1,
  "name": "Pour Foundation Concrete",
  "description": "Pour concrete for foundation and basement walls",
  "status": "Done",
  "priority": "High",
  "task_type": "Construction",
  "budget": 25000.00,
  "start_date": "2025-02-10",
  "end_date": "2025-02-12",
  "component_id": 1,
  "project_id": 1,
  "created_at": "2025-01-15T08:00:00Z",
  "updated_at": "2025-02-13T16:00:00Z"
}
```

**Task Status Options:**
- `To Do` - Not started
- `In Progress` - Currently active
- `Done` - Completed
- `Blocked` - Cannot proceed
- `Cancelled` - Cancelled task
- `Backlog` - Scheduled for later

**Priority Levels:**
- `Low`, `Medium`, `High`, `Critical`

---

## 💰 Finance Management

### Vendor Model
```json
{
  "id": 1,
  "name": "ABC Materials Supply",
  "representative_name": "Mike Johnson",
  "email": "mike@abcmaterials.com",
  "phone": "+1-555-0199",
  "address": "456 Industrial Blvd, City, State 12345",
  "business_type": "Material Supplier",
  "is_active": true,
  "created_at": "2025-01-10T08:00:00Z",
  "updated_at": "2025-01-10T08:00:00Z"
}
```

**Business Types:**
- `Material Supplier`
- `Subcontractor`
- `Equipment Rental`
- `Service Provider`

### PurchaseOrder Model
```json
{
  "id": 1,
  "po_number": "PO-2025-001",
  "task_id": 1,
  "vendor_id": 1,
  "description": "Concrete and rebar for foundation",
  "delivery_date": "2025-02-08",
  "status": "Approved",
  "created_by": 2,
  "approved_by": 3,
  "approved_date": "2025-02-05T14:30:00Z",
  "notes": "Rush delivery required",
  "created_at": "2025-02-03T09:00:00Z",
  "updated_at": "2025-02-05T14:30:00Z"
}
```

**PO Status Options:**
- `Draft`, `Pending Approval`, `Approved`, `Rejected`, `Delivered`, `Paid`

### PurchaseOrderItem Model
```json
{
  "id": 1,
  "purchase_order_id": 1,
  "item_name": "Ready-Mix Concrete",
  "description": "3000 PSI concrete for foundation",
  "category": "Material",
  "price": 125.50,
  "created_at": "2025-02-03T09:00:00Z",
  "updated_at": "2025-02-03T09:00:00Z"
}
```

### ChangeOrder Model
```json
{
  "id": 1,
  "co_number": "CO-2025-001",
  "task_id": 1,
  "title": "Additional Waterproofing",
  "description": "Add extra waterproofing membrane per client request",
  "reason": "Client Request",
  "status": "Approved",
  "created_by": 2,
  "approved_by": 3,
  "approved_date": "2025-02-20T11:00:00Z",
  "notes": "Client approved additional cost",
  "created_at": "2025-02-18T10:00:00Z",
  "updated_at": "2025-02-20T11:00:00Z"
}
```

**Change Order Reasons:**
- `Client Request`
- `Design Change`
- `Site Condition`
- `Code Requirement`

### ChangeOrderItem Model
```json
{
  "id": 1,
  "change_order_id": 1,
  "item_name": "Waterproofing Membrane",
  "description": "Premium waterproofing system",
  "change_type": "Addition",
  "impact_type": "+",
  "amount": 5500.00,
  "created_at": "2025-02-18T10:00:00Z",
  "updated_at": "2025-02-18T10:00:00Z"
}
```

**Change Types:**
- `Addition`, `Deletion`, `Modification`

**Impact Types:**
- `+` - Cost increase
- `-` - Cost decrease

### Transaction Model
```json
{
  "id": 1,
  "transaction_number": "TXN-2025-001",
  "project_id": 1,
  "task_id": 1,
  "transaction_type": "purchase_order",
  "source_id": 1,
  "source_number": "PO-2025-001",
  "amount": 25000.00,
  "impact_type": "+",
  "description": "Foundation materials purchase",
  "budget_before": 450000.00,
  "budget_after": 475000.00,
  "approved_by": 3,
  "approved_date": "2025-02-05T14:30:00Z",
  "created_at": "2025-02-05T14:30:00Z",
  "updated_at": "2025-02-05T14:30:00Z"
}
```

---

## 👷 Workforce Management

### Profession Model
```json
{
  "id": 1,
  "name": "Electrician",
  "description": "Licensed electrical work specialist",
  "category": "Electrical",
  "created_at": "2025-01-05T08:00:00Z",
  "updated_at": "2025-01-05T08:00:00Z"
}
```

**Categories:**
- `Electrical`, `Plumbing`, `Structural`, `Finishing`

### Worker Model
```json
{
  "id": 1,
  "worker_id": "WKR-001",
  "first_name": "Carlos",
  "last_name": "Rodriguez",
  "phone_number": "+1-555-0156",
  "email": "carlos.rodriguez@email.com",
  "profession_id": 1,
  "wage_rate": 35.50,
  "availability": "Available",
  "created_at": "2025-01-08T08:00:00Z",
  "updated_at": "2025-10-15T10:30:00Z"
}
```

**Availability Status:**
- `Available`, `Assigned`, `Unavailable`, `On Leave`

### WorkerProjectHistory Model
```json
{
  "id": 1,
  "worker_id": 1,
  "project_id": 1,
  "start_date": "2025-02-15",
  "end_date": "2025-03-20",
  "role": "Lead Electrician",
  "status": "Completed",
  "created_at": "2025-02-15T08:00:00Z",
  "updated_at": "2025-03-21T17:00:00Z"
}
```

**History Status:**
- `Active`, `Completed`, `Terminated`

---

## 📄 Document Management

### Document Model
```json
{
  "id": 1,
  "name": "Foundation_Plans.pdf",
  "description": "Detailed foundation construction plans",
  "doc_type": "pdf",
  "project_id": 1,
  "component_id": 1,
  "task_id": 1,
  "uploaded_by": 2,
  "created_at": "2025-01-20T09:00:00Z",
  "updated_at": "2025-01-20T09:00:00Z"
}
```

---

# 🛠️ API Endpoints

## 👤 User Management (`/users`)

### Create User
- **POST** `/users/`
- **Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe", 
  "email": "john.doe@example.com",
  "role": "project_manager",
  "phone_number": "+1-555-0123"
}
```

### Get All Users
- **GET** `/users/`
- **Query Parameters:** `skip=0`, `limit=100`

### Get User by ID
- **GET** `/users/{user_id}`

### Update User
- **PUT** `/users/{user_id}`
- **Request Body:** (same as create, all fields optional)

### Delete User
- **DELETE** `/users/{user_id}`

### Get Users by Role
- **GET** `/users/by-role/{role}`

---

## 🏗️ Project Management

### ProjectType Endpoints

#### Create Project Type
- **POST** `/project-types/`
```json
{
  "category": "Commercial",
  "type_name": "Office Building",
  "description": "Multi-story office construction"
}
```

#### Get All Project Types
- **GET** `/project-types/`

#### Get Project Type by ID
- **GET** `/project-types/{type_id}`

#### Update Project Type
- **PUT** `/project-types/{type_id}`

#### Delete Project Type
- **DELETE** `/project-types/{type_id}`

### Project Endpoints

#### Create Project
- **POST** `/projects/`
```json
{
  "name": "Downtown Office Complex",
  "description": "15-story office building",
  "start_date": "2025-03-01",
  "end_date": "2025-12-31",
  "planned_budget": 2500000.00,
  "client_id": 5,
  "project_manager_id": 2,
  "project_type_id": 2
}
```

#### Get All Projects
- **GET** `/projects/`
- **Query Parameters:** `skip=0`, `limit=100`

#### Get Project by ID
- **GET** `/projects/{project_id}`

#### Update Project
- **PUT** `/projects/{project_id}`

#### Delete Project
- **DELETE** `/projects/{project_id}`

#### Get Projects by Client
- **GET** `/projects/by-client/{client_id}`

#### Get Projects by Manager
- **GET** `/projects/by-manager/{manager_id}`

#### Get Projects by Type
- **GET** `/projects/by-type/{type_id}`

### ProjectComponent Endpoints

#### Create Component
- **POST** `/project-components/`
```json
{
  "project_id": 1,
  "name": "Electrical System",
  "description": "Complete electrical installation",
  "budget": 85000.00,
  "start_date": "2025-04-01",
  "end_date": "2025-06-15",
  "parent_id": null
}
```

#### Get All Components
- **GET** `/project-components/`

#### Get Component by ID
- **GET** `/project-components/{component_id}`

#### Update Component
- **PUT** `/project-components/{component_id}`

#### Delete Component
- **DELETE** `/project-components/{component_id}`

#### Get Components by Project
- **GET** `/projects/{project_id}/components`

### Task Endpoints

#### Create Task
- **POST** `/tasks/`
```json
{
  "name": "Install Main Electrical Panel",
  "description": "Install and wire main electrical distribution panel",
  "status": "To Do",
  "priority": "High",
  "task_type": "Construction",
  "budget": 8500.00,
  "start_date": "2025-04-05",
  "end_date": "2025-04-08",
  "component_id": 2,
  "project_id": 1
}
```

#### Get All Tasks
- **GET** `/tasks/`

#### Get Task by ID
- **GET** `/tasks/{task_id}`

#### Update Task
- **PUT** `/tasks/{task_id}`

#### Delete Task
- **DELETE** `/tasks/{task_id}`

#### Get Tasks by Project
- **GET** `/projects/{project_id}/tasks`

#### Get Tasks by Component
- **GET** `/project-components/{component_id}/tasks`

---

## 💰 Finance Management (`/finance`)

### Vendor Endpoints

#### Create Vendor
- **POST** `/finance/vendors/`
```json
{
  "name": "Elite Construction Supplies",
  "representative_name": "Sarah Wilson",
  "email": "sarah@elitecsupply.com",
  "phone": "+1-555-0177",
  "address": "789 Supply St, City, State 12345",
  "business_type": "Material Supplier"
}
```

#### Get All Vendors
- **GET** `/finance/vendors/`

#### Get Vendor by ID
- **GET** `/finance/vendors/{vendor_id}`

#### Get Active Vendors
- **GET** `/finance/vendors/active`

#### Update Vendor
- **PUT** `/finance/vendors/{vendor_id}`

#### Delete Vendor
- **DELETE** `/finance/vendors/{vendor_id}`

### Purchase Order Endpoints

#### Create Purchase Order
- **POST** `/finance/purchase-orders/`
```json
{
  "po_number": "PO-2025-002",
  "task_id": 2,
  "vendor_id": 1,
  "description": "Electrical supplies for main panel installation",
  "delivery_date": "2025-04-03",
  "created_by": 2,
  "notes": "Coordinate with project manager"
}
```

#### Get All Purchase Orders
- **GET** `/finance/purchase-orders/`

#### Get Purchase Order by ID
- **GET** `/finance/purchase-orders/{po_id}`

#### Get Purchase Orders by Status
- **GET** `/finance/purchase-orders/by-status/{status}`

#### Get Purchase Orders by Task
- **GET** `/finance/purchase-orders/by-task/{task_id}`

#### Update Purchase Order
- **PUT** `/finance/purchase-orders/{po_id}`

#### Delete Purchase Order
- **DELETE** `/finance/purchase-orders/{po_id}`

#### Get Purchase Order Items
- **GET** `/finance/purchase-orders/{po_id}/items`

### Purchase Order Item Endpoints

#### Create Purchase Order Item
- **POST** `/finance/purchase-order-items/`
```json
{
  "purchase_order_id": 2,
  "item_name": "200A Main Breaker Panel",
  "description": "Square D 200-amp main electrical panel",
  "category": "Material",
  "price": 485.00
}
```

#### Get Purchase Order Item by ID
- **GET** `/finance/purchase-order-items/{item_id}`

#### Update Purchase Order Item
- **PUT** `/finance/purchase-order-items/{item_id}`

#### Delete Purchase Order Item
- **DELETE** `/finance/purchase-order-items/{item_id}`

### Change Order Endpoints

#### Create Change Order
- **POST** `/finance/change-orders/`
```json
{
  "co_number": "CO-2025-002",
  "task_id": 2,
  "title": "Upgrade to Smart Panel",
  "description": "Client requested upgrade to smart electrical panel with monitoring",
  "reason": "Client Request",
  "created_by": 2,
  "notes": "Client will pay additional cost"
}
```

#### Get All Change Orders
- **GET** `/finance/change-orders/`

#### Get Change Order by ID
- **GET** `/finance/change-orders/{co_id}`

#### Get Change Orders by Status
- **GET** `/finance/change-orders/by-status/{status}`

#### Get Change Orders by Task
- **GET** `/finance/change-orders/by-task/{task_id}`

#### Update Change Order
- **PUT** `/finance/change-orders/{co_id}`

#### Delete Change Order
- **DELETE** `/finance/change-orders/{co_id}`

#### Get Change Order Items
- **GET** `/finance/change-orders/{co_id}/items`

### Change Order Item Endpoints

#### Create Change Order Item
- **POST** `/finance/change-order-items/`
```json
{
  "change_order_id": 2,
  "item_name": "Smart Panel Upgrade",
  "description": "Upgrade from standard to smart monitoring panel",
  "change_type": "Modification",
  "impact_type": "+",
  "amount": 1200.00
}
```

#### Get Change Order Item by ID
- **GET** `/finance/change-order-items/{item_id}`

#### Update Change Order Item
- **PUT** `/finance/change-order-items/{item_id}`

#### Delete Change Order Item
- **DELETE** `/finance/change-order-items/{item_id}`

### Transaction Endpoints

#### Create Transaction
- **POST** `/finance/transactions/`
```json
{
  "transaction_number": "TXN-2025-002",
  "project_id": 1,
  "task_id": 2,
  "transaction_type": "change_order",
  "source_id": 2,
  "source_number": "CO-2025-002",
  "amount": 1200.00,
  "impact_type": "+",
  "description": "Smart panel upgrade approved",
  "budget_before": 475000.00,
  "budget_after": 476200.00,
  "approved_by": 3,
  "approved_date": "2025-04-01T15:00:00Z"
}
```

#### Get All Transactions
- **GET** `/finance/transactions/`

#### Get Transaction by ID
- **GET** `/finance/transactions/{transaction_id}`

#### Get Transactions by Project
- **GET** `/finance/transactions/by-project/{project_id}`

#### Get Transactions by Task
- **GET** `/finance/transactions/by-task/{task_id}`

#### Get Transactions by Type
- **GET** `/finance/transactions/by-type/{transaction_type}`

---

## 👷 Workforce Management (`/workforce`)

### Profession Endpoints

#### Create Profession
- **POST** `/workforce/professions/`
```json
{
  "name": "HVAC Technician",
  "description": "Heating, ventilation, and air conditioning specialist",
  "category": "Mechanical"
}
```

#### Get All Professions
- **GET** `/workforce/professions/`

#### Get Profession by ID
- **GET** `/workforce/professions/{profession_id}`

#### Update Profession
- **PUT** `/workforce/professions/{profession_id}`

#### Delete Profession
- **DELETE** `/workforce/professions/{profession_id}`

### Worker Endpoints

#### Create Worker
- **POST** `/workforce/workers/`
```json
{
  "worker_id": "WKR-002",
  "first_name": "Maria",
  "last_name": "Garcia",
  "phone_number": "+1-555-0188",
  "email": "maria.garcia@email.com",
  "profession_id": 2,
  "wage_rate": 42.75,
  "availability": "Available"
}
```

#### Get All Workers
- **GET** `/workforce/workers/`

#### Get Worker by ID
- **GET** `/workforce/workers/{worker_id}`

#### Get Workers by Profession
- **GET** `/workforce/workers/by-profession/{profession_id}`

#### Get Workers by Availability
- **GET** `/workforce/workers/by-availability/{availability}`

#### Get Available Workers
- **GET** `/workforce/workers/available`

#### Update Worker
- **PUT** `/workforce/workers/{worker_id}`

#### Delete Worker
- **DELETE** `/workforce/workers/{worker_id}`

### Worker Project History Endpoints

#### Create Worker Project History
- **POST** `/workforce/worker-history/`
```json
{
  "worker_id": 2,
  "project_id": 1,
  "start_date": "2025-04-01",
  "end_date": null,
  "role": "HVAC Lead Technician",
  "status": "Active"
}
```

#### Get Worker Project History by ID
- **GET** `/workforce/worker-history/{history_id}`

#### Get Worker's History
- **GET** `/workforce/workers/{worker_id}/history`

#### Get Project's Worker History
- **GET** `/workforce/projects/{project_id}/worker-history`

#### Update Worker Project History
- **PUT** `/workforce/worker-history/{history_id}`

#### Delete Worker Project History
- **DELETE** `/workforce/worker-history/{history_id}`

---

## 📄 Document Management (`/documents`)

### Document Endpoints

#### Create Document
- **POST** `/documents/`
```json
{
  "name": "Electrical_Permit.pdf",
  "description": "City electrical permit for project",
  "doc_type": "pdf",
  "project_id": 1,
  "component_id": 2,
  "task_id": 2,
  "uploaded_by": 2
}
```

#### Get All Documents
- **GET** `/documents/`

#### Get Document by ID
- **GET** `/documents/{document_id}`

#### Update Document
- **PUT** `/documents/{document_id}`

#### Delete Document
- **DELETE** `/documents/{document_id}`

#### Get Documents by Project
- **GET** `/documents/by-project/{project_id}`

#### Get Documents by Component
- **GET** `/documents/by-component/{component_id}`

#### Get Documents by Task
- **GET** `/documents/by-task/{task_id}`

---

# 📋 HTTP Status Codes

## Success Codes
- **200 OK** - Successful GET, PUT requests
- **201 Created** - Successful POST requests
- **204 No Content** - Successful DELETE requests

## Error Codes
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **422 Unprocessable Entity** - Validation errors
- **500 Internal Server Error** - Server error

## Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

# 🔧 Development Notes

## Authentication
- Currently, most endpoints don't require authentication
- Future implementation will include JWT token-based authentication
- Role-based access control will be enforced

## Pagination
- Default pagination: `skip=0`, `limit=100`
- Maximum limit: 1000 items per request

## Filtering
- Many GET endpoints support filtering by related entities
- Use specific filter endpoints for better performance

## Data Validation
- All POST/PUT requests validate data using Pydantic schemas
- Foreign key relationships are validated
- Date ranges are validated (start_date < end_date)

## Database Relationships
- All models support proper cascade operations
- Foreign key constraints are enforced
- Circular dependencies are handled with string references

---

*Last Updated: October 16, 2025*
*Version: 1.0*
