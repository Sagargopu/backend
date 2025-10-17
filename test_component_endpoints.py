#!/usr/bin/env python3
"""
Test Component-Based Finance Endpoints
=====================================
Test the new endpoints for getting change orders and purchase orders by component
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_change_orders_by_component():
    """Test getting change orders by component"""
    print("🧪 Testing Change Orders by Component...")
    
    # Test with component 1 (we created tasks for components 1-6)
    component_id = 1
    
    try:
        response = requests.get(f"{BASE_URL}/finance/change-orders/by-component/{component_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            cos = response.json()
            print(f"✅ Found {len(cos)} change orders for component {component_id}")
            
            for i, co in enumerate(cos, 1):
                print(f"   {i}. {co['co_number']} - {co['title']}")
                print(f"      Task ID: {co['task_id']} | Status: {co['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_purchase_orders_by_component():
    """Test getting purchase orders by component"""
    print("\n🧪 Testing Purchase Orders by Component...")
    
    # Test with component 1
    component_id = 1
    
    try:
        response = requests.get(f"{BASE_URL}/finance/purchase-orders/by-component/{component_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            pos = response.json()
            print(f"✅ Found {len(pos)} purchase orders for component {component_id}")
            
            for i, po in enumerate(pos, 1):
                print(f"   {i}. {po['po_number']} - {po['description']}")
                print(f"      Task ID: {po['task_id']} | Status: {po['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def create_test_data():
    """Create some test change orders and purchase orders for different components"""
    print("\n🛠️ Creating Test Data...")
    
    # Create change orders for different components (via their tasks)
    test_cos = [
        {"task_id": 1, "title": "CO for Component 1 Task", "description": "Test CO for component 1", "created_by": 1},
        {"task_id": 12, "title": "CO for Component 2 Task", "description": "Test CO for component 2", "created_by": 1},
        {"task_id": 22, "title": "CO for Component 3 Task", "description": "Test CO for component 3", "created_by": 1},
    ]
    
    print("📋 Creating Change Orders:")
    for i, co_data in enumerate(test_cos, 1):
        response = requests.post(f"{BASE_URL}/finance/change-orders/", json=co_data)
        if response.status_code in [200, 201]:
            co = response.json()
            print(f"   ✅ {co['co_number']} for task {co_data['task_id']}")
        else:
            print(f"   ❌ Failed for task {co_data['task_id']}: {response.status_code}")
    
    # Create purchase orders for different components
    test_pos = [
        {"task_id": 1, "vendor_id": 1, "description": "PO for Component 1 Task", "created_by": 1},
        {"task_id": 12, "vendor_id": 1, "description": "PO for Component 2 Task", "created_by": 1},
        {"task_id": 22, "vendor_id": 1, "description": "PO for Component 3 Task", "created_by": 1},
    ]
    
    print("\n📦 Creating Purchase Orders:")
    for i, po_data in enumerate(test_pos, 1):
        response = requests.post(f"{BASE_URL}/finance/purchase-orders/", json=po_data)
        if response.status_code in [200, 201]:
            po = response.json()
            print(f"   ✅ {po['po_number']} for task {po_data['task_id']}")
        else:
            print(f"   ❌ Failed for task {po_data['task_id']}: {response.status_code}")

def test_all_components():
    """Test the new endpoints for all components"""
    print("\n🔍 Testing All Components (1-6)...")
    
    for component_id in range(1, 7):
        print(f"\n📂 Component {component_id}:")
        
        # Test change orders
        co_response = requests.get(f"{BASE_URL}/finance/change-orders/by-component/{component_id}")
        if co_response.status_code == 200:
            cos = co_response.json()
            print(f"   📋 Change Orders: {len(cos)}")
        else:
            print(f"   📋 Change Orders: Error {co_response.status_code}")
        
        # Test purchase orders
        po_response = requests.get(f"{BASE_URL}/finance/purchase-orders/by-component/{component_id}")
        if po_response.status_code == 200:
            pos = po_response.json()
            print(f"   📦 Purchase Orders: {len(pos)}")
        else:
            print(f"   📦 Purchase Orders: Error {po_response.status_code}")

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
    print("🚀 Testing Component-Based Finance Endpoints...")
    
    if test_server_health():
        create_test_data()
        test_change_orders_by_component()
        test_purchase_orders_by_component()
        test_all_components()
    else:
        print("❌ Server is not running. Please start it first.")
    
    print("\n🎯 Component endpoint testing completed!")