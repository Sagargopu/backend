# BuildBuzz API Guide for Frontend Developers

## 📖 Overview

BuildBuzz is a comprehensive construction management system with a FastAPI backend. This guide provides complete documentation for frontend developers including all entities, API endpoints, JSON structures, and authentication details.

## 🌐 Base URL
```
http://localhost:8000
```

## 🔐 Authentication

### Test User Credentials
```json
{
  "superadmin": [
    {"email": "admin@buildbuzz.com", "password": "Admin123!"},
    {"email": "alex.admin@buildbuzz.com", "password": "alexadmin2024"}
  ],
  "business_admin": [
    {"email": "maria.business@buildbuzz.com", "password": "mariabiz2024"}
  ],
  "project_manager": [
    {"email": "emma.pm@buildbuzz.com", "password": "emmapm2024"}
  ],
  "accountant": [
    {"email": "robert.finance@buildbuzz.com", "password": "robertfin2024"}
  ],
  "clerk": [
    {"email": "tom.clerk@buildbuzz.com", "password": "tomclerk2024"}
  ],
  "client": [
    {"email": "linda.client@buildbuzz.com", "password": "lindaclient2024"}
  ]
}
```

### Authentication Flow
1. **Login**: POST `/users/login/` with email/password
2. **Response**: Returns JWT token
3. **Authorization**: Include token in headers: `Authorization: Bearer <token>`

---

## 👤 USER MANAGEMENT MODULE

### User Entity Structure
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@buildbuzz.com",
  "role": "project_manager",
  "is_active": true,
  "phone_number": "+1234567890",
  "address": "123 Main St, City, State",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+0987654321",
  "last_login_at": "2025-10-16T10:30:00Z",
  "created_at": "2025-10-15T09:00:00Z",
  "account_setup_completed": true,
  "invitation_status": "accepted"
}
```

### User Role Types
- `superadmin`: Full system access
- `business_admin`: Business operations management
- `project_manager`: Project oversight and management
- `accountant`: Financial management and approval
- `clerk`: Data entry and basic operations
- `client`: Project viewing and basic interactions

### User API Endpoints

#### Authentication
```http
POST /users/login/
Content-Type: application/json

{
  "email": "user@buildbuzz.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@buildbuzz.com",
    "role": "project_manager"
  }
}
```

#### User CRUD Operations
```http
# Get all users
GET /users/
Authorization: Bearer <token>

# Get current user profile
GET /users/me/
Authorization: Bearer <token>

# Get user by ID
GET /users/{user_id}/
Authorization: Bearer <token>

# Create new user (Admin only)
POST /users/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@buildbuzz.com",
  "role": "clerk",
  "phone_number": "+1234567890"
}

# Update user
PUT /users/{user_id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith-Updated",
  "phone_number": "+1234567891"
}

