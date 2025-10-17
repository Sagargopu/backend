# Frontend Implementation Guide: Change Order Approvals & Transaction Management

## Overview
This guide provides a complete implementation for handling Change Order (CO) approvals, rejections, and transaction management in your React frontend. The backend automatically creates transactions and updates budgets when COs are approved.

## Table of Contents
1. [API Endpoints Overview](#api-endpoints-overview)
2. [React Components](#react-components)
3. [State Management](#state-management)
4. [Approval Workflow](#approval-workflow)
5. [Transaction Management](#transaction-management)
6. [Error Handling](#error-handling)
7. [UI/UX Examples](#uiux-examples)

---

## API Endpoints Overview

### Change Order Endpoints
```javascript
// Get all change orders
GET /finance/change-orders/

// Get change order by ID
GET /finance/change-orders/{id}

// Update change order (for approvals/rejections)
PUT /finance/change-orders/{id}

// Get change orders by component
GET /finance/change-orders/by-component/{component_id}

// Get change orders by creator
GET /finance/change-orders/by-creator/{user_id}

// Get change orders by approver
GET /finance/change-orders/by-approver/{user_id}
```

### Transaction Endpoints
```javascript
// Get all transactions (when implemented)
GET /finance/transactions/

// Get transactions by project
GET /finance/transactions/?project_id={project_id}

// Get transactions by task
GET /finance/transactions/?task_id={task_id}
```

---

## React Components

### 1. Change Order Approval Component

```jsx
// components/ChangeOrderApproval.jsx
import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';

const ChangeOrderApproval = ({ changeOrder, onUpdate, currentUser }) => {
    const [loading, setLoading] = useState(false);
    const [showApprovalModal, setShowApprovalModal] = useState(false);
    const [approvalNote, setApprovalNote] = useState('');
    const [budgetImpact, setBudgetImpact] = useState(0);

    useEffect(() => {
        // Calculate budget impact from CO items
        if (changeOrder?.items) {
            const impact = changeOrder.items.reduce((sum, item) => {
                const amount = parseFloat(item.amount) || 0;
                return sum + (item.impact_type === '+' ? amount : -amount);
            }, 0);
            setBudgetImpact(impact);
        }
    }, [changeOrder]);

    const handleApproval = async (status, note = '') => {
        setLoading(true);
        try {
            const response = await fetch(`/api/finance/change-orders/${changeOrder.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    status: status,
                    approved_by: status === 'Approved' ? currentUser.id : null,
                    approved_date: status === 'Approved' ? new Date().toISOString() : null,
                    notes: note
                })
            });

            if (response.ok) {
                const updatedCO = await response.json();
                
                if (status === 'Approved') {
                    toast.success(`Change Order approved! Budget ${budgetImpact >= 0 ? 'increased' : 'decreased'} by $${Math.abs(budgetImpact).toFixed(2)}`);
                } else {
                    toast.success('Change Order rejected');
                }
                
                onUpdate(updatedCO);
                setShowApprovalModal(false);
            } else {
                const error = await response.json();
                toast.error(error.detail || 'Failed to update Change Order');
            }
        } catch (error) {
            toast.error('Network error occurred');
        } finally {
            setLoading(false);
        }
    };

    const canApprove = () => {
        return changeOrder.status === 'Pending Approval' && 
               currentUser.role in ['project_manager', 'admin', 'finance_manager'];
    };

    return (
        <div className="change-order-approval">
            <div className="co-header">
                <h3>{changeOrder.co_number}: {changeOrder.title}</h3>
                <span className={`status-badge ${changeOrder.status.toLowerCase().replace(' ', '-')}`}>
                    {changeOrder.status}
                </span>
            </div>

            <div className="co-details">
                <p><strong>Description:</strong> {changeOrder.description}</p>
                <p><strong>Reason:</strong> {changeOrder.reason}</p>
                <p><strong>Created by:</strong> {changeOrder.creator?.name}</p>
                
                <div className="budget-impact">
                    <h4>Budget Impact:</h4>
                    <span className={`impact-amount ${budgetImpact >= 0 ? 'positive' : 'negative'}`}>
                        {budgetImpact >= 0 ? '+' : ''}${budgetImpact.toFixed(2)}
                    </span>
                </div>

                <div className="co-items">
                    <h4>Change Order Items:</h4>
                    {changeOrder.items?.map(item => (
                        <div key={item.id} className="co-item">
                            <div className="item-header">
                                <span className="item-name">{item.item_name}</span>
                                <span className={`item-amount ${item.impact_type === '+' ? 'positive' : 'negative'}`}>
                                    {item.impact_type}${item.amount}
                                </span>
                            </div>
                            <p className="item-description">{item.description}</p>
                            <small className="item-type">{item.change_type}</small>
                        </div>
                    ))}
                </div>
            </div>

            {canApprove() && (
                <div className="approval-actions">
                    <button 
                        className="btn btn-success"
                        onClick={() => setShowApprovalModal(true)}
                        disabled={loading}
                    >
                        Review for Approval
                    </button>
                    <button 
                        className="btn btn-danger"
                        onClick={() => handleApproval('Rejected', 'Rejected without review')}
                        disabled={loading}
                    >
                        Quick Reject
                    </button>
                </div>
            )}

            {/* Approval Modal */}
            {showApprovalModal && (
                <div className="modal-overlay">
                    <div className="approval-modal">
                        <h3>Review Change Order</h3>
                        
                        <div className="budget-warning">
                            {budgetImpact !== 0 && (
                                <div className={`alert ${budgetImpact > 0 ? 'alert-warning' : 'alert-info'}`}>
                                    <strong>Budget Impact:</strong> This change order will {budgetImpact > 0 ? 'increase' : 'decrease'} 
                                    the task budget by ${Math.abs(budgetImpact).toFixed(2)}
                                </div>
                            )}
                        </div>

                        <div className="form-group">
                            <label>Approval Notes (Optional):</label>
                            <textarea 
                                value={approvalNote}
                                onChange={(e) => setApprovalNote(e.target.value)}
                                placeholder="Add any notes about this approval..."
                                rows="3"
                            />
                        </div>

                        <div className="modal-actions">
                            <button 
                                className="btn btn-success"
                                onClick={() => handleApproval('Approved', approvalNote)}
                                disabled={loading}
                            >
                                {loading ? 'Processing...' : 'Approve'}
                            </button>
                            <button 
                                className="btn btn-danger"
                                onClick={() => handleApproval('Rejected', approvalNote)}
                                disabled={loading}
                            >
                                Reject
                            </button>
                            <button 
                                className="btn btn-secondary"
                                onClick={() => setShowApprovalModal(false)}
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChangeOrderApproval;
```

### 2. Transaction History Component

```jsx
// components/TransactionHistory.jsx
import React, { useState, useEffect } from 'react';

const TransactionHistory = ({ projectId, taskId }) => {
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all'); // 'all', 'change_order', 'purchase_order'

    useEffect(() => {
        fetchTransactions();
    }, [projectId, taskId, filter]);

    const fetchTransactions = async () => {
        setLoading(true);
        try {
            const params = new URLSearchParams();
            if (projectId) params.append('project_id', projectId);
            if (taskId) params.append('task_id', taskId);
            if (filter !== 'all') params.append('transaction_type', filter);

            const response = await fetch(`/api/finance/transactions/?${params}`);
            if (response.ok) {
                const data = await response.json();
                setTransactions(data);
            }
        } catch (error) {
            console.error('Failed to fetch transactions:', error);
        } finally {
            setLoading(false);
        }
    };

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    if (loading) return <div className="loading-spinner">Loading transactions...</div>;

    return (
        <div className="transaction-history">
            <div className="transaction-header">
                <h3>Transaction History</h3>
                <div className="filter-controls">
                    <select 
                        value={filter} 
                        onChange={(e) => setFilter(e.target.value)}
                        className="form-select"
                    >
                        <option value="all">All Transactions</option>
                        <option value="change_order">Change Orders</option>
                        <option value="purchase_order">Purchase Orders</option>
                    </select>
                </div>
            </div>

            {transactions.length === 0 ? (
                <div className="no-transactions">
                    <p>No transactions found for the selected criteria.</p>
                </div>
            ) : (
                <div className="transaction-list">
                    {transactions.map(transaction => (
                        <div key={transaction.id} className="transaction-item">
                            <div className="transaction-header">
                                <div className="transaction-number">
                                    <strong>{transaction.transaction_number}</strong>
                                    <span className="transaction-type">{transaction.transaction_type}</span>
                                </div>
                                <div className="transaction-date">
                                    {formatDate(transaction.approved_date)}
                                </div>
                            </div>

                            <div className="transaction-details">
                                <div className="transaction-description">
                                    <p>{transaction.description}</p>
                                    <small>Source: {transaction.source_number}</small>
                                </div>

                                <div className="transaction-impact">
                                    <span className={`amount ${transaction.impact_type === '+' ? 'positive' : 'negative'}`}>
                                        {transaction.impact_type}{formatCurrency(transaction.amount)}
                                    </span>
                                </div>
                            </div>

                            <div className="budget-change">
                                <div className="budget-flow">
                                    <span className="budget-before">
                                        {formatCurrency(transaction.budget_before)}
                                    </span>
                                    <span className="arrow">→</span>
                                    <span className="budget-after">
                                        {formatCurrency(transaction.budget_after)}
                                    </span>
                                </div>
                                <small>Budget Change</small>
                            </div>

                            <div className="transaction-meta">
                                <small>
                                    Approved by: {transaction.approver?.name} | 
                                    Created by: {transaction.creator?.name}
                                </small>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default TransactionHistory;
```

### 3. Budget Impact Dashboard

```jsx
// components/BudgetImpactDashboard.jsx
import React, { useState, useEffect } from 'react';

const BudgetImpactDashboard = ({ projectId }) => {
    const [budgetData, setBudgetData] = useState(null);
    const [pendingCOs, setPendingCOs] = useState([]);
    const [recentTransactions, setRecentTransactions] = useState([]);

    useEffect(() => {
        fetchBudgetData();
        fetchPendingCOs();
        fetchRecentTransactions();
    }, [projectId]);

    const fetchBudgetData = async () => {
        // Fetch project budget summary
        try {
            const response = await fetch(`/api/projects/${projectId}/budget-summary`);
            if (response.ok) {
                const data = await response.json();
                setBudgetData(data);
            }
        } catch (error) {
            console.error('Failed to fetch budget data:', error);
        }
    };

    const fetchPendingCOs = async () => {
        try {
            const response = await fetch(`/api/finance/change-orders/?status=Pending Approval&project_id=${projectId}`);
            if (response.ok) {
                const data = await response.json();
                setPendingCOs(data);
            }
        } catch (error) {
            console.error('Failed to fetch pending COs:', error);
        }
    };

    const fetchRecentTransactions = async () => {
        try {
            const response = await fetch(`/api/finance/transactions/?project_id=${projectId}&limit=5`);
            if (response.ok) {
                const data = await response.json();
                setRecentTransactions(data);
            }
        } catch (error) {
            console.error('Failed to fetch recent transactions:', error);
        }
    };

    const calculatePendingImpact = () => {
        return pendingCOs.reduce((sum, co) => {
            const impact = co.items?.reduce((itemSum, item) => {
                const amount = parseFloat(item.amount) || 0;
                return itemSum + (item.impact_type === '+' ? amount : -amount);
            }, 0) || 0;
            return sum + impact;
        }, 0);
    };

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    };

    const pendingImpact = calculatePendingImpact();

    return (
        <div className="budget-impact-dashboard">
            <h2>Budget Overview</h2>

            <div className="budget-cards">
                <div className="budget-card current">
                    <h3>Current Budget</h3>
                    <div className="budget-amount">
                        {budgetData ? formatCurrency(budgetData.total_budget) : 'Loading...'}
                    </div>
                    <small>Total allocated budget</small>
                </div>

                <div className="budget-card spent">
                    <h3>Budget Utilized</h3>
                    <div className="budget-amount">
                        {budgetData ? formatCurrency(budgetData.spent_budget) : 'Loading...'}
                    </div>
                    <small>
                        {budgetData ? 
                            `${((budgetData.spent_budget / budgetData.total_budget) * 100).toFixed(1)}% utilized` : 
                            ''
                        }
                    </small>
                </div>

                <div className="budget-card remaining">
                    <h3>Remaining Budget</h3>
                    <div className="budget-amount">
                        {budgetData ? formatCurrency(budgetData.remaining_budget) : 'Loading...'}
                    </div>
                    <small>Available for allocation</small>
                </div>

                {pendingImpact !== 0 && (
                    <div className="budget-card pending">
                        <h3>Pending Changes</h3>
                        <div className={`budget-amount ${pendingImpact >= 0 ? 'positive' : 'negative'}`}>
                            {pendingImpact >= 0 ? '+' : ''}{formatCurrency(pendingImpact)}
                        </div>
                        <small>{pendingCOs.length} pending approval{pendingCOs.length !== 1 ? 's' : ''}</small>
                    </div>
                )}
            </div>

            <div className="dashboard-sections">
                <div className="pending-approvals">
                    <h3>Pending Approvals ({pendingCOs.length})</h3>
                    {pendingCOs.length === 0 ? (
                        <p>No change orders pending approval.</p>
                    ) : (
                        <div className="pending-list">
                            {pendingCOs.map(co => {
                                const impact = co.items?.reduce((sum, item) => {
                                    const amount = parseFloat(item.amount) || 0;
                                    return sum + (item.impact_type === '+' ? amount : -amount);
                                }, 0) || 0;

                                return (
                                    <div key={co.id} className="pending-item">
                                        <div className="co-info">
                                            <strong>{co.co_number}</strong>
                                            <span>{co.title}</span>
                                        </div>
                                        <div className={`co-impact ${impact >= 0 ? 'positive' : 'negative'}`}>
                                            {impact >= 0 ? '+' : ''}{formatCurrency(impact)}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>

                <div className="recent-transactions">
                    <h3>Recent Transactions</h3>
                    {recentTransactions.length === 0 ? (
                        <p>No recent transactions.</p>
                    ) : (
                        <div className="transaction-summary">
                            {recentTransactions.map(txn => (
                                <div key={txn.id} className="transaction-summary-item">
                                    <div className="txn-info">
                                        <strong>{txn.transaction_number}</strong>
                                        <small>{txn.description}</small>
                                    </div>
                                    <div className={`txn-amount ${txn.impact_type === '+' ? 'positive' : 'negative'}`}>
                                        {txn.impact_type}{formatCurrency(txn.amount)}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default BudgetImpactDashboard;
```

---

## State Management

### Context Provider for Change Orders

```jsx
// context/ChangeOrderContext.jsx
import React, { createContext, useContext, useReducer, useEffect } from 'react';

const ChangeOrderContext = createContext();

const changeOrderReducer = (state, action) => {
    switch (action.type) {
        case 'SET_CHANGE_ORDERS':
            return {
                ...state,
                changeOrders: action.payload,
                loading: false
            };
        case 'UPDATE_CHANGE_ORDER':
            return {
                ...state,
                changeOrders: state.changeOrders.map(co => 
                    co.id === action.payload.id ? action.payload : co
                )
            };
        case 'ADD_CHANGE_ORDER':
            return {
                ...state,
                changeOrders: [...state.changeOrders, action.payload]
            };
        case 'SET_LOADING':
            return {
                ...state,
                loading: action.payload
            };
        case 'SET_ERROR':
            return {
                ...state,
                error: action.payload,
                loading: false
            };
        default:
            return state;
    }
};

export const ChangeOrderProvider = ({ children, projectId }) => {
    const [state, dispatch] = useReducer(changeOrderReducer, {
        changeOrders: [],
        loading: true,
        error: null
    });

    useEffect(() => {
        if (projectId) {
            fetchChangeOrders();
        }
    }, [projectId]);

    const fetchChangeOrders = async () => {
        dispatch({ type: 'SET_LOADING', payload: true });
        try {
            const response = await fetch(`/api/finance/change-orders/?project_id=${projectId}`);
            if (response.ok) {
                const data = await response.json();
                dispatch({ type: 'SET_CHANGE_ORDERS', payload: data });
            } else {
                throw new Error('Failed to fetch change orders');
            }
        } catch (error) {
            dispatch({ type: 'SET_ERROR', payload: error.message });
        }
    };

    const updateChangeOrder = (updatedCO) => {
        dispatch({ type: 'UPDATE_CHANGE_ORDER', payload: updatedCO });
    };

    const addChangeOrder = (newCO) => {
        dispatch({ type: 'ADD_CHANGE_ORDER', payload: newCO });
    };

    return (
        <ChangeOrderContext.Provider value={{
            ...state,
            updateChangeOrder,
            addChangeOrder,
            refreshChangeOrders: fetchChangeOrders
        }}>
            {children}
        </ChangeOrderContext.Provider>
    );
};

export const useChangeOrders = () => {
    const context = useContext(ChangeOrderContext);
    if (!context) {
        throw new Error('useChangeOrders must be used within a ChangeOrderProvider');
    }
    return context;
};
```

---

## Approval Workflow Implementation

### Custom Hooks for Approval Logic

```jsx
// hooks/useChangeOrderApproval.js
import { useState } from 'react';
import { toast } from 'react-toastify';

export const useChangeOrderApproval = () => {
    const [loading, setLoading] = useState(false);

    const approveChangeOrder = async (changeOrderId, approvalData) => {
        setLoading(true);
        try {
            const response = await fetch(`/api/finance/change-orders/${changeOrderId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    status: 'Approved',
                    approved_by: approvalData.userId,
                    approved_date: new Date().toISOString(),
                    notes: approvalData.notes || ''
                })
            });

            if (response.ok) {
                const updatedCO = await response.json();
                
                // Calculate budget impact for notification
                const budgetImpact = calculateBudgetImpact(updatedCO.items);
                
                toast.success(
                    `Change Order approved! ${
                        budgetImpact !== 0 
                            ? `Budget ${budgetImpact > 0 ? 'increased' : 'decreased'} by $${Math.abs(budgetImpact).toFixed(2)}` 
                            : 'No budget impact'
                    }`
                );
                
                return { success: true, data: updatedCO };
            } else {
                const error = await response.json();
                toast.error(error.detail || 'Failed to approve Change Order');
                return { success: false, error: error.detail };
            }
        } catch (error) {
            toast.error('Network error occurred');
            return { success: false, error: 'Network error' };
        } finally {
            setLoading(false);
        }
    };

    const rejectChangeOrder = async (changeOrderId, rejectionData) => {
        setLoading(true);
        try {
            const response = await fetch(`/api/finance/change-orders/${changeOrderId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    status: 'Rejected',
                    approved_by: rejectionData.userId,
                    approved_date: new Date().toISOString(),
                    notes: rejectionData.notes || ''
                })
            });

            if (response.ok) {
                const updatedCO = await response.json();
                toast.success('Change Order rejected');
                return { success: true, data: updatedCO };
            } else {
                const error = await response.json();
                toast.error(error.detail || 'Failed to reject Change Order');
                return { success: false, error: error.detail };
            }
        } catch (error) {
            toast.error('Network error occurred');
            return { success: false, error: 'Network error' };
        } finally {
            setLoading(false);
        }
    };

    const calculateBudgetImpact = (items) => {
        if (!items) return 0;
        return items.reduce((sum, item) => {
            const amount = parseFloat(item.amount) || 0;
            return sum + (item.impact_type === '+' ? amount : -amount);
        }, 0);
    };

    return {
        loading,
        approveChangeOrder,
        rejectChangeOrder,
        calculateBudgetImpact
    };
};
```

---

## Error Handling

### Error Handling Utilities

```jsx
// utils/errorHandling.js
export const handleApiError = (error, defaultMessage = 'An error occurred') => {
    if (error.response) {
        // Server responded with error status
        const status = error.response.status;
        const data = error.response.data;
        
        switch (status) {
            case 400:
                return data.detail || 'Invalid request data';
            case 401:
                return 'Unauthorized. Please log in again.';
            case 403:
                return 'You do not have permission to perform this action';
            case 404:
                return 'Change Order not found';
            case 422:
                return data.detail || 'Validation error';
            case 500:
                return 'Server error. Please try again later.';
            default:
                return data.detail || defaultMessage;
        }
    } else if (error.request) {
        // Network error
        return 'Network error. Please check your connection.';
    } else {
        // Other error
        return error.message || defaultMessage;
    }
};

export const validateChangeOrderApproval = (changeOrder, currentUser) => {
    const errors = [];
    
    if (!changeOrder) {
        errors.push('Change Order not found');
        return errors;
    }
    
    if (changeOrder.status !== 'Pending Approval') {
        errors.push('Change Order is not pending approval');
    }
    
    if (!currentUser || !['project_manager', 'admin', 'finance_manager'].includes(currentUser.role)) {
        errors.push('You do not have permission to approve Change Orders');
    }
    
    if (changeOrder.created_by === currentUser.id) {
        errors.push('You cannot approve your own Change Order');
    }
    
    return errors;
};
```

---

## CSS Styles

### Change Order Approval Styles

```css
/* styles/ChangeOrderApproval.css */
.change-order-approval {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.co-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #f0f0f0;
}

.status-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 500;
    text-transform: uppercase;
}

.status-badge.draft { background: #e3f2fd; color: #1976d2; }
.status-badge.pending-approval { background: #fff3e0; color: #f57c00; }
.status-badge.approved { background: #e8f5e8; color: #2e7d32; }
.status-badge.rejected { background: #ffebee; color: #c62828; }

.budget-impact {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 6px;
    margin: 15px 0;
}

.impact-amount {
    font-size: 1.4em;
    font-weight: bold;
    margin-left: 10px;
}

.impact-amount.positive { color: #d32f2f; }
.impact-amount.negative { color: #388e3c; }

.co-items {
    margin: 20px 0;
}

.co-item {
    background: #fafafa;
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 10px;
    border-left: 4px solid #e0e0e0;
}

.item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.item-amount.positive { color: #d32f2f; font-weight: bold; }
.item-amount.negative { color: #388e3c; font-weight: bold; }

.approval-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
}

.btn-success {
    background: #4caf50;
    color: white;
}

.btn-success:hover { background: #45a049; }

.btn-danger {
    background: #f44336;
    color: white;
}

.btn-danger:hover { background: #da190b; }

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-secondary:hover { background: #5a6268; }

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.approval-modal {
    background: white;
    padding: 30px;
    border-radius: 8px;
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
}

.budget-warning {
    margin: 15px 0;
}

.alert {
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 15px;
}

.alert-warning {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
}

.alert-info {
    background: #d1ecf1;
    border: 1px solid #bee5eb;
    color: #0c5460;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

.form-group textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    resize: vertical;
}

.modal-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    margin-top: 20px;
}
```

### Transaction History Styles

```css
/* styles/TransactionHistory.css */
.transaction-history {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.transaction-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #f0f0f0;
}

.filter-controls select {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
}

.transaction-item {
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 15px;
    background: #fafafa;
}

.transaction-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
}

.transaction-number {
    font-weight: bold;
    font-size: 1.1em;
}

.transaction-type {
    background: #e3f2fd;
    color: #1976d2;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    margin-left: 10px;
}

.transaction-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.transaction-impact .amount.positive { color: #d32f2f; }
.transaction-impact .amount.negative { color: #388e3c; }

.budget-change {
    background: white;
    padding: 10px;
    border-radius: 4px;
    text-align: center;
}

.budget-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-weight: 500;
}

.arrow {
    color: #666;
    font-weight: bold;
}

.transaction-meta {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #e0e0e0;
    color: #666;
}
```

---

## Usage Examples

### Main Page Implementation

```jsx
// pages/ProjectFinance.jsx
import React from 'react';
import { ChangeOrderProvider } from '../context/ChangeOrderContext';
import BudgetImpactDashboard from '../components/BudgetImpactDashboard';
import ChangeOrderApproval from '../components/ChangeOrderApproval';
import TransactionHistory from '../components/TransactionHistory';
import { useAuth } from '../context/AuthContext';

const ProjectFinance = ({ projectId }) => {
    const { currentUser } = useAuth();

    return (
        <ChangeOrderProvider projectId={projectId}>
            <div className="project-finance">
                <h1>Project Financial Management</h1>
                
                <BudgetImpactDashboard projectId={projectId} />
                
                <div className="finance-sections">
                    <div className="change-orders-section">
                        <h2>Change Order Management</h2>
                        {/* Change Order components will be rendered here */}
                    </div>
                    
                    <div className="transactions-section">
                        <h2>Transaction History</h2>
                        <TransactionHistory projectId={projectId} />
                    </div>
                </div>
            </div>
        </ChangeOrderProvider>
    );
};

export default ProjectFinance;
```

## Summary

This implementation provides:

1. **Complete CO approval workflow** with automatic budget updates
2. **Transaction tracking** with full audit trail
3. **Real-time budget impact** calculations and display
4. **Comprehensive error handling** and validation
5. **Responsive UI components** with proper styling
6. **State management** for efficient data flow
7. **Role-based access control** for approvals

The frontend automatically handles the backend's transaction creation and budget updates, providing users with immediate feedback on financial impacts and maintaining complete audit trails.
