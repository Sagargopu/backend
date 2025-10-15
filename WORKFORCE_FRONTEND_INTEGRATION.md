# Workforce Management Frontend Integration Guide

## Overview
This guide helps integrate the BuildBuzz workforce API endpoints into your frontend application at `http://localhost:5173/business-clerk/workforce-management`.

## Base Configuration

### API Base URL
```javascript
const API_BASE_URL = 'http://localhost:8000';
const WORKFORCE_API = `${API_BASE_URL}/workforce`;
```

## Core API Integration Functions

### 1. Profession Management

#### Get All Professions
```javascript
const getProfessions = async () => {
  try {
    const response = await fetch(`${WORKFORCE_API}/professions/`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching professions:', error);
    throw error;
  }
};
```

#### Create New Profession
```javascript
const createProfession = async (professionData) => {
  try {
    const response = await fetch(`${WORKFORCE_API}/professions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(professionData)
    });
    return await response.json();
  } catch (error) {
    console.error('Error creating profession:', error);
    throw error;
  }
};

// Example usage:
// createProfession({
//   name: "Electrician",
//   description: "Licensed electrician for commercial projects",
//   category: "Electrical"
// });
```

### 2. Worker Management

#### Get All Workers (with filters)
```javascript
const getWorkers = async (filters = {}) => {
  const params = new URLSearchParams();
  
  if (filters.profession_id) params.append('profession_id', filters.profession_id);
  if (filters.availability) params.append('availability', filters.availability);
  if (filters.min_skill_rating) params.append('min_skill_rating', filters.min_skill_rating);
  if (filters.max_skill_rating) params.append('max_skill_rating', filters.max_skill_rating);
  
  try {
    const response = await fetch(`${WORKFORCE_API}/workers/?${params}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching workers:', error);
    throw error;
  }
};
```

#### Get Available Workers
```javascript
const getAvailableWorkers = async () => {
  try {
    const response = await fetch(`${WORKFORCE_API}/workers/available`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching available workers:', error);
    throw error;
  }
};
```

#### Create New Worker
```javascript
const createWorker = async (workerData) => {
  try {
    const response = await fetch(`${WORKFORCE_API}/workers/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workerData)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to create worker');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error creating worker:', error);
    throw error;
  }
};

