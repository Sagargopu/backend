#!/usr/bin/env python3
"""
Test User-Based Finance Endpoints
=================================
Test the new endpoints for getting change orders and purchase orders by user (creator/approver)
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_change_orders_by_creator():
    """Test getting change orders by creator"""
    print("🧪 Testing Change Orders by Creator...")
    
    # Test with user ID 1 (we used created_by: 1 in our test data)
    creator_id = 1
    
    try:
        response = requests.get(f"{BASE_URL}/finance/change-orders/by-creator/{creator_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            cos = response.json()
            print(f"✅ Found {len(cos)} change orders created by user {creator_id}")
            
            for i, co in enumerate(cos, 1):
                print(f"   {i}. {co['co_number']} - {co['title']}")
                print(f"      Created by: {co['created_by']} | Status: {co['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_change_orders_by_approver():
    """Test getting change orders by approver"""
    print("\n🧪 Testing Change Orders by Approver...")
    
    # Test with approver ID (most COs won't have approver yet)
    approver_id = 1
    
    try:
        response = requests.get(f"{BASE_URL}/finance/change-orders/by-approver/{approver_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            cos = response.json()
            print(f"✅ Found {len(cos)} change orders approved by user {approver_id}")
            
            for i, co in enumerate(cos, 1):
                print(f"   {i}. {co['co_number']} - {co['title']}")
                print(f"      Approved by: {co['approved_by']} | Status: {co['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_purchase_orders_by_creator():
    """Test getting purchase orders by creator"""
    print("\n🧪 Testing Purchase Orders by Creator...")
    
    creator_id = 1
    
    try:
        response = requests.get(f"{BASE_URL}/finance/purchase-orders/by-creator/{creator_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            pos = response.json()
            print(f"✅ Found {len(pos)} purchase orders created by user {creator_id}")
            
            for i, po in enumerate(pos, 1):
                print(f"   {i}. {po['po_number']} - {po['description']}")
                print(f"      Created by: {po['created_by']} | Status: {po['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_purchase_orders_by_approver():
    """Test getting purchase orders by approver"""
    print("\n🧪 Testing Purchase Orders by Approver...")
    
    approver_id = 1
    
    try:
        response = requests.get(f"{BASE_URL}/finance/purchase-orders/by-approver/{approver_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            pos = response.json()
            print(f"✅ Found {len(pos)} purchase orders approved by user {approver_id}")
            
            for i, po in enumerate(pos, 1):
                print(f"   {i}. {po['po_number']} - {po['description']}")
                print(f"      Approved by: {po['approved_by']} | Status: {po['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def get_users_with_finance_activity():
    """Get users who have finance activity"""
    print("\n🔍 Finding Users with Finance Activity...")
    
    try:
        # Get all change orders to see who created them
        co_response = requests.get(f"{BASE_URL}/finance/change-orders/")
        if co_response.status_code == 200:
            cos = co_response.json()
            creators = set()
            approvers = set()
            
            for co in cos:
                creators.add(co['created_by'])
                if co.get('approved_by'):
                    approvers.add(co['approved_by'])
            
            print(f"📋 Change Order Creators: {sorted(creators)}")
            print(f"📋 Change Order Approvers: {sorted(approvers)}")
        
        # Get all purchase orders to see who created them
        po_response = requests.get(f"{BASE_URL}/finance/purchase-orders/")
        if po_response.status_code == 200:
            pos = po_response.json()
            po_creators = set()
            po_approvers = set()
            
            for po in pos:
                po_creators.add(po['created_by'])
                if po.get('approved_by'):
                    po_approvers.add(po['approved_by'])
            
            print(f"📦 Purchase Order Creators: {sorted(po_creators)}")
            print(f"📦 Purchase Order Approvers: {sorted(po_approvers)}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def create_approved_co_for_testing():
    """Create a change order with approval for testing"""
    print("\n🛠️ Creating Approved CO for Testing...")
    
    # Create a new CO
    co_data = {
        "task_id": 1,
        "title": "Test CO with Approval",
        "description": "Testing CO approval workflow",
        "reason": "Testing",
        "created_by": 1
    }
    
    try:
        create_response = requests.post(f"{BASE_URL}/finance/change-orders/", json=co_data)
        if create_response.status_code in [200, 201]:
            co = create_response.json()
            co_id = co['id']
            print(f"✅ Created CO: {co['co_number']}")
            
            # Update it with approval
            update_data = {
                "status": "Approved",
                "approved_by": 2,  # Different user as approver
                "approved_date": "2025-10-16T12:00:00"
            }
            
            update_response = requests.put(f"{BASE_URL}/finance/change-orders/{co_id}", json=update_data)
            if update_response.status_code == 200:
                updated_co = update_response.json()
                print(f"✅ Approved CO: {updated_co['co_number']} by user {updated_co['approved_by']}")
                return updated_co
            else:
                print(f"❌ Failed to approve CO: {update_response.status_code}")
        else:
            print(f"❌ Failed to create CO: {create_response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

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
    print("🚀 Testing User-Based Finance Endpoints...")
    
    if test_server_health():
        get_users_with_finance_activity()
        
        # Create approved CO for testing
        create_approved_co_for_testing()
        
        # Test all endpoints
        test_change_orders_by_creator()
        test_change_orders_by_approver()
        test_purchase_orders_by_creator()
        test_purchase_orders_by_approver()
    else:
        print("❌ Server is not running. Please start it first.")
    
    print("\n🎯 User-based endpoint testing completed!")