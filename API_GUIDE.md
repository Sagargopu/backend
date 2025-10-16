# BuildBuzz Backend API Documentation

## 🏗️ **Construction Management API**

### **Base URL:** `http://localhost:8000`

---

## 🔐 **Authentication System**

### **Authentication Method**
- **Type:** Role-based authentication with invitation system
- **Flow:** Invitation → Signup → Login → Role-based access
- **Roles:** `superadmin`, `business_admin`, `clerk`, `project_manager`, `accountant`, `client`

### **Authentication Flow**
1. **Invitation Phase:** Admin sends invitation with role
2. **Signup Phase:** User accepts invitation and sets password
3. **Login Phase:** User authenticates with email/password
4. **Access Phase:** Role-based endpoint access

---

## 🎯 **User Roles & Permissions**

### **Role Hierarchy** (Higher roles include lower permissions)
```
Superadmin (Level 6) - Full system access
├── Business Admin (Level 5) - Admin operations
├── Clerk (Level 4) - Data entry and user management
├── Project Manager (Level 3) - Project operations
├── Accountant (Level 2) - Financial operations
└── Client (Level 1) - Read-only project access
```

### **Role Capabilities**
| Role | Can Invite | Can Manage Projects | Can Manage Finances | Navigation Route |
|------|------------|-------------------|-------------------|------------------|
| **Superadmin** | All roles | ✅ | ✅ | `/admin/dashboard` |
| **Business Admin** | Clerk, PM, Accountant, Client | ✅ | ✅ | `/admin/dashboard` |
| **Clerk** | Client (future) | ❌ | ❌ | `/clerk/dashboard` |
| **Project Manager** | ❌ | ✅ | View only | `/projects/dashboard` |
| **Accountant** | ❌ | ❌ | ✅ | `/finance/dashboard` |
| **Client** | ❌ | ❌ | ❌ | `/client/dashboard` |

---

## 🔑 **Authentication Endpoints**

### **1. Send User Invitation**
```http
POST /users/invite/
Content-Type: application/json
```

**Request Body:**
```json
{
  "invitation": {
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "project_manager",
    "invitation_message": "Welcome to BuildBuzz!"
  },
  "inviter_id": 1
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "project_manager",
  "invitation_token": "abc123def456...",
  "invitation_status": "pending",
  "invitation_sent_date": "2025-10-15T10:00:00Z",
  "invitation_expires_at": "2025-10-22T10:00:00Z",
  "invited_by_user_id": 1,
  "is_active": false,
  "account_setup_completed": false,
  "created_at": "2025-10-15T10:00:00Z"
}
```

**Error Responses:**
```json
// 400 Bad Request - Invalid role or user exists
{
  "detail": "User with this email already exists"
}

// 403 Forbidden - Insufficient permissions
{
  "detail": "Cannot invite this role"
}
```

### **2. User Signup (Complete Invitation)**
```http
POST /users/signup/
Content-Type: application/json
```

**Request Body:**
```json
{
  "invitation_token": "abc123def456...",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "phone_number": "+1234567890",
  "address": "123 Main St, City, State",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+0987654321"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter  
- At least 1 number
- Password confirmation must match

**Response (200 OK):**
```json
{
  "id": 2,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "project_manager",
  "is_active": true,
  "account_setup_completed": true,
  "phone_number": "+1234567890",
  "address": "123 Main St, City, State",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+0987654321",
  "invitation_status": "accepted",
  "created_at": "2025-10-15T10:00:00Z"
}
```

**Error Responses:**
```json
// 400 Bad Request - Invalid token or expired
{
  "detail": "Invalid invitation token"
}

// 400 Bad Request - Password validation
{
  "detail": "Password must contain at least one uppercase letter"
}
```

### **3. User Login**
```http
POST /users/login/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 2,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "project_manager",
    "is_active": true,
    "account_setup_completed": true,
    "phone_number": "+1234567890",
    "created_at": "2025-10-15T10:00:00Z"
  },
  "navigation_route": "/projects/dashboard",
  "access_token": null,
  "token_type": "bearer"
}
```

**Error Responses:**
```json
// 401 Unauthorized - Invalid credentials
{
  "detail": "Incorrect password"
}

