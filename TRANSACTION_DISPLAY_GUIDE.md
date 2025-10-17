# Guide: Displaying Transactions at Component and Project Level on Project Portal (Frontend)

## Overview
This guide explains how to effectively display financial transactions (such as Purchase Orders, Change Orders, etc.) at both the component and project levels in your project portal frontend. It covers recommended UI structure, API usage, filtering, and best practices for clarity and usability.

---

## 1. Data Structure & API Endpoints
- **Project Level:**
  - Show all transactions related to a specific project.
  - Use endpoints like:
    - `GET /projects/{project_id}/transactions` (if available)
    - Or aggregate from:
      - `GET /finance/purchase-orders/by-project/{project_id}`
      - `GET /finance/change-orders/by-project/{project_id}`
- **Component Level:**
  - Show transactions for a specific project component.
  - Use endpoints like:
    - `GET /projects/components/{component_id}/transactions` (if available)
    - Or aggregate from:
      - `GET /finance/purchase-orders/by-component/{component_id}`
      - `GET /finance/change-orders/by-component/{component_id}`

---

## 2. UI Layout Recommendations
- **Tabbed or Segmented View:**
  - Tabs for "Project Transactions" and "Component Transactions".
  - Each tab lists relevant transactions with summary info.
- **Table/List Display:**
  - Columns: Transaction Type, ID, Description, Amount, Status, Date, Linked Component/Project, Actions.
  - Allow sorting and filtering by type, status, date, etc.
- **Detail Drawer/Modal:**
  - Clicking a transaction opens a detail view with full info and related items.

---

## 3. Filtering & Search
- **Project Level:**
  - Filter by transaction type (PO, Change Order, etc.), status, date range.
- **Component Level:**
  - Filter by transaction type, status, date, and parent project.
- **Search Bar:**
  - Allow searching by transaction ID, description, vendor, etc.

---

## 4. API Integration Example
- **Fetch Project Transactions:**
  ```js
  // Example API call
  fetch(`/finance/purchase-orders/by-project/${projectId}`)
    .then(res => res.json())
    .then(data => setProjectPOs(data));
  fetch(`/finance/change-orders/by-project/${projectId}`)
    .then(res => res.json())
    .then(data => setProjectCOs(data));
  ```
- **Fetch Component Transactions:**
  ```js
  fetch(`/finance/purchase-orders/by-component/${componentId}`)
    .then(res => res.json())
    .then(data => setComponentPOs(data));
  fetch(`/finance/change-orders/by-component/${componentId}`)
    .then(res => res.json())
    .then(data => setComponentCOs(data));
  ```

---

## 5. Best Practices
- **Show Totals:**
  - Display total amounts for each transaction type at both levels.
- **Status Indicators:**
  - Use color-coded badges for status (e.g., Approved, Pending, Draft).
- **Linkage:**
  - Provide links from component-level transactions to their parent project, and vice versa.
- **Responsiveness:**
  - Ensure tables/lists are mobile-friendly and support horizontal scrolling for many columns.
- **Error Handling:**
  - Gracefully handle empty states, API errors, and loading indicators.

---

## 6. Example UI Mockup
```
[ Project Portal ]
-------------------------------------------------
| Tabs: [Project Transactions] [Component Transactions] |
-------------------------------------------------
| Table:                                            |
|---------------------------------------------------|
| Type | ID | Desc | Amount | Status | Date | ...    |
|---------------------------------------------------|
| PO   | 101| ...  | $5000  | Approved| ... |       |
| CO   | 202| ...  | $1200  | Pending | ... |       |
| ...                                             |
-------------------------------------------------
| [Filter] [Search] [Export]                       |
-------------------------------------------------
```

---

## 7. Summary
- Use dedicated endpoints to fetch transactions at both levels.
- Present data in clear, filterable tables with detail views.
- Show totals and status for quick insights.
- Ensure navigation between component and project context is easy.

---

## References
- See API Guide for endpoint details and payload formats.
- Coordinate with backend team for any missing endpoints or custom filters.
