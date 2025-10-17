#!/usr/bin/env python3
"""
Test Change Order Items Creation
===============================
Test adding multiple line items to change orders
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def add_co_items_example():
    """Add multiple items to a change order"""
    print("🧪 Adding Change Order Items...")
    
    # Use the first change order we created
    change_order_id = 1
    
    # Sample CO items with different types
    co_items = [
        {
            "change_order_id": change_order_id,
            "item_name": "Drywall Partition - 8x10ft",
            "description": "New drywall partition with metal studs and insulation",
            "change_type": "Addition",
            "impact_type": "+",
            "amount": 850.00
        },
        {
            "change_order_id": change_order_id,
            "item_name": "Electrical Outlet Installation",
            "description": "Install 2 GFCI outlets with conduit and wiring",
            "change_type": "Addition", 
            "impact_type": "+",
            "amount": 275.00
        },
        {
            "change_order_id": change_order_id,
            "item_name": "Paint and Finish",
            "description": "Prime and paint new partition to match existing",
            "change_type": "Addition",
            "impact_type": "+",
            "amount": 180.00
        },
        {
            "change_order_id": change_order_id,
            "item_name": "Remove Existing Cabinet",
            "description": "Remove old wall cabinet that conflicts with new partition",
            "change_type": "Deletion",
            "impact_type": "-",
            "amount": 125.00
        },
        {
            "change_order_id": change_order_id,
            "item_name": "Modified Door Frame",
            "description": "Modify existing door frame to accommodate new wall",
            "change_type": "Modification",
            "impact_type": "+",
            "amount": 320.00
        }
    ]
    
    created_items = []
    failed_items = []
    
    print(f"📋 Adding {len(co_items)} items to Change Order {change_order_id}:")
    print()
    
    for i, item_data in enumerate(co_items, 1):
        print(f"   Item {i}: {item_data['item_name']}")
        print(f"   Type: {item_data['change_type']} | Impact: {item_data['impact_type']} | Amount: ${item_data['amount']:.2f}")
        
        try:
            response = requests.post(f"{BASE_URL}/finance/change-order-items/", json=item_data)
            
            if response.status_code in [200, 201]:
                created_item = response.json()
                created_items.append(created_item)
                print(f"   ✅ Created! Item ID: {created_item['id']}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                if response.status_code == 422:
                    error_detail = response.json()
                    print(f"   📋 Error Details: {error_detail}")
                failed_items.append(item_data)
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            failed_items.append(item_data)
        
        print()
    
    # Summary
    print("=" * 50)
    print("📊 Summary:")
    print(f"✅ Created Items: {len(created_items)}")
    print(f"❌ Failed Items: {len(failed_items)}")
    
    if created_items:
        total_positive = sum(item['amount'] for item in created_items if item['impact_type'] == '+')
        total_negative = sum(item['amount'] for item in created_items if item['impact_type'] == '-')
        net_impact = total_positive - total_negative
        
        print(f"💰 Total Additions: ${total_positive:.2f}")
        print(f"💰 Total Deductions: ${total_negative:.2f}")
        print(f"💰 Net Change: ${net_impact:.2f}")
    
    return created_items

def get_co_items(change_order_id):
    """Get all items for a change order"""
    print(f"\n🔍 Getting items for Change Order {change_order_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/finance/change-orders/{change_order_id}/items")
        
        if response.status_code == 200:
            items = response.json()
            print(f"✅ Found {len(items)} items:")
            
            total_positive = 0
            total_negative = 0
            
            for i, item in enumerate(items, 1):
                impact_symbol = "+" if item['impact_type'] == '+' else "-"
                print(f"   {i}. {item['item_name']}")
                print(f"      {item['change_type']} | {impact_symbol}${item['amount']:.2f}")
                print(f"      Description: {item['description']}")
                
                if item['impact_type'] == '+':
                    total_positive += float(item['amount'])
                else:
                    total_negative += float(item['amount'])
                print()
            
            net_change = total_positive - total_negative
            print(f"💰 Net Change Impact: ${net_change:.2f}")
            
            return items
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return []

def test_individual_item_creation():
    """Test creating a single CO item"""
    print("\n🧪 Testing Single CO Item Creation...")
    
    single_item = {
        "change_order_id": 2,
        "item_name": "Emergency Exit Sign",
        "description": "Install LED emergency exit sign per code requirement",
        "change_type": "Addition",
        "impact_type": "+",
        "amount": 89.50
    }
    
    try:
        response = requests.post(f"{BASE_URL}/finance/change-order-items/", json=single_item)
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            item = response.json()
            print("✅ Single item created successfully:")
            print(f"   ID: {item['id']}")
            print(f"   Name: {item['item_name']}")
            print(f"   Impact: {item['impact_type']}${item['amount']}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🚀 Testing Change Order Items...")
    
    # Test adding multiple items
    created_items = add_co_items_example()
    
    if created_items:
        # Get items back to verify
        get_co_items(1)
    
    # Test single item creation
    test_individual_item_creation()
    
    print("\n🎯 CO Items testing completed!")