// Example usage:
// createWorker({
//   worker_id: "ELC001",
//   first_name: "John",
//   last_name: "Smith",
//   phone_number: "+1-555-0101",
//   email: "john.smith@buildbuzz.com",
//   profession_id: 1,
//   skill_rating: 8.5,
//   wage_rate: 35.50,
//   availability: "Available"
// });
```

#### Get Worker Details
```javascript
const getWorkerDetails = async (workerId) => {
  try {
    const response = await fetch(`${WORKFORCE_API}/workers/${workerId}`);
    if (!response.ok) {
      throw new Error('Worker not found');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching worker details:', error);
    throw error;
  }
};
```

#### Update Worker
```javascript
const updateWorker = async (workerId, updateData) => {
  try {
    const response = await fetch(`${WORKFORCE_API}/workers/${workerId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateData)
    });
    return await response.json();
  } catch (error) {
    console.error('Error updating worker:', error);
    throw error;
  }
};
```

### 3. Project Assignment Management

#### Assign Worker to Project
```javascript
const assignWorkerToProject = async (workerId, projectId, startDate, endDate = null) => {
  const params = new URLSearchParams({
    project_id: projectId,
    start_date: startDate
  });
  
  if (endDate) params.append('end_date', endDate);
  
  try {
    const response = await fetch(`${WORKFORCE_API}/workers/${workerId}/assign-project?${params}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return await response.json();
  } catch (error) {
    console.error('Error assigning worker to project:', error);
    throw error;
  }
};
```

#### Unassign Worker from Project
```javascript
const unassignWorkerFromProject = async (workerId) => {
  try {
    const response = await fetch(`${WORKFORCE_API}/workers/${workerId}/unassign-project`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return await response.json();
  } catch (error) {
    console.error('Error unassigning worker from project:', error);
    throw error;
  }
};
```

#### Get Workers by Project
```javascript
const getWorkersByProject = async (projectId) => {
  try {
    const response = await fetch(`${WORKFORCE_API}/workers/by-project/${projectId}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching workers by project:', error);
    throw error;
  }
};
```

### 4. Project History Management

#### Get Worker's Project History
```javascript
const getWorkerProjectHistory = async (workerId) => {
  try {
    const response = await fetch(`${WORKFORCE_API}/project-history/worker/${workerId}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching worker project history:', error);
    throw error;
  }
};
```

#### Create Project History Entry
```javascript
const createProjectHistory = async (historyData) => {
  try {
    const response = await fetch(`${WORKFORCE_API}/project-history/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(historyData)
    });
    return await response.json();
  } catch (error) {
    console.error('Error creating project history:', error);
    throw error;
  }
};
```

#### Complete Project Assignment
```javascript
const completeProjectAssignment = async (historyId, endDate, performanceRating = null, notes = null) => {
  const params = new URLSearchParams({ end_date: endDate });
  
  if (performanceRating) params.append('performance_rating', performanceRating);
  if (notes) params.append('notes', notes);
  
  try {
    const response = await fetch(`${WORKFORCE_API}/project-history/${historyId}/complete?${params}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return await response.json();
  } catch (error) {
    console.error('Error completing project assignment:', error);
    throw error;
  }
};
```

## React Component Integration Examples

### Workforce Management Dashboard Component

```javascript
import React, { useState, useEffect } from 'react';

const WorkforceManagement = () => {
  const [workers, setWorkers] = useState([]);
  const [professions, setProfessions] = useState([]);
  const [selectedProfession, setSelectedProfession] = useState('');
  const [availabilityFilter, setAvailabilityFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [workersData, professionsData] = await Promise.all([
        getWorkers(),
        getProfessions()
      ]);
      setWorkers(workersData);
      setProfessions(professionsData);
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = async () => {
    try {
      const filters = {};
      if (selectedProfession) filters.profession_id = selectedProfession;
      if (availabilityFilter) filters.availability = availabilityFilter;
      
      const filteredWorkers = await getWorkers(filters);
      setWorkers(filteredWorkers);
    } catch (error) {
      console.error('Error filtering workers:', error);
    }
  };

  const handleAssignProject = async (workerId, projectId, startDate) => {
    try {
      await assignWorkerToProject(workerId, projectId, startDate);
      // Refresh worker list
      await handleFilterChange();
    } catch (error) {
      console.error('Error assigning worker:', error);
      alert('Failed to assign worker to project');
    }
  };

  if (loading) return <div>Loading workforce data...</div>;

  return (
    <div className="workforce-management">
      <h1>Workforce Management</h1>
      
      {/* Filters */}
      <div className="filters">
        <select 
          value={selectedProfession} 
          onChange={(e) => setSelectedProfession(e.target.value)}
        >
          <option value="">All Professions</option>
          {professions.map(prof => (
            <option key={prof.id} value={prof.id}>
              {prof.name}
            </option>
          ))}
        </select>
        
        <select 
          value={availabilityFilter} 
          onChange={(e) => setAvailabilityFilter(e.target.value)}
        >
          <option value="">All Availability</option>
          <option value="Available">Available</option>
          <option value="Assigned">Assigned</option>
          <option value="On Leave">On Leave</option>
          <option value="Unavailable">Unavailable</option>
        </select>
        
        <button onClick={handleFilterChange}>Apply Filters</button>
      </div>

      {/* Workers List */}
      <div className="workers-list">
        {workers.map(worker => (
          <div key={worker.id} className="worker-card">
            <h3>{worker.first_name} {worker.last_name}</h3>
            <p><strong>ID:</strong> {worker.worker_id}</p>
            <p><strong>Profession:</strong> {worker.profession?.name}</p>
            <p><strong>Skill Rating:</strong> {worker.skill_rating}/10</p>
            <p><strong>Wage Rate:</strong> ${worker.wage_rate}/hour</p>
            <p><strong>Availability:</strong> {worker.availability}</p>
            
            {worker.current_project_id && (
              <p><strong>Current Project:</strong> {worker.current_project_id}</p>
            )}
            
            <div className="worker-actions">
              <button onClick={() => handleViewHistory(worker.id)}>
                View History
              </button>
              {worker.availability === 'Available' && (
                <button onClick={() => handleAssignToProject(worker.id)}>
                  Assign to Project
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WorkforceManagement;
```

## Error Handling

```javascript
const handleApiError = (error, operation) => {
  console.error(`Error during ${operation}:`, error);
  
  if (error.response) {
    // API returned an error response
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        alert(`Bad Request: ${data.detail || 'Invalid data provided'}`);
        break;
      case 404:
        alert(`Not Found: ${data.detail || 'Resource not found'}`);
        break;
      case 422:
        alert(`Validation Error: ${data.detail || 'Please check your input'}`);
        break;
      default:
        alert(`Error: ${data.detail || 'Something went wrong'}`);
    }
  } else {
    // Network or other error
    alert(`Network Error: Unable to ${operation}. Please check your connection.`);
  }
};
```

## Next Steps for Frontend Integration

1. **Install Dependencies**: Make sure your frontend has HTTP client capabilities (fetch API or axios)

2. **Environment Configuration**: Set up your API base URL in environment variables

3. **State Management**: Consider using React Context, Redux, or Zustand for workforce state management

4. **UI Components**: Create reusable components for:
   - Worker cards/lists
   - Profession selection
   - Project assignment dialogs
   - Worker detail views
   - Performance rating inputs

5. **Form Validation**: Implement client-side validation for worker creation/editing forms

6. **Real-time Updates**: Consider WebSocket connections for real-time workforce status updates

7. **Data Caching**: Implement caching for frequently accessed data like professions list

8. **Pagination**: Add pagination for large worker lists

9. **Search Functionality**: Add search capabilities by worker name, ID, or skills

10. **Export Features**: Add functionality to export worker data to CSV/PDF

This integration guide provides all the necessary API calls and examples to fully integrate the workforce management functionality into your frontend application.