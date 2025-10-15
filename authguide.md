# 🔐 BuildBuzz Backend Authentication Setup Guide

## Overview

This guide provides step-by-step instructions for implementing Clerk-based authentication in your BuildBuzz FastAPI backend with role-based access control (RBAC).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Schema Updates](#database-schema-updates)
4. [JWT Verification System](#jwt-verification-system)
5. [Authentication Dependencies](#authentication-dependencies)
6. [Authentication Endpoints](#authentication-endpoints)
7. [Protecting Existing Endpoints](#protecting-existing-endpoints)
8. [Testing](#testing)
9. [Production Deployment](#production-deployment)

---

## Prerequisites

### Required Dependencies
```bash
pip install python-jose[cryptography]  # JWT token verification
pip install requests                    # HTTP requests to Clerk API
pip install pydantic                    # Data validation
pip install python-multipart           # Form data handling
```

### User Roles
- **business_admin**: Full system access
- **business_clerk**: User management, project creation, workforce management
- **project_manager**: Project and workforce management
- **accountant**: Financial data and reports access

---

## Environment Setup

### 1. Environment Variables

Add these to your `.env` file:

```env
# Clerk Authentication
CLERK_SECRET_KEY=sk_test_your_secret_key_here
CLERK_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
CLERK_JWT_ISSUER=https://clerk.your-domain.com
CLERK_JWT_AUDIENCE=your-app-name

# Database (if not already configured)
DATABASE_URL=your_database_connection_string
```

### 2. Get Clerk Keys

1. Go to [Clerk Dashboard](https://dashboard.clerk.dev/)
2. Select your application
3. Navigate to **API Keys**
4. Copy the **Secret Key** and **Publishable Key**

---

## Database Schema Updates

### 1. Add Authentication Columns

Run these SQL commands to update your `users` table:

```sql
-- Add authentication columns
ALTER TABLE users ADD COLUMN clerk_user_id VARCHAR(255) UNIQUE;
ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'business_clerk';
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE users ADD COLUMN permissions TEXT; -- JSON as text
ALTER TABLE users ADD COLUMN last_login_at TIMESTAMP NULL;

-- Create indexes for performance
CREATE INDEX idx_users_clerk_user_id ON users(clerk_user_id);
CREATE INDEX idx_users_role ON users(role);
```

### 2. Update User Model

```python
# models/user.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: int
    email: str
    name: str
    
    # Authentication fields
    clerk_user_id: Optional[str] = None
    role: str = "business_clerk"
    is_active: bool = True
    permissions: List[str] = []
    last_login_at: Optional[datetime] = None
    
    # Existing fields
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

---

## JWT Verification System

### 1. Create JWT Utilities

```python
# utils/jwt_auth.py
import jwt
import requests
from typing import Optional, Dict
from fastapi import HTTPException, status
import os

class ClerkJWTVerifier:
    def __init__(self):
        self.clerk_secret_key = os.getenv("CLERK_SECRET_KEY")
        self.issuer = os.getenv("CLERK_JWT_ISSUER")
        self.audience = os.getenv("CLERK_JWT_AUDIENCE")
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify Clerk JWT token and return payload"""
        try:
            payload = jwt.decode(
                token,
                self.clerk_secret_key,
                algorithms=["HS256"],
                issuer=self.issuer,
                audience=self.audience
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

# Global instance
jwt_verifier = ClerkJWTVerifier()
```

### 2. Database Helper Functions

```python
# database/user_operations.py
from sqlalchemy.orm import Session
from models.user import User
from typing import Optional, Dict, List
import json

def get_user_by_clerk_id(db: Session, clerk_user_id: str) -> Optional[User]:
    """Get user by Clerk ID"""
    return db.query(User).filter(User.clerk_user_id == clerk_user_id).first()

def create_user_from_clerk(db: Session, user_data: Dict) -> User:
    """Create new user from Clerk data"""
    permissions_json = json.dumps(get_default_permissions(user_data.get("role", "business_clerk")))
    
    db_user = User(
        clerk_user_id=user_data["clerk_user_id"],
        email=user_data["email"],
        name=user_data["name"],
        role=user_data.get("role", "business_clerk"),
        permissions=permissions_json,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_default_permissions(role: str) -> List[str]:
    """Get default permissions for each role"""
    permission_map = {
        "business_admin": [
            "read:all", "write:all", "delete:all",
            "admin:users", "admin:projects", "admin:finances"
        ],
        "business_clerk": [
            "read:projects", "write:projects", "read:users", "write:users",
            "read:workforce", "write:workforce"
        ],
        "project_manager": [
            "read:projects", "write:projects", "read:workforce",
            "read:tasks", "write:tasks"
        ],
        "accountant": [
            "read:projects", "read:finances", "write:finances",
            "read:reports", "write:reports"
        ]
    }
    return permission_map.get(role, ["read:basic"])
```

---

## Authentication Dependencies

### 1. Create Authentication Dependencies

```python
# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.connection import get_db
from database.user_operations import get_user_by_clerk_id
from utils.jwt_auth import jwt_verifier
from typing import List
import json

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated user"""
    try:
        # Verify JWT token
        payload = jwt_verifier.verify_token(credentials.credentials)
        clerk_user_id = payload.get("sub")
        
        if not clerk_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Get user from database
        user = get_user_by_clerk_id(db, clerk_user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in database"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated"
            )
        
        # Parse permissions
        if user.permissions:
            user.permissions = json.loads(user.permissions) if isinstance(user.permissions, str) else user.permissions
        else:
            user.permissions = []
            
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

def require_roles(allowed_roles: List[str]):
    """Dependency to require specific roles"""
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return current_user
    return role_checker
```

---

## Authentication Endpoints

### 1. Create Authentication Router

```python
# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database.connection import get_db
from database.user_operations import *
from dependencies.auth import get_current_user, require_roles

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pydantic models
class UserResponse(BaseModel):
    clerk_user_id: str
    email: str
    name: str
    role: str
    permissions: List[str]
    is_active: bool

class UserSyncRequest(BaseModel):
    clerk_user_id: str
    email: str
    name: str
    role: str = "business_clerk"

class RoleUpdateRequest(BaseModel):
    role: str

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current authenticated user information"""
    return UserResponse(
        clerk_user_id=current_user.clerk_user_id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        permissions=current_user.permissions,
        is_active=current_user.is_active
    )

@router.post("/sync-user")
async def sync_clerk_user(
    user_data: UserSyncRequest,
    db: Session = Depends(get_db)
):
    """Sync Clerk user to internal database"""
    existing_user = get_user_by_clerk_id(db, user_data.clerk_user_id)
    
    if existing_user:
        # Update existing user
        existing_user.email = user_data.email
        existing_user.name = user_data.name
        db.commit()
        return {"message": "User updated successfully"}
    else:
        # Create new user
        new_user = create_user_from_clerk(db, user_data.dict())
        return {"message": "User created successfully", "user_id": new_user.id}

@router.get("/can-access")
async def can_access_route(
    route: str,
    current_user = Depends(get_current_user)
):
    """Check if current user can access a specific route"""
    allowed_routes = get_allowed_routes_for_role(current_user.role)
    home_route = get_home_route_for_role(current_user.role)
    
    return {
        "can_access": route in allowed_routes,
        "user_role": current_user.role,
        "allowed_routes": allowed_routes,
        "home_route": home_route
    }

def get_allowed_routes_for_role(role: str) -> List[str]:
    """Get allowed frontend routes for each role"""
    route_map = {
        "business_admin": [
            "/business-admin", "/business-admin/projects", 
            "/business-admin/employees", "/business-admin/financials",
            "/projects", "/users", "/tasks"
        ],
        "business_clerk": [
            "/business-clerk", "/business-clerk/user-management",
            "/business-clerk/project-management", "/business-clerk/workforce-management",
            "/projects", "/tasks"
        ],
        "project_manager": [
            "/project-manager", "/projects", "/tasks", "/workforce-management"
        ],
        "accountant": [
            "/accountant", "/financials", "/projects", "/reports"
        ]
    }
    return route_map.get(role, [])

def get_home_route_for_role(role: str) -> str:
    """Get home route for each role"""
    home_map = {
        "business_admin": "/business-admin",
        "business_clerk": "/business-clerk", 
        "project_manager": "/project-manager",
        "accountant": "/accountant"
    }
    return home_map.get(role, "/dashboard")
```

---

## Protecting Existing Endpoints

### 1. Update Existing Routers

Add authentication to your existing endpoints:

```python
# routers/projects.py
from dependencies.auth import get_current_user, require_roles

@router.get("/")
async def get_projects(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get projects - requires authentication"""
    # Your existing logic
    pass

@router.post("/")
async def create_project(
    project_data: ProjectCreate,
    current_user = Depends(require_roles(["business_admin", "business_clerk"])),
    db: Session = Depends(get_db)
):
    """Create project - requires admin or clerk role"""
    # Your existing logic
    pass

# routers/workforce.py
@router.get("/workers/")
async def get_workers(
    current_user = Depends(require_roles(["business_admin", "business_clerk", "project_manager"])),
    db: Session = Depends(get_db)
):
    """Get workers - requires specific roles"""
    # Your existing logic
    pass

# routers/users.py
@router.get("/")
async def get_users(
    current_user = Depends(require_roles(["business_admin", "business_clerk"])),
    db: Session = Depends(get_db)
):
    """Get users - admin/clerk only"""
    # Your existing logic
    pass
```

### 2. Update main.py

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import projects, users, workforce, auth

app = FastAPI(title="BuildBuzz API", version="2.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)      # Add auth router
app.include_router(projects.router)
app.include_router(users.router)
app.include_router(workforce.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "auth": "enabled"}
```

---

## Testing

### 1. Test Script

```python
# test_auth.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test if server is running"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())

def test_sync_user():
    """Test user sync endpoint"""
    sync_data = {
        "clerk_user_id": "test_user_123",
        "email": "test@example.com", 
        "name": "Test User",
        "role": "business_clerk"
    }
    
    response = requests.post(f"{BASE_URL}/auth/sync-user", json=sync_data)
    print("Sync User:", response.json())

def test_protected_endpoint_without_auth():
    """Test that protected endpoints require auth"""
    response = requests.get(f"{BASE_URL}/auth/me")
    print("Protected without auth:", response.status_code, response.json())

if __name__ == "__main__":
    test_health()
    test_sync_user()
    test_protected_endpoint_without_auth()
```

### 2. Manual Testing Steps

1. **Start server**: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
2. **Test health**: Visit `http://localhost:8000/health`
3. **View API docs**: Visit `http://localhost:8000/docs`
4. **Test endpoints**: Use the interactive API docs to test authentication

---

## Production Deployment

### 1. Security Configuration

```python
# config/security.py
import os
from functools import lru_cache

class Settings:
    # Clerk settings
    clerk_secret_key: str = os.getenv("CLERK_SECRET_KEY")
    clerk_publishable_key: str = os.getenv("CLERK_PUBLISHABLE_KEY")
    
    # JWT settings
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS settings
    allowed_origins: list = [
        "https://your-production-domain.com",
        "http://localhost:5173"  # Remove in production
    ]

@lru_cache()
def get_settings():
    return Settings()
```

### 2. Environment Variables for Production

```env
# Production .env
CLERK_SECRET_KEY=sk_live_your_production_secret_key
CLERK_PUBLISHABLE_KEY=pk_live_your_production_publishable_key
CLERK_JWT_ISSUER=https://your-production-domain.clerk.accounts.dev
CLERK_JWT_AUDIENCE=your-production-app

DATABASE_URL=your_production_database_url
```

---

## Implementation Checklist

### Phase 1: Setup
- [ ] Install required dependencies
- [ ] Configure environment variables
- [ ] Get Clerk API keys

### Phase 2: Database
- [ ] Add authentication columns to users table
- [ ] Update User model
- [ ] Create database indexes

### Phase 3: JWT System
- [ ] Create JWT verification utilities
- [ ] Implement database helper functions
- [ ] Test token verification

### Phase 4: Authentication
- [ ] Create authentication dependencies
- [ ] Build authentication endpoints
- [ ] Test role-based access

### Phase 5: Protection
- [ ] Add authentication to existing endpoints
- [ ] Update main application
- [ ] Test protected routes

### Phase 6: Testing & Deployment
- [ ] Test all authentication flows
- [ ] Configure production settings
- [ ] Deploy with proper security

---

## Common Issues & Solutions

### Issue: JWT Verification Fails
**Solution**: Check that Clerk secret key is correct and token format matches

### Issue: User Not Found After Login
**Solution**: Ensure `/auth/sync-user` is called after Clerk registration

### Issue: CORS Errors
**Solution**: Add your frontend URL to allowed origins in CORS middleware

### Issue: Permission Denied
**Solution**: Verify user role is correctly assigned and matches required roles

---

## API Endpoints Summary

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/auth/me` | GET | Get current user info | Yes |
| `/auth/sync-user` | POST | Sync Clerk user to database | No |
| `/auth/can-access` | GET | Check route access | Yes |
| `/health` | GET | Health check | No |
| `/projects/` | GET | Get projects | Yes |
| `/workforce/workers/` | GET | Get workers | Yes (role-based) |

---

## Support

For issues with this authentication setup:

1. Check the [Clerk Documentation](https://clerk.dev/docs)
2. Verify environment variables are set correctly
3. Test JWT token verification with online tools
4. Check database connections and user data

---

*This guide provides complete authentication setup for BuildBuzz backend with Clerk integration and role-based access control.*