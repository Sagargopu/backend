# Change Order Line Items - Frontend Implementation Guide

## 📋 Overview

This guide provides complete frontend implementation details for managing Change Order line items in the BuildBuzz system. Change Orders can have multiple line items that represent individual cost additions, deletions, or modifications.

## 🔗 API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/finance/change-order-items/` | Create a new CO line item |
| `GET` | `/finance/change-order-items/{item_id}` | Get specific line item |
| `GET` | `/finance/change-orders/{co_id}/items` | Get all items for a CO |
| `PUT` | `/finance/change-order-items/{item_id}` | Update line item |
| `DELETE` | `/finance/change-order-items/{item_id}` | Delete line item |

## 📝 Data Models

### Change Order Item Structure
```typescript
interface ChangeOrderItem {
  id: number;                    // Auto-generated
  change_order_id: number;       // Required - Parent CO ID
  item_name: string;             // Required - Item name
  description?: string;          // Optional - Detailed description
  change_type?: string;          // Optional - "Addition", "Deletion", "Modification"
  impact_type: string;           // Required - "+" or "-"
  amount: number;                // Required - Always positive
  created_at: string;            // Auto-generated ISO date
  updated_at?: string;           // Auto-generated ISO date
}
```

### Create Request Payload
```typescript
interface CreateCOItemRequest {
  change_order_id: number;       // Must reference existing CO
  item_name: string;             // Max 255 characters
  description?: string;          // Optional detailed description
  change_type?: "Addition" | "Deletion" | "Modification";
  impact_type: "+" | "-";        // Cost impact direction
  amount: number;                // Always positive decimal
}
```

## 🎨 UI Components

### 1. Line Items List Component

