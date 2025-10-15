"""
BuildBuzz API - Useful GET Endpoints Guide
This file documents the key GET endpoints you can test once the server is running
"""

# =============================================================================
# 🚀 HOW TO RUN THE SERVER
# =============================================================================

"""
1. Activate virtual environment:
   .\.venv\Scripts\Activate.ps1

2. Start the server:
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

3. Server will be available at: http://localhost:8000
4. API Documentation: http://localhost:8000/docs
5. Alternative docs: http://localhost:8000/redoc
"""

# =============================================================================
# 📡 KEY GET ENDPOINTS TO TEST YOUR DATA
# =============================================================================

GET_ENDPOINTS = {
    
    # =============================================================================
    # 👥 USER ENDPOINTS
    # =============================================================================
    "USERS": {
        "Get all users": "GET /users/",
        "Get user by ID": "GET /users/{user_id}",
        "Get users by role": "GET /users/?role=project_manager",
        "Get active users": "GET /users/?is_active=true",
        "Get user profile": "GET /users/{user_id}/profile",
    },
    
    # =============================================================================
    # 🏗️ PROJECT ENDPOINTS  
    # =============================================================================
    "PROJECTS": {
        "Get all projects": "GET /projects/",
        "Get project by ID": "GET /projects/{project_id}",
        "Get projects by status": "GET /projects/?status=in_progress",
        "Get projects by manager": "GET /projects/?project_manager_id={user_id}",
        "Get project components": "GET /projects/{project_id}/components",
        "Get project tasks": "GET /projects/{project_id}/tasks",
        "Get project timeline": "GET /projects/{project_id}/timeline",
    },
    
    # =============================================================================
    # 🔧 COMPONENT ENDPOINTS
    # =============================================================================
    "COMPONENTS": {
        "Get all components": "GET /components/",
        "Get component by ID": "GET /components/{component_id}",
        "Get component tasks": "GET /components/{component_id}/tasks",
        "Get components by type": "GET /components/?type=Foundation",
        "Get components by status": "GET /components/?status=in_progress",
    },
    
    # =============================================================================
    # 📋 TASK ENDPOINTS
    # =============================================================================
    "TASKS": {
        "Get all tasks": "GET /tasks/",
        "Get task by ID": "GET /tasks/{task_id}",
        "Get tasks by status": "GET /tasks/?status=In Progress",
        "Get tasks by priority": "GET /tasks/?priority=High",
        "Get tasks by assignee": "GET /tasks/?assigned_to={user_id}",
    },
    
    # =============================================================================
    # 💰 FINANCE ENDPOINTS
    # =============================================================================
    "FINANCE": {
        "Get all transactions": "GET /transactions/",
        "Get transaction by ID": "GET /transactions/{transaction_id}",
        "Get transactions by project": "GET /transactions/?project_id={project_id}",
        "Get transactions by type": "GET /transactions/?transaction_type=outgoing",
        "Get transactions by date range": "GET /transactions/?start_date=2024-01-01&end_date=2024-12-31",
        
        "Get all purchase orders": "GET /purchase-orders/",
        "Get PO by ID": "GET /purchase-orders/{po_id}",
        "Get POs by status": "GET /purchase-orders/?status=Approved",
        "Get POs by vendor": "GET /purchase-orders/?vendor_id={vendor_id}",
        
        "Get all change orders": "GET /change-orders/",
        "Get change order by ID": "GET /change-orders/{co_id}",
        "Get change orders by project": "GET /change-orders/?project_id={project_id}",
        "Get change orders by status": "GET /change-orders/?status=Pending Approval",
        
        "Get all vendors": "GET /vendors/",
        "Get vendor by ID": "GET /vendors/{vendor_id}",
        
        "Get all contracts": "GET /contracts/",
        "Get contract by ID": "GET /contracts/{contract_id}",
        "Get contracts by project": "GET /contracts/?project_id={project_id}",
    },
    
    # =============================================================================
    # 📄 DOCUMENT ENDPOINTS
    # =============================================================================
    "DOCUMENTS": {
        "Get all documents": "GET /documents/",
        "Get document by ID": "GET /documents/{document_id}",
        "Get documents by project": "GET /documents/?project_id={project_id}",
        "Get documents by type": "GET /documents/?document_type=blueprint",
        "Get public documents": "GET /documents/?is_public=true",
    },
    
    # =============================================================================
    # 📊 ANALYTICS & REPORTS
    # =============================================================================
    "ANALYTICS": {
        "Project summary": "GET /projects/{project_id}/summary",
        "Financial summary": "GET /projects/{project_id}/financial-summary", 
        "User workload": "GET /users/{user_id}/workload",
        "Project progress": "GET /projects/{project_id}/progress",
        "Budget analysis": "GET /projects/{project_id}/budget-analysis",
    }
}

