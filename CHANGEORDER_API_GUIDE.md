# ChangeOrder API Guide for Frontend

## 1. Create ChangeOrder (POST /change-orders/)
- **Payload Example:**
```json
{
  "task_id": 123,
  "title": "Change HVAC unit",
  "description": "Replace with higher capacity unit.",
  "reason": "Client Request",
  "status": "Draft",
  "notes": "Urgent request from client.",
  "created_by": 45
}
```
- **Required fields:** `task_id`, `title`, `description`, `created_by`
- **Optional fields:** `reason`, `status`, `notes`
- **Returns:** Newly created ChangeOrder object.

## 2. List ChangeOrders (GET /change-orders/)
- **Returns:** Array of ChangeOrder objects, each with:
  - `id`, `co_number`, `task_id`, `title`, `description`, `reason`, `status`, `notes`, `created_by`, `approved_by`, `approved_date`, `created_at`, `updated_at`
  - **Extended fields:** `project_name`, `component_name`, `pm_name`

## 3. Get Single ChangeOrder (GET /change-orders/{co_id})
- **Returns:** ChangeOrder object with all fields above.

## 4. Filter ChangeOrders
- By status: `GET /change-orders/by-status/{status}`
- By task: `GET /change-orders/by-task/{task_id}`
- By component: `GET /change-orders/by-component/{component_id}`
- By creator: `GET /change-orders/by-creator/{creator_id}`
- By approver: `GET /change-orders/by-approver/{approver_id}`
- **Returns:** Array of ChangeOrder objects (extended schema).

## 5. Update ChangeOrder (PUT /change-orders/{co_id})
- **Payload:** Same as create, but all fields optional.
- **Returns:** Updated ChangeOrder object.

## Notes for Frontend
- Dates are ISO strings.
- Extended endpoints include `project_name`, `component_name`, and `pm_name` for display.
- Handle missing optional fields gracefully.
- Use `id` for referencing and updates.
