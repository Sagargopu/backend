# Task Creation API Guide
## POST /tasks/

### Required JSON Format

#### Minimum Required Fields:
```json
{
  "name": "Task Name",
  "project_id": 1
}
```

#### Complete JSON Format:
```json
{
  "name": "Complete Task Example",
  "description": "Optional task description",
  "status": "To Do",
  "priority": "Medium", 
  "task_type": "Planning",
  "budget": 5000.00,
  "start_date": "2025-02-01",
  "end_date": "2025-02-15",
  "component_id": 1,
  "project_id": 1
}
```

### Field Details and Validations

#### Required Fields:
- **`name`** (string): Task name - REQUIRED, max 255 characters
- **`project_id`** (integer): Valid project ID - REQUIRED

#### Optional Fields:
- **`description`** (string or null): Task description - Optional
- **`status`** (string): Task status - Defaults to "To Do"
  - Valid values: "To Do", "In Progress", "Done", "Blocked", "Cancelled", "Backlog"
- **`priority`** (string): Task priority - Defaults to "Medium"  
  - Valid values: "Low", "Medium", "High", "Critical"
- **`task_type`** (string or null): Type of task - Optional, max 100 characters
  - Examples: "Planning", "Construction", "Inspection", "Documentation"
- **`budget`** (decimal or null): Task budget - Optional, up to 15 digits with 2 decimal places
  - Example: 5000.00, 123456.78
- **`start_date`** (date string or null): Task start date - Optional
  - Format: "YYYY-MM-DD" (ISO date format)
  - Example: "2025-02-01"
- **`end_date`** (date string or null): Task end date - Optional
  - Format: "YYYY-MM-DD" (ISO date format)
  - Example: "2025-02-15"
- **`component_id`** (integer or null): Optional component association

### Date Validation Rules

1. **Task End Date > Start Date:**
   ```
   If both start_date and end_date are provided:
   end_date must be after start_date
   ```

2. **Component Date Constraints:**
   ```
   If component_id is provided and component has dates:
   - task start_date must be >= component start_date
   - task end_date must be <= component end_date
   ```

3. **Project Date Constraints:**
   ```
   If task has no component but has project dates:
   - task start_date must be >= project start_date  
   - task end_date must be <= project end_date
   ```

### Example Valid Requests

#### 1. Minimal Task:
```json
{
  "name": "Review Requirements", 
  "project_id": 1
}
```

#### 2. Task with Component:
```json
{
  "name": "Install Electrical Outlets",
  "description": "Install 25 electrical outlets in office areas", 
  "status": "To Do",
  "priority": "High",
  "task_type": "Construction",
  "budget": 3750.00,
  "start_date": "2025-02-01",
  "end_date": "2025-02-05", 
  "component_id": 1,
  "project_id": 1
}
```

#### 3. Planning Task without Component:
```json
{
  "name": "Site Survey and Planning",
  "description": "Initial site survey and project planning",
  "status": "In Progress", 
  "priority": "Critical",
  "task_type": "Planning",
  "budget": 15000.00,
  "start_date": "2025-01-15",
  "end_date": "2025-01-25",
  "project_id": 1
}
```

### Common Validation Errors (422 Responses)

#### 1. Missing Required Fields:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "name"],
      "msg": "Field required"
    }
  ]
}
```

#### 2. Invalid Date Format:
```json
{
  "detail": [
    {
      "type": "date_parsing", 
      "loc": ["body", "start_date"],
      "msg": "Input should be a valid date or datetime"
    }
  ]
}
```

#### 3. Date Logic Errors:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body"],
      "msg": "Task end date must be after start date"
    }
  ]
}
```

#### 4. Invalid Foreign Key:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "project_id"],
      "msg": "Project with this ID does not exist"
    }
  ]
}
```

### Response Format (Success - 200/201):
```json
{
  "id": 15,
  "name": "Review Requirements",
  "description": null,
  "status": "To Do", 
  "priority": "Medium",
  "task_type": null,
  "budget": null,
  "start_date": null,
  "end_date": null,
  "component_id": null,
  "project_id": 1,
  "created_at": "2025-10-16T22:30:45",
  "updated_at": null
}
```

### Frontend Integration Tips

1. **Always validate dates on frontend before sending**
2. **Use ISO date format (YYYY-MM-DD) for date fields**
3. **Handle null values properly (set to null, not empty string)**
4. **Validate budget as decimal with max 2 decimal places**
5. **Ensure project_id exists before creating task**
6. **If using component_id, verify it belongs to the same project**