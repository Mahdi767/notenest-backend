

If you need to add a new resource type, contact the backend team. New types require:
1. Adding to `RESOURCE_TYPE_CHOICES` in `resources/constant.py`
2. Running Django migrations
3. Redeploying the backend

---

## ❌ Why Edit Was Failing with 400 Error

### The Problem
The backend was requiring a **file field** even when editing metadata-only fields (title, description, etc.).

### The Fix Applied
✅ Made the file field optional for PATCH/PUT requests  
✅ File is still required for initial POST (creation)  
✅ Added proper update() method to handle partial updates  

### What Changed
**Before:**
```python
file = serializers.FileField(required=True)  # ❌ Always required
```

**After:**
```python
file = serializers.FileField(required=False)  # ✅ Optional for updates
```

---

## Now Working: Edit Without File

You can now update resources **without re-uploading the file**:

### Example 1: Edit Title & Description Only
```javascript
const updateResource = async (resourceId, newTitle, newDescription) => {
  const response = await fetch(
    `/api/resources/resources/${resourceId}/`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': `Token ${userToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: newTitle,
        description: newDescription
        // NO FILE - that's fine now!
      })
    }
  );
  return await response.json();
};
```

### Example 2: Update Multiple Fields
```javascript
const updateResource = async (resourceId, updates) => {
  const payload = {};
  
  if (updates.title) payload.title = updates.title;
  if (updates.description) payload.description = updates.description;
  if (updates.resource_type) payload.resource_type = updates.resource_type;
  if (updates.tags) payload.tags = updates.tags;
  if (updates.file) payload.file = updates.file; // Optional
  
  const response = await fetch(
    `/api/resources/resources/${resourceId}/`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': `Token ${userToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    }
  );
  return await response.json();
};
```

### Example 3: Update with File Replacement
```javascript
// If you DO want to update the file, send it as FormData
const updateResourceWithFile = async (resourceId, formData) => {
  const response = await fetch(
    `/api/resources/resources/${resourceId}/`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': `Token ${userToken}`
        // NO Content-Type header - let browser set it
      },
      body: formData // FormData with file
    }
  );
  return await response.json();
};
```

---

## Updated Frontend Checklist

- [ ] Remove file requirement validation for edit forms
- [ ] Allow users to edit title/description without file
- [ ] Make file upload optional in edit form
- [ ] Show "File is optional" label on edit forms
- [ ] Handle both JSON (no file) and FormData (with file) submissions
- [x] ~~Require file for every update~~ (FIXED)

---

## Important Notes

If you need to add a new resource type, contact the backend team. New types require:
1. Adding to `RESOURCE_TYPE_CHOICES` in `resources/constant.py`
2. Running Django migrations
3. Redeploying the backend

## Important: Status Reset Behavior

When editing an **approved resource**, the backend automatically resets its status to **"pending"** for review. This is a security/quality control feature.

---

## Status Reset Rules

### ✅ Resources That KEEP Their Status
- Resources edited by **staff/admin users** (is_staff = true)
- Resources edited by **moderators with special permissions**
- Non-content field edits (minor updates like view_count, download_count)

### ⚠️ Resources That RESET to Pending
- **Approved resources** edited by **regular students/non-staff users**
- When any of these fields are changed:
  - Title
  - Description
  - File
  - Resource Type
  - Department
  - Course
  - Semester
  - Tags

---

## User Scenarios

### Scenario 1: Student Editing Their Own Approved Resource
```
Student uploads resource → Approved by moderator → Status = "approved"
         ↓
Student edits the resource title/file/description
         ↓
Status automatically changes → "pending" (needs re-review)
```

**Frontend behavior:** Show alert to user
```
⚠️ "Your changes have been saved, but your resource needs to be reviewed again.
Status has been reset to Pending. A moderator will review it shortly."
```

### Scenario 2: Admin/Staff Editing a Resource
```
Approved resource (Status = "approved")
         ↓
Admin/Staff edits the resource
         ↓
