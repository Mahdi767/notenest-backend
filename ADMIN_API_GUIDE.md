# NoteNest Admin UI - Complete API Guideline

**Base URL:** `https://notenest-backend.onrender.com/api/` (Render Deployment)
**Documentation:** `/api/docs/` (Swagger UI) | `/api/redoc/` (ReDoc)

---

## Table of Contents
1. [Authentication](#authentication)
2. [Academic Module APIs](#academic-module-apis)
3. [Resources Module APIs](#resources-module-apis)
4. [Moderation Module APIs](#moderation-module-apis)
5. [Accounts Module APIs](#accounts-module-apis)
6. [Interactions Module APIs](#interactions-module-apis)
7. [Notifications Module APIs](#notifications-module-apis)
8. [Response Format Standards](#response-format-standards)
9. [Error Handling](#error-handling)

---

## Authentication

### JWT Token Authentication
All admin endpoints (except login) require a valid JWT token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Login Endpoint (Public)
```
POST /api/accounts/login/
Content-Type: application/json

Request Body:
{
  "email": "admin@example.com",
  "password": "password123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "first_name": "Admin",
    "role": "admin",
    "is_staff": true,
    "is_verified": true
  }
}
```

### Verify Admin Access
```
GET /api/accounts/me/
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "role": "admin",
  "is_staff": true,
  "is_verified": true,
  "date_joined": "2024-01-01T10:00:00Z"
}
```

---

## Academic Module APIs

### ✅ ADMIN ONLY - Departments Management

#### Create Department
```
POST /api/academic/departments/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "name": "Computer Science",
  "code": "CSE"
}

Response (201 Created):
{
  "id": 1,
  "name": "Computer Science",
  "code": "CSE",
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### List All Departments
```
GET /api/academic/departments/
Authorization: Bearer <admin_token>

Response:
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Computer Science",
      "code": "CSE",
      "created_at": "2024-01-01T10:00:00Z"
    },
    ...
  ]
}
```

#### Retrieve Department Details
```
GET /api/academic/departments/{id}/
Authorization: Bearer <admin_token>

Response:
{
  "id": 1,
  "name": "Computer Science",
  "code": "CSE",
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### Update Department
```
PUT /api/academic/departments/{id}/
PATCH /api/academic/departments/{id}/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "name": "Computer Science & Engineering",
  "code": "CSE"
}

Response (200 OK):
{
  "id": 1,
  "name": "Computer Science & Engineering",
  "code": "CSE",
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### Delete Department
```
DELETE /api/academic/departments/{id}/
Authorization: Bearer <admin_token>

Response (204 No Content)
```

---

### ✅ ADMIN ONLY - Courses Management

#### Create Course
```
POST /api/academic/courses/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "title": "Data Structures",
  "course_code": "CSE201",
  "department": 1
}

Response (201 Created):
{
  "id": 1,
  "title": "Data Structures",
  "course_code": "CSE201",
  "department": 1,
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### List All Courses
```
GET /api/academic/courses/
Authorization: Bearer <admin_token>

Query Parameters:
- department (optional): Filter by department ID
  GET /api/academic/courses/?department=1

Response:
{
  "count": 20,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Data Structures",
      "course_code": "CSE201",
      "department": 1,
      "created_at": "2024-01-01T10:00:00Z"
    },
    ...
  ]
}
```

#### Retrieve Course Details
```
GET /api/academic/courses/{id}/
Authorization: Bearer <admin_token>

Response:
{
  "id": 1,
  "title": "Data Structures",
  "course_code": "CSE201",
  "department": 1,
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### Update Course
```
PUT /api/academic/courses/{id}/
PATCH /api/academic/courses/{id}/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "title": "Data Structures & Algorithms",
  "course_code": "CSE201",
  "department": 1
}

Response (200 OK):
{
  "id": 1,
  "title": "Data Structures & Algorithms",
  "course_code": "CSE201",
  "department": 1,
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### Delete Course
```
DELETE /api/academic/courses/{id}/
Authorization: Bearer <admin_token>

Response (204 No Content)
```

---

### ✅ ADMIN ONLY - Semesters Management

#### Create Semester
```
POST /api/academic/semesters/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "name": "Fall",
  "year": 2024,
  "is_active": true
}

Response (201 Created):
{
  "id": 1,
  "name": "Fall",
  "year": 2024,
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### List All Semesters
```
GET /api/academic/semesters/
Authorization: Bearer <admin_token>

Response:
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Fall",
      "year": 2024,
      "is_active": true,
      "created_at": "2024-01-01T10:00:00Z"
    },
    ...
  ]
}
```

#### Retrieve Semester Details
```
GET /api/academic/semesters/{id}/
Authorization: Bearer <admin_token>

Response:
{
  "id": 1,
  "name": "Fall",
  "year": 2024,
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### Update Semester
```
PUT /api/academic/semesters/{id}/
PATCH /api/academic/semesters/{id}/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "name": "Fall",
  "year": 2024,
  "is_active": false
}

Response (200 OK):
{
  "id": 1,
  "name": "Fall",
  "year": 2024,
  "is_active": false,
  "created_at": "2024-01-01T10:00:00Z"
}
```

#### Delete Semester
```
DELETE /api/academic/semesters/{id}/
Authorization: Bearer <admin_token>

Response (204 No Content)
```

---

## Resources Module APIs

### ✅ ADMIN ONLY - Resource Approval & Content Moderation

#### List All Resources (Admin View)
```
GET /api/resources/resources/
Authorization: Bearer <admin_token>

Query Parameters:
- status: Filter by status (pending, approved, rejected)
  GET /api/resources/resources/?status=pending
- department: Filter by department ID
- course: Filter by course ID
- semester: Filter by semester ID
- semester__year: Filter by semester year
- resource_type: Filter by type (lecture_note, assignment, etc.)
- search: Search by title
- ordering: Sort by field (-created_at, view_count, download_count)

Response:
{
  "count": 150,
  "next": "https://notenest-backend.onrender.com/api/resources/resources/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Data Structures Lecture",
      "description": "Comprehensive guide to DS",
      "file": "https://cloudinary-url.com/file.pdf",
      "tags": [
        {"id": 1, "name": "important"},
        {"id": 2, "name": "exam"}
      ],
      "uploaded_by": {
        "id": 5,
        "first_name": "John",
        "last_name": "Doe"
      },
      "department": {
        "id": 1,
        "name": "Computer Science",
        "code": "CSE"
      },
      "course": {
        "id": 3,
        "title": "Data Structures",
        "course_code": "CSE201"
      },
      "semester": {
        "id": 2,
        "name": "Fall",
        "year": 2024
      },
      "resource_type": "lecture_note",
      "status": "pending",
      "view_count": 45,
      "download_count": 12,
      "likes_count": 8,
      "comments_count": 3,
      "bookmarks_count": 2,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    },
    ...
  ]
}
```

#### Retrieve Resource for Approval
```
GET /api/resources/resources/{id}/
Authorization: Bearer <admin_token>

Response:
{
  "id": 1,
  "title": "Data Structures Lecture",
  "description": "Comprehensive guide to DS",
  "file": "https://cloudinary-url.com/file.pdf",
  "tags": [...],
  "uploaded_by": {...},
  "department": {...},
  "course": {...},
  "semester": {...},
  "resource_type": "lecture_note",
  "status": "pending",
  "view_count": 45,
  "download_count": 12,
  "likes_count": 8,
  "comments_count": 3,
  "bookmarks_count": 2,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### Approve/Reject Resource (Update Status)
```
PATCH /api/resources/resources/{id}/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "status": "approved"  // or "rejected"
}

Response (200 OK):
{
  "id": 1,
  "title": "Data Structures Lecture",
  ...
  "status": "approved",
  ...
}
```

#### Delete Resource (Admin)
```
DELETE /api/resources/resources/{id}/
Authorization: Bearer <admin_token>

Response (204 No Content)
```

---

## Moderation Module APIs

### ✅ ADMIN ONLY - Moderation Actions

#### Create Moderation Action (Approve/Reject Resource)
```
POST /api/moderation/action/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "resource": 1,
  "action": "approved",  // or "rejected"
  "reason": "Excellent resource, well structured"
}

Response (201 Created):
{
  "id": 10,
  "resource": 1,
  "moderator": {
    "id": 1,
    "first_name": "Admin",
    "last_name": "User"
  },
  "action": "approved",
  "reason": "Excellent resource, well structured",
  "created_at": "2024-01-20T15:30:00Z"
}
```

#### List All Moderation Actions
```
GET /api/moderation/action/
Authorization: Bearer <admin_token>

Query Parameters:
- action: Filter by action type (approved, rejected)
  GET /api/moderation/action/?action=rejected
- resource__status: Filter by resource status
  GET /api/moderation/action/?resource__status=approved

Response:
{
  "count": 45,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 10,
      "resource": 1,
      "moderator": {
        "id": 1,
        "first_name": "Admin",
        "last_name": "User"
      },
      "action": "approved",
      "reason": "Excellent resource, well structured",
      "created_at": "2024-01-20T15:30:00Z"
    },
    ...
  ]
}
```

#### Retrieve Moderation Action Details
```
GET /api/moderation/action/{id}/
Authorization: Bearer <admin_token>

Response:
{
  "id": 10,
  "resource": 1,
  "moderator": {...},
  "action": "approved",
  "reason": "Excellent resource, well structured",
  "created_at": "2024-01-20T15:30:00Z"
}
```

#### Update/Delete Moderation Action
```
PUT /PATCH /api/moderation/action/{id}/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "reason": "Updated reason"
}

