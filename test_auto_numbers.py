#!/usr/bin/env python3
"""
Test Auto-Generated CO/PO Numbers
================================
Test the updated Change Order and Purchase Order creation with auto-generated numbers
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_change_order_creation():
    """Test change order creation with auto-generated CO number"""
    print("🧪 Testing Change Order Creation (Auto CO Number)...")
    
    change_order_data = {
        "task_id": 1,
        "title": "Test Auto-Generated CO",
        "description": "Testing auto-generated CO number functionality",
        "reason": "Client Request",
        "status": "Draft",
        "created_by": 1,
        "notes": "Auto-generated CO number test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/finance/change-orders/", json=change_order_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            print("❌ Validation Error Details:")
            error_detail = response.json()
            print(json.dumps(error_detail, indent=2))
        elif response.status_code in [200, 201]:
            created_co = response.json()
            print("✅ Change Order created successfully:")
            print(f"   ID: {created_co['id']}")
            print(f"   CO Number: {created_co['co_number']}")
            print(f"   Title: {created_co['title']}")
            print(f"   Status: {created_co['status']}")
            return created_co
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def test_purchase_order_creation():
    """Test purchase order creation with auto-generated PO number"""
    print("\n🧪 Testing Purchase Order Creation (Auto PO Number)...")
    
    # First create a vendor
    vendor_data = {
        "name": "Auto-Test Vendor",
        "business_type": "Material Supplier",
        "is_active": True
    }
    
    vendor_response = requests.post(f"{BASE_URL}/finance/vendors/", json=vendor_data)
    
    if vendor_response.status_code in [200, 201]:
        vendor_id = vendor_response.json()['id']
        print(f"   Created vendor with ID: {vendor_id}")
    else:
        vendor_id = 1  # Use existing vendor
        print(f"   Using existing vendor ID: {vendor_id}")
    
    purchase_order_data = {
        "task_id": 1,
        "vendor_id": vendor_id,
        "description": "Testing auto-generated PO number functionality",
        "status": "Draft",
        "created_by": 1,
        "notes": "Auto-generated PO number test"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/finance/purchase-orders/", json=purchase_order_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 422:
            print("❌ Validation Error Details:")
            error_detail = response.json()
            print(json.dumps(error_detail, indent=2))
        elif response.status_code in [200, 201]:
            created_po = response.json()
            print("✅ Purchase Order created successfully:")
            print(f"   ID: {created_po['id']}")
            print(f"   PO Number: {created_po['po_number']}")
            print(f"   Description: {created_po['description']}")
            print(f"   Status: {created_po['status']}")
            return created_po
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def test_multiple_creations():
    """Test creating multiple COs and POs to verify number incrementing"""
    print("\n🧪 Testing Multiple Creations (Number Incrementing)...")
    
    # Create 3 change orders
    print("\n📋 Creating 3 Change Orders:")
    for i in range(1, 4):
        co_data = {
            "task_id": 1,
            "title": f"Test CO #{i}",
            "description": f"Testing CO number sequence #{i}",
            "reason": "Testing",
            "created_by": 1
        }
        
        response = requests.post(f"{BASE_URL}/finance/change-orders/", json=co_data)
        if response.status_code in [200, 201]:
            co = response.json()
            print(f"   CO #{i}: {co['co_number']}")
        else:
            print(f"   CO #{i}: Failed ({response.status_code})")
    
    # Create 3 purchase orders
    print("\n📋 Creating 3 Purchase Orders:")
    for i in range(1, 4):
        po_data = {
            "task_id": 1,
            "vendor_id": 1,
            "description": f"Testing PO number sequence #{i}",
            "created_by": 1
        }
        
        response = requests.post(f"{BASE_URL}/finance/purchase-orders/", json=po_data)
        if response.status_code in [200, 201]:
            po = response.json()
            print(f"   PO #{i}: {po['po_number']}")
        else:
            print(f"   PO #{i}: Failed ({response.status_code})")

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
    print("🚀 Testing Auto-Generated Numbers...")
    
    if test_server_health():
        test_change_order_creation()
        test_purchase_order_creation()
        test_multiple_creations()
    else:
        print("❌ Server is not running. Please start it first.")
    
    print("\n🎯 Auto-generation testing completed!")