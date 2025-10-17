# Purchase Order Workflow Guide for Frontend

## 1. Create Purchase Order
- **Endpoint:** `POST /purchase-orders/`
- **Payload Example:**
```json
{
  "task_id": 123,
  "vendor_id": 10,
  "description": "Order for steel beams",
  "delivery_date": "2025-10-20",
  "status": "Draft",
  "notes": "Urgent delivery required",
  "created_by": 45
}
```
- **Required fields:** `task_id`, `vendor_id`, `description`, `created_by`
- **Optional fields:** `delivery_date`, `status`, `notes`
- **Returns:** Newly created PurchaseOrder object.

---

## 2. Add Items to Purchase Order
- **Endpoint:** `POST /purchase-order-items/`
- **Payload Example:**
```json
{
  "purchase_order_id": 1,
  "item_name": "Steel Beam",
  "description": "I-beam, 20ft",
  "category": "Material",
  "price": 500.00
}
```
- **Required fields:** `purchase_order_id`, `item_name`, `price`
- **Optional fields:** `description`, `category`
- **Returns:** Newly created PurchaseOrderItem object.

---

## 3. List Purchase Orders
- **Endpoint:** `GET /purchase-orders/`
- **Returns:** Array of PurchaseOrder objects, each with:
  - `id`, `po_number`, `task_id`, `vendor_id`, `description`, `delivery_date`, `status`, `notes`, `created_by`, `approved_by`, `approved_date`, `created_at`, `updated_at`
- **Tip:** Use filters like `/purchase-orders/by-status/{status}` or `/purchase-orders/by-task/{task_id}` as needed.

---

## 4. Get Single Purchase Order (with Items)
- **Endpoint:** `GET /purchase-orders/{po_id}`
- **Returns:** PurchaseOrder object.
- **To get items:** `GET /purchase-orders/{po_id}/items` returns an array of items for that PO.

---

## 5. Approve or Update Purchase Order
- **Endpoint:** `PUT /purchase-orders/{po_id}`
- **Payload:** Any updatable fields (e.g., `status`, `approved_by`, `approved_date`)
- **Returns:** Updated PurchaseOrder object.

---

## 6. Delete Purchase Order or Item
- **Endpoint:** `DELETE /purchase-orders/{po_id}` or `DELETE /purchase-order-items/{item_id}`
- **Returns:** Success message.

---

## Frontend Workflow Example
1. User fills out a PO form and submits (create PO).
2. User adds one or more items to the PO.
3. User or manager reviews and updates PO status (e.g., submits for approval).
4. Approver reviews and approves PO (update status, set `approved_by` and `approved_date`).
5. PO and items can be listed, filtered, or deleted as needed.

---

## Notes
- Dates are ISO strings.
- Always handle optional fields gracefully.
- Use PO `id` for referencing and updates.
- For approval, ensure the correct user ID is set in `approved_by`.