Response (200 OK):
{
  "id": 10,
  "resource": 1,
  "moderator": {...},
  "action": "approved",
  "reason": "Updated reason",
  "created_at": "2024-01-20T15:30:00Z"
}
```

---

### ✅ ADMIN ONLY - Resource Reports Management

#### List All Resource Reports
```
GET /api/moderation/report/
Authorization: Bearer <admin_token>

Query Parameters:
- status: Filter by report status (pending, resolved, closed)
  GET /api/moderation/report/?status=pending
- resource__status: Filter by resource status

Response:
{
  "count": 23,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "resource": 5,
      "reported_by": {
        "id": 12,
        "first_name": "John",
        "last_name": "Doe"
      },
      "reason": "Inappropriate content",
      "description": "This resource contains offensive material",
      "status": "pending",
      "created_at": "2024-01-22T08:15:00Z",
      "updated_at": "2024-01-22T08:15:00Z"
    },
    ...
  ]
}
```

#### Retrieve Report Details
```
GET /api/moderation/report/{id}/
Authorization: Bearer <admin_token>

Response:
{
  "id": 1,
  "resource": 5,
  "reported_by": {
    "id": 12,
    "first_name": "John",
    "last_name": "Doe"
  },
  "reason": "Inappropriate content",
  "description": "This resource contains offensive material",
  "status": "pending",
  "created_at": "2024-01-22T08:15:00Z",
  "updated_at": "2024-01-22T08:15:00Z"
}
```

#### Update Report Status
```
PATCH /api/moderation/report/{id}/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "status": "resolved"  // or "closed", "pending"
}

