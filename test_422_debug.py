#!/usr/bin/env python3
"""
Debug 422 Validation Errors
==========================
Test finance endpoints to identify validation issues
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_vendor_creation():
    """Test basic vendor creation"""
    print("🧪 Testing Vendor Creation...")
    
    vendor_data = {
        "name": "Test Vendor",
        "representative_name": "John Doe",
        "email": "john@testvendor.com",
        "phone": "555-0123",
        "business_type": "Material Supplier",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/finance/vendors/", json=vendor_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            print("❌ Validation Error Details:")
            error_detail = response.json()
            print(json.dumps(error_detail, indent=2))
        elif response.status_code in [200, 201]:
            print("✅ Vendor created successfully:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_change_order_creation():
    """Test change order creation"""
    print("\n🧪 Testing Change Order Creation...")
    
    # First, let's check if we have any tasks
    try:
        tasks_response = requests.get(f"{BASE_URL}/tasks/")
        if tasks_response.status_code == 200:
            tasks = tasks_response.json()
            if tasks:
                task_id = tasks[0]['id']
                print(f"Using task ID: {task_id}")
            else:
                print("❌ No tasks found - creating with task ID 1")
                task_id = 1
        else:
            print("❌ Cannot fetch tasks - using task ID 1")
            task_id = 1
    except:
        print("❌ Exception fetching tasks - using task ID 1")
        task_id = 1
    
    change_order_data = {
        "co_number": "CO-TEST-001",
        "task_id": task_id,
        "title": "Test Change Order",
        "description": "This is a test change order",
        "reason": "Client Request",
        "status": "Draft",
        "created_by": 1,
        "notes": "Test notes"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/finance/change-orders/", json=change_order_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            print("❌ Validation Error Details:")
            error_detail = response.json()
            print(json.dumps(error_detail, indent=2))
        elif response.status_code in [200, 201]:
            print("✅ Change Order created successfully:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_purchase_order_creation():
    """Test purchase order creation"""
    print("\n🧪 Testing Purchase Order Creation...")
    
    # Create a vendor first
    vendor_data = {
        "name": "PO Test Vendor",
        "business_type": "Material Supplier",
        "is_active": True
    }
    
    vendor_response = requests.post(f"{BASE_URL}/finance/vendors/", json=vendor_data)
    
    if vendor_response.status_code in [200, 201]:
        vendor_id = vendor_response.json()['id']
    else:
        vendor_id = 1  # Use existing vendor
    
    po_data = {
        "po_number": "PO-TEST-001",
        "task_id": 1,
        "vendor_id": vendor_id,
        "description": "Test purchase order",
        "status": "Draft",
        "created_by": 1,
        "notes": "Test PO notes"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/finance/purchase-orders/", json=po_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            print("❌ Validation Error Details:")
            error_detail = response.json()
            print(json.dumps(error_detail, indent=2))
        elif response.status_code in [200, 201]:
            print("✅ Purchase Order created successfully:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_server_health():
    """Test if server is running"""
    print("🏥 Testing Server Health...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting 422 Error Debugging...")
    
    if test_server_health():
        test_vendor_creation()
        test_change_order_creation()
        test_purchase_order_creation()
    else:
        print("❌ Server is not running. Please start it first.")
    
    print("\n🎯 Debugging completed!")