# Delete user (Admin only)
DELETE /users/{user_id}/
Authorization: Bearer <token>
```

---

## 🏗️ PROJECT MANAGEMENT MODULE

### Project Entity Structure
```json
{
  "id": 1,
  "name": "Downtown Office Complex",
  "description": "Modern 20-story office building with retail space",
  "start_date": "2025-01-15",
  "end_date": "2025-12-30",
  "planned_budget": 5000000.00,
  "actual_budget": 2500000.00,
  "status": "in_progress",
  "client_id": 5,
  "project_manager_id": 3,
  "accountant_id": 4,
  "project_type_id": 1,
  "created_at": "2025-10-15T09:00:00Z",
  "updated_at": "2025-10-16T10:30:00Z",
  "client": {
    "id": 5,
    "first_name": "Linda",
    "last_name": "Davis",
    "email": "linda.client@buildbuzz.com"
  },
  "project_manager": {
    "id": 3,
    "first_name": "Emma",
    "last_name": "Thompson",
    "email": "emma.pm@buildbuzz.com"
  },
  "accountant": {
    "id": 4,
    "first_name": "Robert",
    "last_name": "Johnson",
    "email": "robert.finance@buildbuzz.com"
  }
}
```

### Project Status Types
- `planned`: Project in planning phase
- `in_progress`: Currently under construction
- `completed`: Project finished
- `on_hold`: Temporarily paused

### Project Type Entity
```json
{
  "id": 1,
  "category": "Commercial",
  "type_name": "Office Building",
  "description": "Multi-story office complexes",
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Project Component Entity
```json
{
  "id": 1,
  "project_id": 1,
  "name": "Foundation",
  "description": "Building foundation and basement",
  "budget": 500000.00,
  "status": "completed",
  "start_date": "2025-01-15",
  "end_date": "2025-03-30",
  "parent_id": null,
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Task Entity
```json
{
  "id": 1,
  "name": "Pour Foundation Concrete",
  "description": "Pour concrete for main foundation",
  "status": "Done",
  "priority": "High",
  "component_id": 1,
  "project_id": 1,
  "task_type": "Construction",
  "budget": 50000.00,
  "start_date": "2025-02-01",
  "end_date": "2025-02-15",
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Task Status Types
- `To Do`: Not started
- `In Progress`: Currently working
- `Done`: Completed
- `Blocked`: Cannot proceed
- `Cancelled`: No longer needed
- `Backlog`: Planned for future

### Task Priority Types
- `Low`: Minor priority
- `Medium`: Normal priority
- `High`: Important task
- `Critical`: Urgent task

### Project API Endpoints

```http
# Get all projects
GET /projects/
Authorization: Bearer <token>

# Get project by ID
GET /projects/{project_id}/
Authorization: Bearer <token>

# Create new project
POST /projects/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Office Building",
  "description": "Modern office complex",
  "start_date": "2025-02-01",
  "end_date": "2025-12-31",
  "planned_budget": 3000000.00,
  "client_id": 5,
  "project_manager_id": 3,
  "accountant_id": 4,
  "project_type_id": 1
}

# Update project
PUT /projects/{project_id}/
Authorization: Bearer <token>

# Delete project
DELETE /projects/{project_id}/
Authorization: Bearer <token>

# Get project types
GET /project-types/
Authorization: Bearer <token>

# Create project type
POST /project-types/
Authorization: Bearer <token>
Content-Type: application/json

{
  "category": "Residential",
  "type_name": "Single Family Home",
  "description": "Individual residential houses"
}

# Get project components
GET /projects/{project_id}/components/
Authorization: Bearer <token>

# Create project component
POST /projects/{project_id}/components/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Electrical System",
  "description": "Complete electrical installation",
  "budget": 150000.00,
  "start_date": "2025-06-01",
  "end_date": "2025-08-30"
}

# Get tasks
GET /projects/{project_id}/tasks/
Authorization: Bearer <token>

# Create task
POST /tasks/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Install Main Electrical Panel",
  "description": "Install 400A main electrical panel",
  "priority": "High",
  "component_id": 2,
  "project_id": 1,
  "task_type": "Construction",
  "budget": 5000.00,
  "start_date": "2025-06-15",
  "end_date": "2025-06-20"
}

# Update task status
PUT /tasks/{task_id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "In Progress"
}
```

---

## 💰 FINANCE MANAGEMENT MODULE

### Vendor Entity
```json
{
  "id": 1,
  "name": "ABC Construction Supply",
  "contact_person": "Mike Johnson",
  "email": "mike@abcsupply.com",
  "phone": "+1234567890",
  "address": "456 Industrial Blvd, City, State",
  "vendor_type": "supplier",
  "is_active": true,
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Purchase Order Entity
```json
{
  "id": 1,
  "po_number": "PO-2025-001",
  "vendor_id": 1,
  "project_id": 1,
  "order_date": "2025-10-15",
  "delivery_date": "2025-10-25",
  "status": "approved",
  "total_amount": 25000.00,
  "notes": "Urgent delivery required",
  "created_by": 2,
  "approved_by": 4,
  "created_at": "2025-10-15T09:00:00Z",
  "items": [
    {
      "id": 1,
      "description": "Steel Rebar #4",
      "quantity": 100,
      "unit_price": 45.00,
      "total_price": 4500.00
    }
  ]
}
```

### Transaction Entity
```json
{
  "id": 1,
  "project_id": 1,
  "transaction_type": "expense",
  "amount": 15000.00,
  "description": "Material purchase - concrete",
  "transaction_date": "2025-10-15",
  "category": "materials",
  "reference_number": "TXN-2025-001",
  "created_by": 2,
  "approved_by": 4,
  "status": "approved",
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Change Order Entity
```json
{
  "id": 1,
  "project_id": 1,
  "change_order_number": "CO-2025-001",
  "description": "Additional electrical outlets",
  "reason": "Client requested additional power outlets",
  "cost_impact": 5000.00,
  "time_impact_days": 3,
  "status": "pending",
  "requested_by": 3,
  "approved_by": null,
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Finance API Endpoints

```http
# Get all vendors
GET /finance/vendors/
Authorization: Bearer <token>

# Create vendor
POST /finance/vendors/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "XYZ Materials Inc",
  "contact_person": "Sarah Wilson",
  "email": "sarah@xyzmaterials.com",
  "phone": "+1987654321",
  "address": "789 Supply St, City, State",
  "vendor_type": "supplier"
}

# Get purchase orders
GET /finance/purchase-orders/
Authorization: Bearer <token>

# Create purchase order
POST /finance/purchase-orders/
Authorization: Bearer <token>
Content-Type: application/json

{
  "vendor_id": 1,
  "project_id": 1,
  "delivery_date": "2025-11-01",
  "notes": "Standard delivery",
  "items": [
    {
      "description": "Concrete mix",
      "quantity": 50,
      "unit_price": 120.00
    }
  ]
}

# Approve purchase order
PUT /finance/purchase-orders/{po_id}/approve/
Authorization: Bearer <token>

# Get transactions
GET /finance/transactions/
Authorization: Bearer <token>

# Create transaction
POST /finance/transactions/
Authorization: Bearer <token>
Content-Type: application/json

{
  "project_id": 1,
  "transaction_type": "expense",
  "amount": 8500.00,
  "description": "Equipment rental",
  "category": "equipment",
  "reference_number": "REF-001"
}

# Get change orders
GET /finance/change-orders/
Authorization: Bearer <token>

# Create change order
POST /finance/change-orders/
Authorization: Bearer <token>
Content-Type: application/json

{
  "project_id": 1,
  "description": "Additional HVAC unit",
  "reason": "Increased capacity needed",
  "cost_impact": 12000.00,
  "time_impact_days": 7
}
```

---

## 👷 WORKFORCE MANAGEMENT MODULE

### Profession Entity
```json
{
  "id": 1,
  "name": "Electrician",
  "description": "Licensed electrical contractor",
  "hourly_rate_min": 45.00,
  "hourly_rate_max": 85.00,
  "skill_level": "skilled",
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Worker Entity
```json
{
  "id": 1,
  "first_name": "Carlos",
  "last_name": "Martinez",
  "email": "carlos.martinez@email.com",
  "phone": "+1234567890",
  "profession_id": 1,
  "hourly_rate": 65.00,
  "skill_level": "expert",
  "hire_date": "2024-03-15",
  "status": "active",
  "emergency_contact_name": "Maria Martinez",
  "emergency_contact_phone": "+1987654321",
  "certifications": ["Licensed Electrician", "OSHA 30"],
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Worker Project History Entity
```json
{
  "id": 1,
  "worker_id": 1,
  "project_id": 1,
  "start_date": "2025-01-15",
  "end_date": "2025-06-30",
  "role": "Lead Electrician",
  "hours_worked": 480.0,
  "performance_rating": 4.8,
  "notes": "Excellent work quality and leadership",
  "created_at": "2025-10-15T09:00:00Z"
}
```

### Workforce API Endpoints

```http
# Get all professions
GET /workforce/professions/
Authorization: Bearer <token>

# Create profession
POST /workforce/professions/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Plumber",
  "description": "Licensed plumbing contractor",
  "hourly_rate_min": 40.00,
  "hourly_rate_max": 75.00,
  "skill_level": "skilled"
}

# Get all workers
GET /workforce/workers/
Authorization: Bearer <token>

# Create worker
POST /workforce/workers/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "Ana",
  "last_name": "Rodriguez",
  "email": "ana.rodriguez@email.com",
  "phone": "+1555666777",
  "profession_id": 2,
  "hourly_rate": 55.00,
  "skill_level": "intermediate",
  "hire_date": "2025-01-10",
  "emergency_contact_name": "Luis Rodriguez",
  "emergency_contact_phone": "+1555666888"
}

# Get worker project history
GET /workforce/workers/{worker_id}/history/
Authorization: Bearer <token>

# Add worker to project
POST /workforce/workers/{worker_id}/projects/
Authorization: Bearer <token>
Content-Type: application/json

{
  "project_id": 1,
  "start_date": "2025-11-01",
  "role": "Junior Plumber"
}
```

---

## 📄 DOCUMENT MANAGEMENT MODULE

### Document Entity
```json
{
  "id": 1,
  "filename": "foundation-blueprint.pdf",
  "file_path": "/uploads/projects/1/foundation-blueprint.pdf",
  "file_size": 2048576,
  "mime_type": "application/pdf",
  "document_type": "blueprint",
  "description": "Foundation construction blueprint",
  "uploader_id": 3,
  "project_id": 1,
  "component_id": 1,
  "task_id": null,
  "is_active": true,
  "upload_date": "2025-10-15T14:30:00Z",
  "created_at": "2025-10-15T14:30:00Z"
}
```

### Document Access Entity
```json
{
  "id": 1,
  "user_id": 5,
  "document_id": 1,
  "permission_level": "read",
  "granted_by": 3,
  "granted_at": "2025-10-15T15:00:00Z"
}
```

### Document API Endpoints

```http
# Get all documents
GET /documents/
Authorization: Bearer <token>

# Get project documents
GET /documents/project/{project_id}/
Authorization: Bearer <token>

# Upload document
POST /documents/upload/
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "file": <file_data>,
  "document_type": "blueprint",
  "description": "Updated foundation plans",
  "project_id": 1,
  "component_id": 1
}