// 401 Unauthorized - Account issues
{
  "detail": "Account setup not completed"
}
```

### **4. Get Invitation Details**
```http
GET /users/invitation/{token}/
```

**Response (200 OK):**
```json
{
  "id": 2,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "project_manager",
  "invitation_status": "pending",
  "invitation_expires_at": "2025-10-22T10:00:00Z"
}
```

---

## 👥 **User Management Endpoints**

### **5. Get All Users** (Admin/Clerk only)
```http
GET /users/users/?skip=0&limit=100
```

**Query Parameters:**
- `requester_id` (required): ID of the requesting user
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "email": "admin@buildbuzz.com",
    "first_name": "System",
    "last_name": "Administrator",
    "role": "superadmin",
    "is_active": true,
    "account_setup_completed": true,
    "phone_number": "+1555-0101",
    "created_at": "2025-10-15T10:00:00Z"
  },
  {
    "id": 2,
    "email": "pm@buildbuzz.com",
    "first_name": "John",
    "last_name": "Manager",
    "role": "project_manager",
    "is_active": true,
    "account_setup_completed": true,
    "created_at": "2025-10-15T11:00:00Z"
  }
]
```

### **6. Get Users by Role** (Admin/Clerk only)
```http
GET /users/users/role/{role}/?requester_id=1&skip=0&limit=100
```

**Path Parameters:**
- `role`: One of `superadmin`, `business_admin`, `clerk`, `project_manager`, `accountant`, `client`

### **7. Get Pending Invitations** (Admin/Clerk only)
```http
GET /users/invitations/pending/?requester_id=1&skip=0&limit=100
```

**Response (200 OK):**
```json
[
  {
    "id": 3,
    "email": "pending@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "accountant",
    "invitation_status": "pending",
    "invitation_sent_date": "2025-10-15T10:00:00Z",
    "invitation_expires_at": "2025-10-22T10:00:00Z",
    "invited_by_user_id": 1,
    "account_setup_completed": false
  }
]
```

### **8. Get Available Roles for Invitation**
```http
GET /users/roles/?requester_id=1
```

**Response (200 OK):**
```json
[
  "clerk",
  "project_manager", 
  "accountant",
  "client"
]
```

### **9. Activate User Account** (Admin only)
```http
PUT /users/users/{user_id}/activate/?requester_id=1
```

**Response (200 OK):**
```json
{
  "message": "User activated successfully"
}
```

### **10. Deactivate User Account** (Admin only)
```http
PUT /users/users/{user_id}/deactivate/?requester_id=1
```

### **11. Expire Old Invitations** (Superadmin only)
```http
POST /users/invitations/expire/?requester_id=1
```

**Response (200 OK):**
```json
{
  "message": "Expired 3 old invitations"
}
```

---

## 🏗️ **Project Management Endpoints**

### **Data Models**