Response (200 OK):
{
  "id": 1,
  "resource": 5,
  "reported_by": {...},
  "reason": "Inappropriate content",
  "description": "This resource contains offensive material",
  "status": "resolved",
  "created_at": "2024-01-22T08:15:00Z",
  "updated_at": "2024-01-25T14:45:00Z"
}
```

#### Delete Report
```
DELETE /api/moderation/report/{id}/
Authorization: Bearer <admin_token>

Response (204 No Content)
```

---

## Accounts Module APIs

### ✅ ADMIN ONLY - User Management

#### Retrieve User Details (Admin)
```
GET /api/accounts/users/{user_id}/
Authorization: Bearer <admin_token>

Response:
{
  "id": 5,
  "email": "student@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "is_staff": false,
  "is_verified": true,
  "date_joined": "2024-01-01T10:00:00Z"
}
```

#### Change User Password (Admin)
```
POST /api/accounts/change-password/
Authorization: Bearer <admin_token>
Content-Type: application/json

Request Body:
{
  "old_password": "current_password",
  "new_password": "new_password123",
  "re_new_password": "new_password123"
}

Response (200 OK):
{
  "detail": "Password changed successfully."
}
```

---

## Interactions Module APIs

### ⚠️ USER ACTIONS (For Admin Monitoring Only)

#### List All Likes
```
GET /api/interactions/like/
Authorization: Bearer <admin_token>

Response:
{
  "count": 1250,
  "next": "...",
  "previous": null,
  "results": [
    {
      "id": 100,
      "user": {
        "id": 5,
        "first_name": "John",
        "last_name": "Doe"
      },
      "resource": 1,
      "created_at": "2024-01-20T10:00:00Z"
    },
    ...
  ]
}
```

#### List All Comments
```
GET /api/interactions/comment/
Authorization: Bearer <admin_token>

Response:
{
  "count": 450,
  "next": "...",
  "previous": null,
  "results": [
    {
      "id": 50,
      "user": {
        "id": 5,
        "first_name": "John",
        "last_name": "Doe"
      },
      "resource": 1,
      "content": "Great resource!",
      "parent": null,
      "created_at": "2024-01-20T10:00:00Z",
      "updated_at": "2024-01-20T10:00:00Z"
    },
    ...
  ]
}
```

#### Delete Comment (Admin)
```
DELETE /api/interactions/comment/{id}/
Authorization: Bearer <admin_token>

Response (204 No Content)
```

#### List All Bookmarks
```
GET /api/interactions/bookmark/
Authorization: Bearer <admin_token>

Response:
{
  "count": 890,
  "next": "...",
  "previous": null,
  "results": [
    {
      "id": 180,
      "user": {
        "id": 5,
        "first_name": "John",
        "last_name": "Doe"
      },
      "resource": 1,
      "created_at": "2024-01-20T10:00:00Z"
    },
    ...
  ]
}
```

---

## Notifications Module APIs

### ⚠️ USER-SPECIFIC (Admin Cannot Modify)

#### List User Notifications
```
GET /api/notifications/
Authorization: Bearer <admin_token>