# Download document
GET /documents/{document_id}/download/
Authorization: Bearer <token>

# Grant document access
POST /documents/{document_id}/access/
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": 5,
  "permission_level": "read"
}

# Get document access permissions
GET /documents/{document_id}/access/
Authorization: Bearer <token>
```

---

## 📊 Response Status Codes

### Success Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Delete successful

### Client Error Codes
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

### Server Error Codes
- `500 Internal Server Error`: Server-side error

---

## 🔧 Common Error Response Format

```json
{
  "detail": "Error description",
  "error_code": "VALIDATION_ERROR",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

---

## 🚀 Getting Started Examples

### 1. Authenticate User
```javascript
const response = await fetch('http://localhost:8000/users/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'emma.pm@buildbuzz.com',
    password: 'emmapm2024'
  })
});

const data = await response.json();
const token = data.access_token;
```

### 2. Get Projects with Authentication
```javascript
const response = await fetch('http://localhost:8000/projects/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  }
});

const projects = await response.json();
```

### 3. Create New Project
```javascript
const response = await fetch('http://localhost:8000/projects/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'Shopping Mall Complex',
    description: 'Large retail shopping center',
    start_date: '2025-03-01',
    end_date: '2025-11-30',
    planned_budget: 8000000.00,
    client_id: 5,
    project_manager_id: 3,
    project_type_id: 1
  })
});

const newProject = await response.json();
```

---

## 📝 Notes for Frontend Developers

### 1. **Authentication**
- Always include the Bearer token in Authorization header
- Handle token expiration gracefully
- Store token securely (consider httpOnly cookies)

### 2. **Error Handling**
- Check response status codes
- Display user-friendly error messages
- Handle validation errors properly

### 3. **Data Relationships**
- Projects have clients, project managers, and accountants (all are users)
- Components belong to projects
- Tasks belong to components and projects
- Documents can be linked to projects, components, or tasks

### 4. **File Uploads**
- Use FormData for file uploads
- Handle large file uploads with progress indicators
- Validate file types and sizes on frontend

### 5. **Real-time Updates**
- Consider implementing WebSocket connections for real-time project updates
- Refresh data periodically for critical information

### 6. **Performance**
- Implement pagination for large data sets
- Use query parameters for filtering and searching
- Cache frequently accessed data

---

## 🔗 API Documentation URL

When the server is running, you can access interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive interfaces to test all API endpoints directly in the browser.