#### **Project Schema**
```json
{
  "id": 1,
  "name": "Downtown Office Complex",
  "description": "15-story office building with retail space",
  "start_date": "2024-01-15",
  "end_date": "2025-06-30",
  "budget": "2500000.00",
  "status": "in_progress",
  "client_name": "Metro Development Corp",
  "project_manager_id": 2,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### **Project Status Values**
- `planning` - Initial planning phase
- `in_progress` - Active construction
- `on_hold` - Temporarily paused
- `completed` - Project finished
- `cancelled` - Project cancelled

### **12. Create Project**
```http
POST /projects/
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "New Office Building",
  "description": "Modern 10-story office complex",
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "budget": "1500000.00",
  "status": "planning",
  "client_name": "ABC Corporation",
  "project_manager_id": 2
}
```

### **13. Get All Projects**
```http
GET /projects/?skip=0&limit=100
```

### **14. Get Project by ID**
```http
GET /projects/{project_id}
```

### **15. Update Project**
```http
PUT /projects/{project_id}
Content-Type: application/json
```

**Request Body (Partial Update):**
```json
{
  "status": "in_progress",
  "budget": "1750000.00"
}
```

### **16. Delete Project**
```http
DELETE /projects/{project_id}
```

---

## 🧩 **Project Components Endpoints**

#### **Component Schema**
```json
{
  "id": 1,
  "project_id": 1,
  "name": "Foundation & Structure",
  "description": "Foundation work and structural framework",
  "budget": "800000.00",
  "status": "in_progress",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### **17. Get Components for Project**
```http
GET /projects/{project_id}/components/
```

### **18. Create Component**
```http
POST /components/
Content-Type: application/json
```

**Request Body:**
```json
{
  "project_id": 1,
  "name": "Electrical Systems",
  "description": "Complete electrical installation",
  "budget": "450000.00",
  "status": "planned"
}
```

---

## ✅ **Task Management Endpoints**

#### **Task Schema**
```json
{
  "id": 1,
  "component_id": 1,
  "name": "Site Preparation",
  "description": "Clear and level the construction site",
  "assigned_to": 5,
  "status": "completed",
  "priority": "high",
  "estimated_hours": 40,
  "actual_hours": 45,
  "start_date": "2024-01-15",
  "due_date": "2024-01-17",
  "created_at": "2024-01-15T10:00:00Z"
}
```

#### **Task Status Values**
- `todo` - Not started
- `in_progress` - Currently being worked on
- `completed` - Finished
- `on_hold` - Temporarily paused
- `cancelled` - Cancelled

#### **Priority Values**
- `urgent` - Highest priority
- `high` - High priority
- `medium` - Normal priority
- `low` - Low priority

### **19. Get Tasks for Component**
```http
GET /components/{component_id}/tasks/?skip=0&limit=100
```

### **20. Create Task**
```http
POST /tasks/
Content-Type: application/json
```

**Request Body:**
```json
{
  "component_id": 1,
  "name": "Concrete Pour",
  "description": "Pour and cure foundation concrete",
  "assigned_to": 5,
  "status": "pending",
  "priority": "urgent",
  "estimated_hours": 60,
  "start_date": "2024-02-01",
  "due_date": "2024-02-03"
}
```

### **21. Get All Tasks for Project**
```http
GET /projects/{project_id}/tasks/
```

### **22. Get Project Task Summary**
```http
GET /projects/{project_id}/tasks/summary/
```

**Response:**
```json
{
  "project_id": 1,
  "total_tasks": 15,
  "components_with_tasks": 3,
  "by_status": {
    "todo": 5,
    "in_progress": 7,
    "completed": 3,
    "on_hold": 0,
    "cancelled": 0
  },
  "by_priority": {
    "urgent": 2,
    "high": 5,
    "medium": 6,
    "low": 2
  },
  "completion_rate": 20.0
}
```

---

## 💰 **Financial Management Endpoints**

#### **Transaction Schema**
```json
{
  "id": 1,
  "transaction_type": "outgoing",
  "expense_name": "Steel Beams Purchase",
  "description": "Structural steel beams for foundation",
  "amount": "15000.00",
  "transaction_date": "2024-02-15",
  "project_id": 1,
  "status": "approved",
  "payment_method": "bank_transfer",
  "vendor_supplier": "Steel Supply Co",
  "created_at": "2024-02-15T10:00:00Z"
}
```

#### **Transaction Types**
- `incoming` - Money received (payments from clients)
- `outgoing` - Money spent (payments to vendors)

#### **Payment Methods**
- `cash` - Cash payment
- `check` - Check payment
- `bank_transfer` - Bank transfer
- `credit_card` - Credit card payment
- `wire_transfer` - Wire transfer

### **23. Get All Transactions**
```http
GET /transactions/?skip=0&limit=100
```

### **24. Create Transaction**
```http
POST /transactions/
Content-Type: application/json
```

**Request Body:**
```json
{
  "transaction_type": "outgoing",
  "expense_name": "Equipment Rental",
  "description": "Excavator rental for foundation work",
  "amount": "3500.00",
  "transaction_date": "2024-02-20",
  "project_id": 1,
  "payment_method": "check",
  "vendor_supplier": "Equipment Rental Co"
}
```

### **25. Get Transactions by Project**
```http
GET /projects/{project_id}/transactions/
```

### **26. Approve Transaction**
```http
PUT /transactions/{transaction_id}/approve
Content-Type: application/json
```

**Request Body:**
```json
{
  "approval_notes": "Approved for construction phase"
}
```

---

## 📄 **Document Management Endpoints**

#### **Document Schema**
```json
{
  "id": 1,
  "name": "Blueprint_Floor1.pdf",
  "description": "First floor architectural blueprint",
  "storage_path": "/documents/blueprints/floor1.pdf",
  "file_type": "pdf",
  "file_size": 2048576,
  "document_type": "blueprint",
  "project_id": 1,
  "uploaded_by_id": 1,
  "is_public": false,
  "created_at": "2024-01-15T10:00:00Z"
}
```

#### **Document Types**
- `blueprint` - Architectural blueprints
- `contract` - Legal contracts
- `permit` - Building permits
- `invoice` - Financial invoices
- `photo` - Project photos
- `report` - Progress reports
- `other` - Other documents

### **27. Get All Documents**
```http
GET /documents/?skip=0&limit=100
```

### **28. Upload Document**
```http
POST /documents/upload
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: Binary file data
- `project_id`: Project ID (integer)
- `document_type`: Document type (string)
- `description`: Document description (string)

### **29. Get Documents by Project**
```http
GET /projects/{project_id}/documents/
```

### **30. Download Document**
```http
GET /documents/{document_id}/download
```

---

## 👷 **Workforce Management Endpoints**

#### **Profession Schema**
```json
{
  "id": 1,
  "name": "Electrician",
  "description": "Electrical installation and maintenance",
  "category": "Electrical",
  "created_at": "2024-01-15T10:00:00Z"
}
```

#### **Worker Schema**
```json
{
  "id": 1,
  "worker_id": "ELC001",
  "first_name": "Tom",
  "last_name": "Voltage",
  "email": "tom.voltage@example.com",
  "phone_number": "555-7001",
  "profession_id": 1,
  "skill_rating": "8.5",
  "wage_rate": "45.00",
  "availability": "Available",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### **31. Get All Professions**
```http
GET /workforce/professions/
```

### **32. Create Profession**
```http
POST /workforce/professions/
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Concrete Specialist",
  "description": "Concrete pouring and finishing",
  "category": "Structural"
}
```

### **33. Get All Workers**
```http
GET /workforce/workers/?skip=0&limit=100
```

### **34. Create Worker**
```http
POST /workforce/workers/
Content-Type: application/json
```

**Request Body:**
```json
{
  "worker_id": "CAR002",
  "first_name": "Sarah",
  "last_name": "Builder",
  "email": "sarah.builder@example.com",
  "phone_number": "555-7004",
  "profession_id": 3,
  "skill_rating": "9.0",
  "wage_rate": "42.00",
  "availability": "Available"
}
```

---

## 📊 **Response Formats**

### **Success Response Format**
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2",
  "created_at": "2025-10-15T10:00:00Z",
  "updated_at": "2025-10-15T10:00:00Z"
}
```

### **Error Response Format**
```json
{
  "detail": "Error description",
  "status_code": 400,
  "type": "validation_error"
}
```

### **List Response Format**
```json
[
  {
    "id": 1,
    "field1": "value1"
  },
  {
    "id": 2,
    "field1": "value2"
  }
]
```

### **Validation Error Format**
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "Password must contain at least one uppercase letter",
      "type": "value_error"
    }
  ]
}
```

---

## 🔄 **HTTP Status Codes**

| Code | Meaning | Usage |
|------|---------|--------|
| **200** | OK | Successful GET, PUT requests |
| **201** | Created | Successful POST requests |
| **204** | No Content | Successful DELETE requests |
| **400** | Bad Request | Invalid request data |
| **401** | Unauthorized | Authentication required |
| **403** | Forbidden | Insufficient permissions |
| **404** | Not Found | Resource not found |
| **422** | Unprocessable Entity | Validation errors |
| **500** | Internal Server Error | Server errors |

---

## 🧪 **Testing Examples**

### **Frontend Authentication Flow**

**1. Login User:**
```javascript
const login = async (email, password) => {
  const response = await fetch('/users/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password })
  });
  
  if (response.ok) {
    const data = await response.json();
    // Store user data and redirect to navigation_route
    localStorage.setItem('user', JSON.stringify(data.user));
    window.location.href = data.navigation_route;
  }
};
```

**2. Send Invitation:**
```javascript
const sendInvitation = async (invitationData, inviterId) => {
  const response = await fetch('/users/invite/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      invitation: invitationData,
      inviter_id: inviterId
    })
  });
  
  return await response.json();
};
```

**3. Complete Signup:**
```javascript
const completeSignup = async (signupData) => {
  const response = await fetch('/users/signup/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(signupData)
  });
  
  if (response.ok) {
    // Redirect to login page
    window.location.href = '/login';
  }
};
```

---

## 🚀 **Getting Started**

### **1. Start the Backend Server**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### **2. Create Initial Superuser**
```bash
python create_superuser_with_password.py
```

### **3. Test API Endpoints**
- **Interactive Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`
- **Root Endpoint:** `http://localhost:8000/`

### **4. Database Setup**
```bash
python setup_database.py
```

---

## 📝 **Important Notes for Frontend**

1. **Password Validation:** Enforce password rules on frontend for better UX
2. **Role-based UI:** Show/hide UI elements based on user role
3. **Error Handling:** Handle all HTTP status codes appropriately
4. **Token Expiry:** Invitation tokens expire in 7 days
5. **Navigation:** Use `navigation_route` from login response for role-based routing
6. **Timestamps:** All dates are in ISO 8601 format (UTC)
7. **Money Fields:** All amounts are strings with 2 decimal places
8. **File Uploads:** Use `multipart/form-data` for document uploads

---

**Server Status:** ✅ Running at `http://localhost:8000`  
**Interactive Documentation:** `http://localhost:8000/docs`  
**Health Endpoint:** `http://localhost:8000/health`