Status remains → "approved" (no re-review needed)
```

---

## Frontend Implementation Guide

### 1. **Edit Endpoint**

```
PUT /api/resources/resources/{resource_id}/
PATCH /api/resources/resources/{resource_id}/
```

**Request Format:**
```javascript
const updateResource = async (resourceId, updatedData) => {
  const response = await fetch(
    `https://notenest-backend.h35.onrender.com/api/resources/resources/${resourceId}/`,
    {
      method: 'PATCH',  // or PUT for full replacement
      headers: {
        'Authorization': `Token ${userToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: updatedData.title,
        description: updatedData.description,
        resource_type: updatedData.resourceType,
        tags: updatedData.tags,
        department: updatedData.department,
        course: updatedData.course,
        semester: updatedData.semester
        // file: updatedData.file  // If updating file
      })
    }
  );
  
  const result = await response.json();
  return result;
};
```

### 2. **Handle Status Reset Response**

```javascript
const handleResourceEdit = async (resourceId, formData) => {
  try {
    const response = await updateResource(resourceId, formData);
    
    // Check if status was reset
    if (response.status === 'pending' && response.previous_status === 'approved') {
      // Show warning to user
      showAlert({
        type: 'warning',
        title: 'Resource Under Review',
        message: 'Your changes have been saved. The resource status has been reset to "Pending" and will be reviewed by a moderator.',
        duration: 5000
      });
    } else {
      showAlert({
        type: 'success',
        message: 'Resource updated successfully!'
      });
    }
    
    // Refresh resource data
    loadResourceDetails(resourceId);
    
  } catch (error) {
    showAlert({
      type: 'error',
      message: error.message
    });
  }
};
```

### 3. **Edit Form UI Best Practices**

```javascript
// Display warning if resource is approved
{resource.status === 'approved' && (
  <div className="alert alert-info">
    <strong>📌 Note:</strong> If you edit this resource, it will be reset to "Pending" 
    and needs to be approved again by a moderator.
  </div>
)}

// Edit form
<form onSubmit={handleEdit}>
  <input 
    type="text" 
    name="title" 
    value={formData.title}
    placeholder="Resource Title"
    required
  />
  <textarea 
    name="description" 
    value={formData.description}
    placeholder="Description"
    required
  />
  {/* Other fields */}
  
  <button type="submit" className="btn btn-primary">
    Save Changes
  </button>
</form>

// Status badge
<span className={`badge badge-${getBadgeColor(resource.status)}`}>
  {resource.status.charAt(0).toUpperCase() + resource.status.slice(1)}
</span>
```

### 4. **Status Timeline Display**

Show users the resource status flow:

```
Created: {created_at}
    ↓
Status: Pending → Review by Moderator
    ↓
Status: Approved ← Current
    ↓
(If edited by student) → Status: Pending (Re-review needed)
```

---

## API Response Examples

### Success Response After Edit:
```json
{
  "id": 42,
  "title": "Updated Title",
  "description": "Updated Description",
  "resource_type": "lecture_note",
  "status": "pending",
  "created_at": "2026-04-01T10:00:00Z",
  "updated_at": "2026-04-05T15:30:00Z",
  "view_count": 150,
  "download_count": 25,
  "tags": [2, 18, 5],
  "department": 1,
  "course": 3,
  "semester": 1,
  "uploaded_by": 5
}
```

### Error Response (No Permission):
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Expected Behavior by User Type

| User Type | Edit Own Resource | Edit Others | Status Persists? |
|-----------|------------------|-------------|-----------------|
| Student (non-staff) | ✅ Yes | ❌ No | ❌ Resets to pending if approved |
| Admin/Staff | ✅ Yes | ✅ Yes | ✅ Yes, stays approved |
| Moderator | ❌ No | ✅ Limited | Depends on role |

---

## Frontend Checklist for Edit Feature

- [ ] Add edit button/icon to resource cards/detail view
- [ ] Create edit form with all editable fields
- [ ] Show warning if editing an approved resource
- [ ] Send PATCH/PUT request to correct endpoint
- [ ] Handle status reset response gracefully
- [ ] Show success/error notifications
- [ ] Refresh resource data after successful edit
- [ ] Disable file upload field if only editing metadata
- [ ] Show current status badge prominently
- [ ] Track edit history (optional, backend supports it)

---

## Important Notes

1. **Non-staff users cannot edit other users' resources** - You'll get a 403 Forbidden error
2. **Status reset is automatic** - No manual approval needed from moderators, but moderation review is required
3. **File updates also trigger reset** - Even if you only update the file, approved status will reset
4. **Tags, department, course, semester changes trigger reset** - These are content changes
5. **View count and download count don't trigger reset** - These are auto-incremented