Response:
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "title": "Resource Approved",
      "message": "Your resource 'Data Structures' has been approved",
      "is_read": false,
      "created_at": "2024-01-20T10:00:00Z"
    },
    ...
  ]
}
```

---

## Response Format Standards

### Success Response (200 OK)
```json
{
  "id": 1,
  "name": "Resource Name",
  "status": "approved",
  "created_at": "2024-01-20T10:00:00Z"
}
```

### Paginated Response (List Endpoints)
```json
{
  "count": 150,
  "next": "https://notenest-backend.onrender.com/api/endpoint/?page=2",
  "previous": null,
  "results": [
    { ... },
    { ... }
  ]
}
```

### Error Response (400 Bad Request)
```json
{
  "fieldname": [
    "This field is required."
  ]
}
```

### Error Response (401 Unauthorized)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Error Response (403 Forbidden)
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Error Response (404 Not Found)
```json
{
  "detail": "Not found."
}
```

### Error Response (500 Internal Server Error)
```json
{
  "error": "Internal server error occurred"
}
```

---

## Error Handling

### Common HTTP Status Codes

| Status | Meaning | Example |
|--------|---------|---------|
| 200 | OK - Request succeeded | GET, PUT, PATCH |
| 201 | Created - Resource created | POST (successful) |
| 204 | No Content - Delete successful | DELETE |
| 400 | Bad Request - Invalid data | Invalid field values |
| 401 | Unauthorized - Missing/invalid token | No Authorization header |
| 403 | Forbidden - No permission | Non-admin user action |
| 404 | Not Found - Resource doesn't exist | Invalid ID |
| 429 | Too Many Requests - Rate limited | Exceeded rate limit |
| 500 | Server Error - Backend issue | Cloudinary connection failure |

### Validation Errors
```json
{
  "name": ["This field may not be blank."],
  "code": ["Ensure this field has at most 15 characters."],
  "department": ["Invalid pk \"999\" - object does not exist."]
}
```

### Rate Limiting
- **Resource Upload:** 10 uploads/hour per admin
- **Resource Download:** 500 downloads/hour per admin
- **Interactions:** 100 actions/hour per user
- **Admin Operations:** No explicit limit

---

## Important Notes for Admin Interface

1. **Authentication Required:** All endpoints except `/login/` require JWT token
2. **Admin-Only Operations:** Only users with `is_staff=true` can access write operations on:
   - Academic module (departments, courses, semesters)
   - Resource approval/rejection
   - Moderation actions and report management
3. **File Storage:** Files are stored in Cloudinary. URLs are permanent as long as file exists on cloud.
4. **Cascading Deletes:** 
   - Deleting a Department does NOT delete associated Courses (SET_NULL)
   - Deleting a Course does NOT delete Resources (SET_NULL)
   - Deleting a Semester does NOT delete Resources (SET_NULL)
   - Deleting a Resource cascades deletes to: Views, Likes, Comments, Bookmarks, Reports
5. **Status Workflow for Resources:**
   - New uploads start as "pending"
   - Admin can change to "approved" or "rejected"
   - Once approved, auto-visible to all users
6. **Soft/Hard Deletes:** All deletes are hard deletes (permanent removal)

---

## Quick Reference - Admin Required Endpoints

### Create
- `POST /api/academic/departments/`
- `POST /api/academic/courses/`
- `POST /api/academic/semesters/`
- `POST /api/moderation/action/`

### Update
- `PUT/PATCH /api/academic/departments/{id}/`
- `PUT/PATCH /api/academic/courses/{id}/`
- `PUT/PATCH /api/academic/semesters/{id}/`
- `PATCH /api/resources/resources/{id}/` (status update)
- `PUT/PATCH /api/moderation/action/{id}/`
- `PATCH /api/moderation/report/{id}/` (status update)

### Delete
- `DELETE /api/academic/departments/{id}/`
- `DELETE /api/academic/courses/{id}/`
- `DELETE /api/academic/semesters/{id}/`
- `DELETE /api/resources/resources/{id}/`
- `DELETE /api/moderation/action/{id}/`
- `DELETE /api/moderation/report/{id}/`
- `DELETE /api/interactions/comment/{id}/`

---

## Support & Documentation

- **OpenAPI Schema:** `GET /api/schema/`
- **Swagger UI:** `https://notenest-backend.onrender.com/api/docs/`
- **ReDoc:** `https://notenest-backend.onrender.com/api/redoc/`
- **Render Deployment:** https://notenest-backend.onrender.com/

---

**Last Updated:** January 2025
**Version:** 1.0
**Status:** Production Ready