# =============================================================================
# 🧪 SAMPLE TEST CALLS WITH YOUR DATA
# =============================================================================

SAMPLE_CALLS = """
Based on your loaded data, here are some specific endpoints you can test:

1. GET ALL USERS BY ROLE:
   http://localhost:8000/users/?role=project_manager
   http://localhost:8000/users/?role=accountant
   http://localhost:8000/users/?role=client

2. GET PROJECTS BY STATUS:
   http://localhost:8000/projects/?status=in_progress
   http://localhost:8000/projects/?status=planned

3. GET RECENT TRANSACTIONS:
   http://localhost:8000/transactions/?limit=20
   http://localhost:8000/transactions/?transaction_type=outgoing

4. GET CHANGE ORDERS NEEDING APPROVAL:
   http://localhost:8000/change-orders/?status=Pending Approval

5. GET PROJECT COMPONENTS:
   http://localhost:8000/projects/1/components
   http://localhost:8000/projects/2/components

6. GET VENDOR INFORMATION:
   http://localhost:8000/vendors/
   http://localhost:8000/vendors/1

7. GET PURCHASE ORDERS:
   http://localhost:8000/purchase-orders/?status=Approved
   http://localhost:8000/purchase-orders/?limit=10

8. GET TASKS BY STATUS:
   http://localhost:8000/tasks/?status=In Progress
   http://localhost:8000/tasks/?priority=High

9. GET PROJECT DOCUMENTS:
   http://localhost:8000/documents/?project_id=1
   http://localhost:8000/documents/?document_type=contract

10. GET USER WORKLOAD:
    http://localhost:8000/users/1
    http://localhost:8000/users/5/workload
"""

# =============================================================================
# 🔧 TROUBLESHOOTING SERVER STARTUP
# =============================================================================

TROUBLESHOOTING = """
If you're having issues starting the server:

1. SQLAlchemy compatibility issue with Python 3.13:
   pip install "sqlalchemy<2.1" --force-reinstall

2. Alternative server startup methods:
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   python -m uvicorn app.main:app --reload

3. Check if all dependencies are installed:
   pip install -r requirements.txt

4. Test individual modules:
   python -c "from app.main import app; print('App loaded successfully')"

5. Use different port if 8000 is busy:
   python -m uvicorn app.main:app --port 8080
"""

if __name__ == "__main__":
    print("🚀 BuildBuzz API Endpoints Guide")
    print("=" * 50)
    
    for category, endpoints in GET_ENDPOINTS.items():
        print(f"\n📡 {category} ENDPOINTS:")
        print("-" * 30)
        for desc, endpoint in endpoints.items():
            print(f"   {desc}: {endpoint}")
    
    print("\n" + "=" * 50)
    print("🧪 SAMPLE TEST CALLS:")
    print(SAMPLE_CALLS)
    
    print("\n" + "=" * 50)
    print("🔧 TROUBLESHOOTING:")
    print(TROUBLESHOOTING)