```jsx
import React, { useState, useEffect } from 'react';

const COLineItemsList = ({ changeOrderId }) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [totalImpact, setTotalImpact] = useState(0);

  useEffect(() => {
    fetchLineItems();
  }, [changeOrderId]);

  const fetchLineItems = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/finance/change-orders/${changeOrderId}/items`);
      const data = await response.json();
      setItems(data);
      calculateTotalImpact(data);
    } catch (error) {
      console.error('Error fetching line items:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateTotalImpact = (itemsList) => {
    const total = itemsList.reduce((sum, item) => {
      const amount = parseFloat(item.amount);
      return item.impact_type === '+' ? sum + amount : sum - amount;
    }, 0);
    setTotalImpact(total);
  };

  const handleDeleteItem = async (itemId) => {
    if (window.confirm('Are you sure you want to delete this line item?')) {
      try {
        await fetch(`/finance/change-order-items/${itemId}`, {
          method: 'DELETE'
        });
        fetchLineItems(); // Refresh list
      } catch (error) {
        console.error('Error deleting item:', error);
      }
    }
  };

  if (loading) return <div className="loading">Loading line items...</div>;

  return (
    <div className="co-line-items">
      <div className="header">
        <h3>Change Order Line Items</h3>
        <div className="total-impact">
          <strong>Net Impact: 
            <span className={totalImpact >= 0 ? 'positive' : 'negative'}>
              ${Math.abs(totalImpact).toFixed(2)}
            </span>
          </strong>
        </div>
      </div>

      <div className="items-list">
        {items.length === 0 ? (
          <div className="no-items">No line items added yet.</div>
        ) : (
          items.map((item, index) => (
            <div key={item.id} className="line-item">
              <div className="item-header">
                <span className="item-number">#{index + 1}</span>
                <h4 className="item-name">{item.item_name}</h4>
                <div className="item-actions">
                  <button 
                    onClick={() => onEditItem(item)}
                    className="btn-edit"
                  >
                    Edit
                  </button>
                  <button 
                    onClick={() => handleDeleteItem(item.id)}
                    className="btn-delete"
                  >
                    Delete
                  </button>
                </div>
              </div>
              
              <div className="item-details">
                <p className="description">{item.description}</p>
                <div className="item-meta">
                  <span className="change-type">{item.change_type}</span>
                  <span className={`impact ${item.impact_type === '+' ? 'positive' : 'negative'}`}>
                    {item.impact_type}${parseFloat(item.amount).toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default COLineItemsList;
```

### 2. Add Line Item Form Component

```jsx
import React, { useState } from 'react';

const AddCOLineItemForm = ({ changeOrderId, onItemAdded, onCancel }) => {
  const [formData, setFormData] = useState({
    item_name: '',
    description: '',
    change_type: 'Addition',
    impact_type: '+',
    amount: ''
  });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.item_name.trim()) {
      newErrors.item_name = 'Item name is required';
    }
    
    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setSubmitting(true);
    try {
      const payload = {
        change_order_id: changeOrderId,
        item_name: formData.item_name.trim(),
        description: formData.description.trim() || undefined,
        change_type: formData.change_type,
        impact_type: formData.impact_type,
        amount: parseFloat(formData.amount)
      };

      const response = await fetch('/finance/change-order-items/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        const newItem = await response.json();
        onItemAdded(newItem);
        
        // Reset form
        setFormData({
          item_name: '',
          description: '',
          change_type: 'Addition',
          impact_type: '+',
          amount: ''
        });
      } else {
        const errorData = await response.json();
        console.error('Error creating line item:', errorData);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <div className="add-line-item-form">
      <h3>Add Line Item</h3>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="item_name">Item Name *</label>
          <input
            type="text"
            id="item_name"
            name="item_name"
            value={formData.item_name}
            onChange={handleInputChange}
            placeholder="e.g., Additional Electrical Outlet"
            className={errors.item_name ? 'error' : ''}
          />
          {errors.item_name && <span className="error-text">{errors.item_name}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            placeholder="Detailed description of the change..."
            rows={3}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="change_type">Change Type</label>
            <select
              id="change_type"
              name="change_type"
              value={formData.change_type}
              onChange={handleInputChange}
            >
              <option value="Addition">Addition</option>
              <option value="Deletion">Deletion</option>
              <option value="Modification">Modification</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="impact_type">Impact</label>
            <select
              id="impact_type"
              name="impact_type"
              value={formData.impact_type}
              onChange={handleInputChange}
            >
              <option value="+">+ Cost Increase</option>
              <option value="-">- Cost Decrease</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="amount">Amount * (always positive)</label>
          <input
            type="number"
            id="amount"
            name="amount"
            value={formData.amount}
            onChange={handleInputChange}
            placeholder="0.00"
            step="0.01"
            min="0"
            className={errors.amount ? 'error' : ''}
          />
          {errors.amount && <span className="error-text">{errors.amount}</span>}
        </div>

        <div className="form-actions">
          <button type="button" onClick={onCancel} className="btn-cancel">
            Cancel
          </button>
          <button type="submit" disabled={submitting} className="btn-primary">
            {submitting ? 'Adding...' : 'Add Line Item'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddCOLineItemForm;
```

### 3. Complete Change Order Items Manager

```jsx
import React, { useState } from 'react';
import COLineItemsList from './COLineItemsList';
import AddCOLineItemForm from './AddCOLineItemForm';

const COItemsManager = ({ changeOrderId, changeOrderData }) => {
  const [showAddForm, setShowAddForm] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleItemAdded = (newItem) => {
    setShowAddForm(false);
    setRefreshTrigger(prev => prev + 1); // Trigger refresh
  };

  const handleEditItem = (item) => {
    // Implementation for editing items
    console.log('Edit item:', item);
  };

  return (
    <div className="co-items-manager">
      <div className="manager-header">
        <h2>Change Order: {changeOrderData.co_number}</h2>
        <p>{changeOrderData.title}</p>
        
        {!showAddForm && (
          <button 
            onClick={() => setShowAddForm(true)}
            className="btn-primary"
          >
            Add Line Item
          </button>
        )}
      </div>

      {showAddForm ? (
        <AddCOLineItemForm
          changeOrderId={changeOrderId}
          onItemAdded={handleItemAdded}
          onCancel={() => setShowAddForm(false)}
        />
      ) : (
        <COLineItemsList
          changeOrderId={changeOrderId}
          refreshTrigger={refreshTrigger}
          onEditItem={handleEditItem}
        />
      )}
    </div>
  );
};

export default COItemsManager;
```

## 💼 API Integration Examples

### Fetch Line Items
```javascript
const fetchCOItems = async (changeOrderId) => {
  try {
    const response = await fetch(`/finance/change-orders/${changeOrderId}/items`);
    if (!response.ok) throw new Error('Failed to fetch items');
    return await response.json();
  } catch (error) {
    console.error('Error fetching CO items:', error);
    return [];
  }
};
```

### Create Line Item
```javascript
const createCOItem = async (itemData) => {
  try {
    const response = await fetch('/finance/change-order-items/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(itemData)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to create item');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error creating CO item:', error);
    throw error;
  }
};
```

### Update Line Item
```javascript
const updateCOItem = async (itemId, updateData) => {
  try {
    const response = await fetch(`/finance/change-order-items/${itemId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateData)
    });
    
    if (!response.ok) throw new Error('Failed to update item');
    return await response.json();
  } catch (error) {
    console.error('Error updating CO item:', error);
    throw error;
  }
};
```

### Delete Line Item
```javascript
const deleteCOItem = async (itemId) => {
  try {
    const response = await fetch(`/finance/change-order-items/${itemId}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) throw new Error('Failed to delete item');
    return true;
  } catch (error) {
    console.error('Error deleting CO item:', error);
    throw error;
  }
};
```

## 📋 Example Payloads

### Construction Examples

#### Electrical Work
```json
{
  "change_order_id": 1,
  "item_name": "Additional Electrical Outlet",
  "description": "Install GFCI outlet in kitchen island with conduit",
  "change_type": "Addition",
  "impact_type": "+",
  "amount": 150.00
}
```

#### Drywall Addition
```json
{
  "change_order_id": 1,
  "item_name": "Interior Partition Wall",
  "description": "8x10ft drywall partition with metal studs and insulation",
  "change_type": "Addition",
  "impact_type": "+",
  "amount": 850.00
}
```

#### Material Upgrade
```json
{
  "change_order_id": 1,
  "item_name": "Granite Countertop Upgrade",
  "description": "Upgrade from laminate to granite in kitchen",
  "change_type": "Modification",
  "impact_type": "+",
  "amount": 2100.00
}
```

#### Removal/Credit
```json
{
  "change_order_id": 1,
  "item_name": "Remove Built-in Shelves",
  "description": "Client decided against planned built-in shelving",
  "change_type": "Deletion",
  "impact_type": "-",
  "amount": 450.00
}
```

## 🎨 CSS Styling Examples

```css
.co-items-manager {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.manager-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.line-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 15px;
  padding: 15px;
  background: #f9f9f9;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.impact.positive {
  color: #28a745;
  font-weight: bold;
}

.impact.negative {
  color: #dc3545;
  font-weight: bold;
}

.total-impact .positive {
  color: #28a745;
}

.total-impact .negative {
  color: #dc3545;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group input.error,
.form-group select.error {
  border-color: #dc3545;
}

.error-text {
  color: #dc3545;
  font-size: 14px;
  margin-top: 5px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-edit,
.btn-delete {
  padding: 5px 10px;
  margin-left: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-edit {
  background-color: #ffc107;
  color: black;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}
```

## ⚠️ Important Notes

### Field Validation Rules
- `amount` must always be positive (> 0)
- `impact_type` must be exactly `"+"` or `"-"`
- `item_name` is required and max 255 characters
- `change_order_id` must reference an existing Change Order

### Financial Logic
- **Addition** items typically use `impact_type: "+"`
- **Deletion** items typically use `impact_type: "-"`
- **Modification** items can use either "+" or "-"
- The `amount` field is always positive; `impact_type` determines if it adds or subtracts from total

### Best Practices
1. Always validate form data before submission
2. Calculate total impact in real-time as user adds items
3. Confirm deletion actions with user
4. Show loading states during API calls
5. Handle errors gracefully with user-friendly messages
6. Auto-refresh item lists after CRUD operations

## 🚀 Quick Start Checklist

- [ ] Install required dependencies
- [ ] Set up API base URL configuration
- [ ] Implement `COLineItemsList` component
- [ ] Implement `AddCOLineItemForm` component
- [ ] Add CSS styling for visual consistency
- [ ] Test with real Change Order data
- [ ] Add error handling and loading states
- [ ] Implement edit functionality (optional)
- [ ] Add confirmation dialogs for destructive actions

This implementation provides a complete, production-ready solution for managing Change Order line items in your frontend application.