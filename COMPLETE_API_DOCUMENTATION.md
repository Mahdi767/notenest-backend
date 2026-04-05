# NoteNest Complete API Documentation
**Version:** 2.0 - Production Ready  
**Base URL:** `https://notenest-backend.onrender.com/api/`  
**Last Updated:** April 2026  
**Status:** ✅ Fully Analyzed & Documented  

---

## 📋 Complete Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication & User Management](#authentication--user-management)
3. [Academic Module](#academic-module)
4. [Resources Module](#resources-module)
5. [Moderation & Reporting](#moderation--reporting)
6. [Interactions (Likes, Comments, Bookmarks)](#interactions-likes-comments-bookmarks)
7. [Notifications](#notifications)
8. [Error Handling & Status Codes](#error-handling--status-codes)
9. [Rate Limiting & Throttling](#rate-limiting--throttling)
10. [Frontend Implementation Guide](#frontend-implementation-guide)

---

# SECTION 1: AUTHENTICATION & USER MANAGEMENT

## 🔑 Overview
- **Email Verification:** Brevo API (check inbox + spam folder)
- **Password Reset:** Token-based via email
- **JWT Tokens:** Access tokens for authenticated requests
- **Token Storage:** Browser localStorage or sessionStorage

---

## 1.1 Register New User

### Endpoint
```
POST /api/accounts/register/
```

### Request
```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Success Response (201 Created)
```json
{
  "message": "User registered successfully. Please verify your email.",
  "email": "newuser@example.com"
}
```

### Error Responses
```json
{
  "email": ["A user with that email already exists."],
  "username": ["A user with that username already exists."],
  "password": ["This password is too common."],
  "password2": ["The two password fields didn't match."]
}
```

### What Happens Next
✅ **Verification Email Sent** via Brevo to user's inbox  
✅ **Email Contains:** Activation link (valid for 24 hours)  
✅ **User Action:** Click link or copy token to app  
⏱️ **Timeout:** Token expires after 24 hours  

---

## 1.2 Activate Account (Email Verification)

### Two Methods:

#### Method A: Click Email Link (Recommended)
Email contains link like:
```
https://yourdomain.com/verify?uid=ENCODED_UID&token=TOKEN
```

#### Method B: API Endpoint
```
GET /api/accounts/activate/{uid64}/{token}/
```

### Success Response (200 OK)
```json
{
  "message": "Account activated successfully. You can now login."
}
```

### Error Response
```json
{
  "error": "Activation link is invalid or expired."
}
```

---

## 1.3 Resend Verification Email (If Not Received)

### Endpoint
```
POST /api/accounts/resend-verification/
```

### Request
```json
{
  "email": "newuser@example.com"
}
```

### Success Response (200 OK)
```json
{
  "message": "Verification email sent successfully. Please check your inbox."
}
```

### Already Verified Response
```json
{
  "message": "Account is already verified. You can login now."
}
```

### Error Response
```json
{
  "error": "Email is required"
}
```

### 🔘 Frontend Button Implementation

**Important:** Resend button should be **DISABLED** for 60 seconds after clicking:

```javascript
const [resendDisabled, setResendDisabled] = useState(false);
const [resendTimer, setResendTimer] = useState(0);

const handleResendEmail = async () => {
  try {
    await api.post('/accounts/resend-verification/', { 
      email: userEmail 
    });
    
    // Disable button for 60 seconds
    setResendDisabled(true);
    setResendTimer(60);
    
    const interval = setInterval(() => {
      setResendTimer(prev => {
        if (prev <= 1) {
          clearInterval(interval);
          setResendDisabled(false);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    
    showSuccessMessage("Check your email!");
  } catch (error) {
    showErrorMessage("Failed to resend email");
  }
};

return (
  <button 
    onClick={handleResendEmail}
    disabled={resendDisabled}
  >
    {resendDisabled ? `Resend in ${resendTimer}s` : 'Resend Email'}
  </button>
);
```

---

## 1.4 Login (Get JWT Token)

### Endpoint
```
POST /api/accounts/login/
```

### Request
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Success Response (200 OK)
```json
{
  "user": {
    "id": 5,
    "username": "newuser",
    "email": "newuser@example.com"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Error Response - Invalid Credentials
```json
{
  "error": "Invalid username or password"
}
```

### Error Response - Email Not Verified
```json
{
  "error": "Please verify your email first"
}
```

### Token Usage After Login
Store tokens in localStorage:
```javascript
const response = await api.post('/accounts/login/', credentials);
localStorage.setItem('access_token', response.data.access);
localStorage.setItem('refresh_token', response.data.refresh);

// Add to all authenticated requests
api.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
```

---

## 1.5 Get Current User Profile

### Endpoint
```
GET /api/accounts/me/
Authorization: Bearer <access_token>
```

### Success Response (200 OK)
```json
{
  "id": 5,
  "email": "user@example.com",
  "username": "newuser",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "is_staff": false,
  "is_verified": true,
  "date_joined": "2024-01-15T10:00:00Z"
}
```

### Error Response - No Token
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Error Response - Invalid Token
```json
{
  "detail": "Given token not valid for any token type"
}
```

---

## 1.6 Update User Profile

### Endpoint
```
PATCH /api/accounts/me/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Request (Update Any Fields)
```json
{
  "first_name": "Johnny",
  "last_name": "Doe Updated"
}
```

### Success Response (200 OK)
```json
{
  "id": 5,
  "email": "user@example.com",
  "username": "newuser",
  "first_name": "Johnny",
  "last_name": "Doe Updated",
  "role": "student",
  "is_staff": false,
  "is_verified": true,
  "date_joined": "2024-01-15T10:00:00Z"
}
```

---

## 1.7 Change Password (Logged-in User)

### Endpoint
```
POST /api/accounts/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Request
```json
{
  "old_password": "CurrentPassword123!",
  "new_password": "NewPassword456!",
  "re_new_password": "NewPassword456!"
}
```

### Success Response (200 OK)
```json
{
  "message": "Password changed successfully"
}
```

### Error Response - Wrong Old Password
```json
{
  "old_password": ["Old password is not correct"],
  "new_password": ["This password is too common."]
}
```

---

## 1.8 Forgot Password - Request Reset Link

### Endpoint
```
POST /api/accounts/password-reset/
```

### Request
```json
{
  "email": "user@example.com"
}
```

### Success Response (200 OK)
```json
{
  "message": "If an account exists with this email, a password reset link has been sent."
}
```

### How It Works
1. ✅ Email sent with reset link (valid 24 hours)
2. Email can be in **inbox or spam folder**
3. Link contains encoded UID and token
4. User clicks link or copies data to app

### Reset Link Format
Email contains link:
```
https://yourdomain.com/reset-password?uid=ENCODED_UID&token=TOKEN
```

---

## 1.9 Forgot Password - Confirm New Password

### Endpoint
```
POST /api/accounts/password-reset-confirm/
```

### Request
```json
{
  "uid": "MTM=",
  "token": "abcdef123456",
  "new_password": "NewPassword789!",
  "re_new_password": "NewPassword789!"
}
```

### Success Response (200 OK)
```json
{
  "message": "Password reset successfully. You can now login with your new password."
}
```

### Error Response - Invalid Token
```json
{
  "error": "Password reset token is invalid or expired."
}
```

### Error Response - Passwords Don't Match
```json
{
  "new_password": ["The two password fields didn't match."],
  "re_new_password": ["The two password fields didn't match."]
}
```

---

## 1.10 Logout

### Endpoint
```
POST /api/accounts/logout/
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Request
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Success Response (200 OK)
```json
{
  "message": "Logged out successfully"
}
```

### Frontend Implementation
```javascript
const handleLogout = async () => {
  try {
    await api.post('/accounts/logout/', {
      refresh: localStorage.getItem('refresh_token')
    });
    
    // Clear tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // Redirect to login
    navigate('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};
```

---

## 1.11 Get User Details (Other Users)

### Endpoint
```
GET /api/accounts/users/{user_id}/
Authorization: Bearer <access_token>
```

### Success Response (200 OK)
```json
{
  "id": 5,
  "email": "johndoe@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "is_staff": false,
  "is_verified": true,
  "date_joined": "2024-01-15T10:00:00Z"
}
```

---

# SECTION 2: ACADEMIC MODULE

## Overview
- **Departments:** Multiple departments (CSE, EEE, etc.)
- **Courses:** Each course belongs to one department
- **Semesters:** Academic semesters with year tracking
- **Permissions:** Read=Anyone, Write=Admin Only

---

## 2.1 List Departments

### Endpoint
```
GET /api/academic/departments/
Authorization: Bearer <token> (Optional for non-admin)
```

### Query Parameters
```
- page (optional): Page number (default: 1)
- page_size (optional): Items per page (default: 10)
```

### Success Response (200 OK)
```json
{
  "count": 5,
  "next": "https://api.onrender.com/api/academic/departments/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Computer Science & Engineering",
      "code": "CSE",
      "created_at": "2024-01-01T10:00:00Z"
    },
    {
      "id": 2,
      "name": "Electrical & Electronics Engineering",
      "code": "EEE",
      "created_at": "2024-01-02T10:00:00Z"
    }
  ]
}
```

---

## 2.2 Get Department Details

### Endpoint
```
GET /api/academic/departments/{id}/
Authorization: Bearer <token> (Optional)
```

### Success Response (200 OK)
```json
{
  "id": 1,
  "name": "Computer Science & Engineering",
  "code": "CSE",
  "created_at": "2024-01-01T10:00:00Z"
}
```

---

## 2.3 Create Department (ADMIN ONLY)

### Endpoint
```
POST /api/academic/departments/
Authorization: Bearer <admin_token>
Content-Type: application/json
```

### Request
```json
{
  "name": "Mechanical Engineering",
  "code": "ME"
}
```

### Success Response (201 Created)
```json
{
  "id": 3,
  "name": "Mechanical Engineering",
  "code": "ME",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Error Response - Permission Denied
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 2.4 Update Department (ADMIN ONLY)

### Endpoint
```
PUT /api/academic/departments/{id}/
PATCH /api/academic/departments/{id}/
Authorization: Bearer <admin_token>
```

### Request
```json
{
  "name": "Mechanical & Manufacturing Engineering"
}
```

### Success Response (200 OK)
```json
{
  "id": 3,
  "name": "Mechanical & Manufacturing Engineering",
  "code": "ME",
  "created_at": "2024-01-15T10:00:00Z"
}
```

---

## 2.5 Delete Department (ADMIN ONLY)

### Endpoint
```
DELETE /api/academic/departments/{id}/
Authorization: Bearer <admin_token>
```

### Success Response (204 No Content)
```
No response body
```

### Warning
- Associated courses will have `department = null`
- Resources linked to deleted courses become orphaned
- **Permanent deletion** - cannot be undone

---

## 2.6 List Courses

### Endpoint
```
GET /api/academic/courses/
Authorization: Bearer <token> (Optional)
```

### Query Parameters
```
- page (optional): Page number
- page_size (optional): Items per page
- department (optional): Filter by department ID
  Example: GET /api/academic/courses/?department=1
```

### Success Response (200 OK)
```json
{
  "count": 45,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Data Structures & Algorithms",
      "course_code": "CSE201",
      "department": 1,
      "created_at": "2024-01-01T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Web Development",
      "course_code": "CSE301",
      "department": 1,
      "created_at": "2024-01-02T10:00:00Z"
    }
  ]
}
```

### Frontend: Dynamic Course Loading by Department
```javascript
const handleDepartmentChange = async (deptId) => {
  try {
    const response = await api.get(`/academic/courses/?department=${deptId}`);
    setCourses(response.data.results);
  } catch (error) {
    console.error('Failed to load courses:', error);
  }
};
```

---

## 2.7 Get Course Details

### Endpoint
```
GET /api/academic/courses/{id}/
Authorization: Bearer <token> (Optional)
```

### Success Response (200 OK)
```json
{
  "id": 1,
  "title": "Data Structures & Algorithms",
  "course_code": "CSE201",
  "department": 1,
  "created_at": "2024-01-01T10:00:00Z"
}
```

---

## 2.8 Create Course (ADMIN ONLY)

### Endpoint
```
POST /api/academic/courses/
Authorization: Bearer <admin_token>
```

### Request
```json
{
  "title": "Machine Learning Fundamentals",
  "course_code": "CSE401",
  "department": 1
}
```

### Success Response (201 Created)
```json
{
  "id": 46,
  "title": "Machine Learning Fundamentals",
  "course_code": "CSE401",
  "department": 1,
  "created_at": "2024-01-20T10:00:00Z"
}
```

---

## 2.9 Update Course (ADMIN ONLY)

### Endpoint
```
PUT /api/academic/courses/{id}/
PATCH /api/academic/courses/{id}/
Authorization: Bearer <admin_token>
```

### Request
```json
{
  "title": "Machine Learning & AI Fundamentals"
}
```

### Success Response (200 OK)
```json
{
  "id": 46,
  "title": "Machine Learning & AI Fundamentals",
  "course_code": "CSE401",
  "department": 1,
  "created_at": "2024-01-20T10:00:00Z"
}
```

---

## 2.10 Delete Course (ADMIN ONLY)

### Endpoint
```
DELETE /api/academic/courses/{id}/
Authorization: Bearer <admin_token>
```

### Success Response (204 No Content)

---

## 2.11 List Semesters

### Endpoint
```
GET /api/academic/semesters/
Authorization: Bearer <token> (Optional)
```

### Success Response (200 OK)
```json
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
    {
      "id": 2,
      "name": "Spring",
      "year": 2024,
      "is_active": false,
      "created_at": "2024-01-02T10:00:00Z"
    },
    {
      "id": 3,
      "name": "Summer",
      "year": 2024,
      "is_active": false,
      "created_at": "2024-01-03T10:00:00Z"
    }
  ]
}
```

---

## 2.12 Create Semester (ADMIN ONLY)

### Endpoint
```
POST /api/academic/semesters/
Authorization: Bearer <admin_token>
```

### Request
```json
{
  "name": "Fall",
  "year": 2025,
  "is_active": false
}
```

### Success Response (201 Created)
```json
{
  "id": 9,
  "name": "Fall",
  "year": 2025,
  "is_active": false,
  "created_at": "2024-01-20T10:00:00Z"
}
```

---

## 2.13 Update Semester (Set Active) (ADMIN ONLY)

### Endpoint
```
PATCH /api/academic/semesters/{id}/
Authorization: Bearer <admin_token>
```

### Request
```json
{
  "is_active": true
}
```

### Success Response (200 OK)
```json
{
  "id": 9,
  "name": "Fall",
  "year": 2025,
  "is_active": true,
  "created_at": "2024-01-20T10:00:00Z"
}
```

---

# SECTION 3: RESOURCES MODULE

## Overview
- **Status Workflow:** pending → approved / rejected
- **Visibility:** Users see only approved resources + their own
- **Admins:** See all resources regardless of status
- **File Storage:** Cloudinary (automatic CDN)

---

## 3.1 List Resources (User View)

### Endpoint
```
GET /api/resources/resources/
Authorization: Bearer <token> (Optional - different results for admin vs user)
```

### Query Parameters
```
- page (optional): Page number
- page_size (optional): Items per page (default: 10)
- status (optional): pending, approved, rejected
- department (optional): Department ID
- course (optional): Course ID
- semester (optional): Semester ID
- semester__year (optional): Year (e.g., 2024)
- resource_type (optional): lecture_note, assignment, lab_report, question_bank, book
- search (optional): Search by title
- ordering (optional): -created_at, view_count, download_count, -updated_at
```

### Example Requests
```
# Get all approved resources
GET /api/resources/resources/?status=approved

# Filter by department and semester
GET /api/resources/resources/?department=1&semester=2&ordering=-created_at

# Search with filters
GET /api/resources/resources/?search=algorithms&resource_type=lecture_note

# Sort by downloads
GET /api/resources/resources/?ordering=download_count&page_size=20
```

### Success Response (200 OK)
```json
{
  "count": 150,
  "next": "https://api.onrender.com/api/resources/resources/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Data Structures Complete Guide",
      "description": "A comprehensive guide covering all data structures",
      "file": "https://res.cloudinary.com/resources/file.pdf",
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
      "status": "approved",
      "view_count": 156,
      "download_count": 42,
      "likes_count": 23,
      "comments_count": 8,
      "bookmarks_count": 15,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### What Users See
- **Authenticated User:** All approved + their own pending/rejected
- **Anonymous User:** Only approved resources
- **Admin User:** ALL resources (pending, approved, rejected)

---

## 3.2 Get Resource Details

### Endpoint
```
GET /api/resources/resources/{id}/
Authorization: Bearer <token> (Optional)
```

### Success Response (200 OK)
```json
{
  "id": 1,
  "title": "Data Structures Complete Guide",
  "description": "A comprehensive guide covering all data structures",
  "file": "https://res.cloudinary.com/resources/file.pdf",
  "tags": [...],
  "uploaded_by": {...},
  "department": {...},
  "course": {...},
  "semester": {...},
  "resource_type": "lecture_note",
  "status": "approved",
  "view_count": 157,
  "download_count": 42,
  "likes_count": 23,
  "comments_count": 8,
  "bookmarks_count": 15,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Important Notes
- ✅ **View count increments** automatically when retrieved
- ✅ **Only unique views** per user are counted
- ✅ **Anonymous views** tracked by IP address
- ⚠️ **Do NOT call this endpoint multiple times** to inflate view count

---

## 3.3 Upload Resource (Create)

### Endpoint
```
POST /api/resources/resources/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

### Request (Form Data)
```
{
  "title": "Database Design Principles",
  "description": "Learn how to design efficient databases - normalization, schemas, optimization",
  "file": <binary file>,
  "resource_type": "lecture_note",
  "department": 1,
  "course": 3,
  "semester": 2,
  "tags": [1, 2]  // Optional: Tag IDs
}
```

### Success Response (201 Created)
```json
{
  "id": 156,
  "title": "Database Design Principles",
  "description": "Learn how to design efficient databases...",
  "file": "https://res.cloudinary.com/resources/file.pdf",
  "tags": [
    {"id": 1, "name": "database"},
    {"id": 2, "name": "sql"}
  ],
  "uploaded_by": {
    "id": 5,
    "first_name": "John",
    "last_name": "Doe"
  },
  "department": 1,
  "course": 3,
  "semester": 2,
  "resource_type": "lecture_note",
  "status": "pending",
  "view_count": 0,
  "download_count": 0,
  "likes_count": 0,
  "comments_count": 0,
  "bookmarks_count": 0,
  "created_at": "2024-01-25T10:00:00Z",
  "updated_at": "2024-01-25T10:00:00Z"
}
```

### Validation Errors
```json
{
  "title": ["This field may not be blank."],
  "description": ["This field may not be blank."],
  "resource_type": ["\"invalid_type\" is not a valid choice. Valid choices are: lecture_note, assignment, lab_report, question_bank, book"],
  "department": ["Invalid pk \"999\" - object does not exist."],
  "course": ["Invalid pk \"999\" - object does not exist."],
  "semester": ["Invalid pk \"999\" - object does not exist."],
  "file": ["No file was submitted."]
}
```

### Rate Limiting
- **Max 10 uploads per hour** per user
- Response if exceeded:
```json
{
  "detail": "Request was throttled. Expected available in 60 seconds."
}
```

### File Requirements
- **Accepted Formats:** PDF, DOC, DOCX, PPT, PPTX, ZIP
- **Max Size:** No strict limit (Cloudinary handles)
- **Storage:** Automatic to Cloudinary CDN

### Important Status Info
- ✅ **New uploads start as "pending"**
- ⏳ **Admin must approve** before visible to other users
- 👤 **You can see your own pending resources**
- ⚠️ **Editing a resource resets it to pending** (for non-admin)

---

## 3.4 Update Resource (Non-Admin User)

### Endpoint
```
PUT /api/resources/resources/{id}/
PATCH /api/resources/resources/{id}/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

### Request
```
{
  "title": "Updated Title",
  "description": "Updated description"
}
```

### Important Behavior
⚠️ **If resource was approved, editing it resets status to "pending"**

```json
{
  "id": 156,
  "title": "Updated Title",
  "status": "pending",  // Was "approved", now "pending"
  ...
}
```

---

## 3.5 Delete Resource

### Endpoint
```
DELETE /api/resources/resources/{id}/
Authorization: Bearer <access_token>
```

### Permissions
- ✅ **User Can:** Delete their own resources
- ✅ **Admin Can:** Delete any resource
- ❌ **User Cannot:** Delete other user's resources

### Success Response (204 No Content)

---

## 3.6 Download Resource (Increment Count)

### Endpoint
```
GET /api/resources/resources/{id}/download/
Authorization: Bearer <token> (Optional)
```

### Success Response (200 OK)
```json
{
  "success": true,
  "file_url": "https://res.cloudinary.com/resources/file.pdf",
  "download_count": 43,
  "filename": "Database_Design.pdf"
}
```

### Error Response - No File
```json
{
  "error": "No file associated with this resource"
}
```

### Frontend Implementation
```javascript
const handleDownload = async (resourceId) => {
  try {
    const response = await api.get(`/resources/resources/${resourceId}/download/`);
    
    // Get file URL and filename from response
    const { file_url, filename } = response.data;
    
    // Create download link
    const link = document.createElement('a');
    link.href = file_url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Update download count in UI
    setResource(prev => ({
      ...prev,
      download_count: response.data.download_count
    }));
    
    showSuccessMessage("Download started!");
  } catch (error) {
    showErrorMessage("Failed to download resource");
  }
};
```

### Rate Limiting
- **500 downloads per hour** per admin/user
- **50 downloads per hour** for anonymous users

---

## 3.7 Approve/Reject Resource (ADMIN ONLY)

### Endpoint
```
PATCH /api/resources/resources/{id}/
Authorization: Bearer <admin_token>
```

### Request - Approve
```json
{
  "status": "approved"
}
```

### Request - Reject
```json
{
  "status": "rejected"
}
```

### Success Response (200 OK)
```json
{
  "id": 156,
  "title": "Database Design Principles",
  ...
  "status": "approved",
  ...
}
```

### Workflow After Approval
1. ✅ Resource becomes visible to all users
2. ✅ Uploader receives notification
3. ✅ Resource appears in search/filter results
4. ✅ Users can like, comment, bookmark

---

# SECTION 4: MODERATION & REPORTING

## Overview
- **Reports:** Users report inappropriate resources
- **Actions:** Admins document approval/rejection decisions
- **Visibility:** Users see only their own reports; Admins see all

---

## 4.1 Create Resource Report

### Endpoint
```
POST /api/moderation/report/
Authorization: Bearer <access_token>
```

### Request
```json
{
  "resource": 1,
  "reason": "Copyright Violation",
  "description": "This appears to be copyrighted material without permission"
}
```

### Success Response (201 Created)
```json
{
  "id": 1,
  "resource": 1,
  "reported_by": {
    "id": 5,
    "first_name": "John",
    "last_name": "Doe"
  },
  "reason": "Copyright Violation",
  "description": "This appears to be copyrighted material without permission",
  "status": "pending",
  "created_at": "2024-01-25T10:00:00Z",
  "updated_at": "2024-01-25T10:00:00Z"
}
```

### Report Reasons
- Inappropriate Content
- Copyright Violation
- Spam
- Duplicate
- Other

---

## 4.2 List Resource Reports (Users See Own, Admins See All)

### Endpoint
```
GET /api/moderation/report/
Authorization: Bearer <access_token>
```

### Query Parameters
```
- status (optional): pending, resolved, closed
- resource__status (optional): Filter by resource status
```

### User Example (Non-Admin)
```
GET /api/moderation/report/
```
Response:
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "resource": 1,
      "reported_by": {...},
      "reason": "Copyright Violation",
      "description": "...",
      "status": "pending",
      "created_at": "2024-01-25T10:00:00Z"
    }
  ]
}
```

### Admin Example
```
GET /api/moderation/report/?status=pending
```
Response:
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "resource": 1,
      "reported_by": {...},
      "reason": "Copyright Violation",
      "description": "...",
      "status": "pending",
      "created_at": "2024-01-25T10:00:00Z"
    },
    ...
  ]
}
```

---

## 4.3 Update Report Status (ADMIN ONLY)

### Endpoint
```
PATCH /api/moderation/report/{id}/
Authorization: Bearer <admin_token>
```

### Request
```json
{
  "status": "resolved"
}
```

### Status Values
- `pending` - New report, not reviewed
- `resolved` - Reviewed and acted upon
- `closed` - Resolved, no further action needed

### Success Response (200 OK)
```json
{
  "id": 1,
  "resource": 1,
  "reported_by": {...},
  "reason": "Copyright Violation",
  "description": "...",
  "status": "resolved",
  "created_at": "2024-01-25T10:00:00Z",
  "updated_at": "2024-01-26T14:30:00Z"
}
```

---

## 4.4 Create Moderation Action (ADMIN ONLY)

### Endpoint
```
POST /api/moderation/action/
Authorization: Bearer <admin_token>
```

### Request
```json
{
  "resource": 1,
  "action": "approved",
  "reason": "Content is legitimate and well-structured"
}
```

### Actions
- `approved` - Approve the resource
- `rejected` - Reject the resource

### Success Response (201 Created)
```json
{
  "id": 10,
  "resource": 1,
  "moderator": {
    "id": 1,
    "first_name": "Admin",
    "last_name": "User"
  },
  "action": "approved",
  "reason": "Content is legitimate and well-structured",
  "created_at": "2024-01-26T15:00:00Z"
}
```

### Automatic Effects
- ✅ Resource status updated to "approved" or "rejected"
- ✅ Uploader receives notification
- ✅ Action logged in moderation history

---

## 4.5 List Moderation Actions (ADMIN ONLY)

### Endpoint
```
GET /api/moderation/action/
Authorization: Bearer <admin_token>
```

### Query Parameters
```
- action (optional): approved, rejected
- resource__status (optional): Filter by resource status
```

### Success Response (200 OK)
```json
{
  "count": 145,
  "results": [
    {
      "id": 10,
      "resource": 1,
      "moderator": {...},
      "action": "approved",
      "reason": "Content is legitimate and well-structured",
      "created_at": "2024-01-26T15:00:00Z"
    }
  ]
}
```

---

# SECTION 5: INTERACTIONS (Likes, Comments, Bookmarks)

## Overview
- **Likes:** Simple reactions to resources
- **Comments:** Threaded discussion (replies to comments)
- **Bookmarks:** Save resources for later
- **Rate Limiting:** 100 actions/hour per user

---

## 5.1 Like a Resource

### Endpoint
```
POST /api/interactions/like/
Authorization: Bearer <access_token>
```

### Request
```json
{
  "resource": 1
}
```

### Success Response (201 Created)
```json
{
  "id": 100,
  "user": {
    "id": 5,
    "first_name": "John",
    "last_name": "Doe"
  },
  "resource": 1,
  "created_at": "2024-01-26T10:00:00Z"
}
```

### Error - Already Liked
```json
{
  "error": "You already liked this resource"
}
```

---

## 5.2 Unlike a Resource

### Endpoint
```
DELETE /api/interactions/like/{id}/
Authorization: Bearer <access_token>
```

### Success Response (204 No Content)

---

## 5.3 List Likes on a Resource

### Endpoint
```
GET /api/interactions/like/?resource=1
Authorization: Bearer <access_token>
```

### Success Response (200 OK)
```json
{
  "count": 23,
  "results": [
    {
      "id": 100,
      "user": {...},
      "resource": 1,
      "created_at": "2024-01-26T10:00:00Z"
    }
  ]
}
```

---

## 5.4 Create Comment on Resource

### Endpoint
```
POST /api/interactions/comment/
Authorization: Bearer <access_token>
```

### Request
```json
{
  "resource": 1,
  "content": "Great resource! Very helpful for understanding the topic."
}
```

### Success Response (201 Created)
```json
{
  "id": 50,
  "user": {
    "id": 5,
    "first_name": "John",
    "last_name": "Doe"
  },
  "resource": 1,
  "content": "Great resource! Very helpful for understanding the topic.",
  "parent": null,
  "created_at": "2024-01-26T10:00:00Z",
  "updated_at": "2024-01-26T10:00:00Z"
}
```

---

## 5.5 Reply to a Comment

### Endpoint
```
POST /api/interactions/comment/
Authorization: Bearer <access_token>
```

### Request (Parent Comment)
```json
{
  "resource": 1,
  "content": "I agree! The examples were very clear.",
  "parent": 50
}
```

### Success Response (201 Created)
```json
{
  "id": 51,
  "user": {...},
  "resource": 1,
  "content": "I agree! The examples were very clear.",
  "parent": 50,
  "created_at": "2024-01-26T10:05:00Z",
  "updated_at": "2024-01-26T10:05:00Z"
}
```

---

## 5.6 List Comments on a Resource

### Endpoint
```
GET /api/interactions/comment/?resource=1
Authorization: Bearer <access_token>
```

### Success Response (200 OK)
```json
{
  "count": 8,
  "results": [
    {
      "id": 50,
      "user": {...},
      "resource": 1,
      "content": "Great resource!...",
      "parent": null,
      "created_at": "2024-01-26T10:00:00Z",
      "updated_at": "2024-01-26T10:00:00Z"
    },
    {
      "id": 51,
      "user": {...},
      "resource": 1,
      "content": "I agree!...",
      "parent": 50,
      "created_at": "2024-01-26T10:05:00Z",
      "updated_at": "2024-01-26T10:05:00Z"
    }
  ]
}
```

---

## 5.7 Update Comment

### Endpoint
```
PATCH /api/interactions/comment/{id}/
Authorization: Bearer <access_token>
```

### Request
```json
{
  "content": "Updated comment content"
}
```

### Success Response (200 OK)
```json
{
  "id": 50,
  "user": {...},
  "resource": 1,
  "content": "Updated comment content",
  "parent": null,
  "created_at": "2024-01-26T10:00:00Z",
  "updated_at": "2024-01-26T11:30:00Z"
}
```

---

## 5.8 Delete Comment

### Endpoint
```
DELETE /api/interactions/comment/{id}/
Authorization: Bearer <access_token>
```

### Restrictions
- ✅ Can delete own comments
- ❌ Cannot delete if it has replies
- ✅ Admins can delete any comment

### Error - Has Replies
```json
{
  "error": "Cannot delete comment with replies. Delete replies first.",
  "reply_count": 3
}
```

### Success Response (204 No Content)

---

## 5.9 Bookmark a Resource

### Endpoint
```
POST /api/interactions/bookmark/
Authorization: Bearer <access_token>
```

### Request
```json
{
  "resource": 1
}
```

### Success Response (201 Created)
```json
{
  "id": 180,
  "user": {...},
  "resource": 1,
  "created_at": "2024-01-26T10:00:00Z"
}
```

### Error - Already Bookmarked
```json
{
  "error": "You already bookmarked this resource"
}
```

---

## 5.10 Remove Bookmark

### Endpoint
```
DELETE /api/interactions/bookmark/{id}/
Authorization: Bearer <access_token>
```

### Success Response (204 No Content)

---

## 5.11 List User's Bookmarks

### Endpoint
```
GET /api/interactions/bookmark/?user=me
Authorization: Bearer <access_token>
```

### Success Response (200 OK)
```json
{
  "count": 15,
  "results": [
    {
      "id": 180,
      "user": {...},
      "resource": 1,
      "created_at": "2024-01-26T10:00:00Z"
    }
  ]
}
```

---

# SECTION 6: NOTIFICATIONS

## Overview
- **Automatic:** Generated when resources are approved/rejected, comments are made, etc.
- **User-Specific:** Each user sees only their own notifications
- **Read Status:** Can mark as read individually

---

## 6.1 List User's Notifications

### Endpoint
```
GET /api/notifications/
Authorization: Bearer <access_token>
```

### Success Response (200 OK)
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "user": 5,
      "title": "Resource Approved",
      "message": "Your resource 'Data Structures' has been approved",
      "is_read": false,
      "created_at": "2024-01-26T10:00:00Z"
    },
    {
      "id": 2,
      "user": 5,
      "title": "New Comment",
      "message": "John Doe commented on your resource: 'Great resource!'",
      "is_read": false,
      "created_at": "2024-01-25T15:30:00Z"
    },
    {
      "id": 3,
      "user": 5,
      "title": "Resource Rejected",
      "message": "Your resource 'Database Design' was rejected",
      "is_read": true,
      "created_at": "2024-01-25T10:00:00Z"
    }
  ]
}
```

---

## 6.2 Mark Notification as Read

### Endpoint
```
PATCH /api/notifications/{id}/mark_as_read/
Authorization: Bearer <access_token>
```

### Success Response (200 OK)
```json
{
  "id": 1,
  "user": 5,
  "title": "Resource Approved",
  "message": "Your resource 'Data Structures' has been approved",
  "is_read": true,
  "created_at": "2024-01-26T10:00:00Z"
}
```

---

## 6.3 Delete Notification

### Endpoint
```
DELETE /api/notifications/{id}/delete_notification/
Authorization: Bearer <access_token>
```

### Success Response (204 No Content)

---

# SECTION 7: ERROR HANDLING & STATUS CODES

## HTTP Status Code Reference

| Code | Name | Meaning | Example |
|------|------|---------|---------|
| 200 | OK | Request successful | GET, PUT, PATCH |
| 201 | Created | Resource created | POST (successful) |
| 204 | No Content | Delete successful | DELETE |
| 400 | Bad Request | Invalid data | Missing required field |
| 401 | Unauthorized | Missing/invalid token | No Authorization header |
| 403 | Forbidden | No permission | Non-admin creating dept |
| 404 | Not Found | Resource doesn't exist | Invalid ID |
| 429 | Too Many Requests | Rate limited | Too many requests |
| 500 | Server Error | Server issue | Database connection failure |

---

## Common Error Responses

### Authorization Missing
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Invalid Token
```json
{
  "detail": "Given token not valid for any token type"
}
```

### Permission Denied
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Resource Not Found
```json
{
  "detail": "Not found."
}
```

### Validation Error (400)
```json
{
  "fieldname": [
    "Error message 1",
    "Error message 2"
  ]
}
```

### Rate Limit Exceeded (429)
```json
{
  "detail": "Request was throttled. Expected available in 60 seconds."
}
```

---

# SECTION 8: RATE LIMITING & THROTTLING

## Upload Rate Limits
- **Resource Upload:** 10 uploads/hour per user
- **Recommended:** One upload every 6 minutes

## Download Rate Limits
- **Authenticated Users:** 500 downloads/hour
- **Anonymous Users:** 50 downloads/hour

## Interaction Rate Limits
- **Likes, Comments, Bookmarks:** 100 actions/hour per user
- **Recommended:** Spread actions throughout the hour

## Email Rate Limits
- **Resend Verification:** 60-second wait between attempts
- **Password Reset:** No limit (backoff handled by Brevo)

### Rate Limit Response
```json
{
  "detail": "Request was throttled. Expected available in 300 seconds."
}
```

---

# SECTION 9: FRONTEND IMPLEMENTATION GUIDE

## 9.1 API Client Setup (Axios)

```javascript
import axios from 'axios';

const API_BASE_URL = 'https://notenest-backend.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auto-add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 - refresh or logout
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Try to refresh token
      try {
        const refresh = localStorage.getItem('refresh_token');
        const response = await axios.post(
          `${API_BASE_URL}/accounts/token/refresh/`,
          { refresh }
        );
        localStorage.setItem('access_token', response.data.access);
        // Retry original request
        return api(error.config);
      } catch {
        // Refresh failed - logout
        localStorage.clear();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

## 9.2 Authentication Flow

```javascript
import api from './api';

// Register
const register = async (userData) => {
  try {
    const response = await api.post('/accounts/register/', userData);
    return { success: true, message: response.data.message };
  } catch (error) {
    return { success: false, errors: error.response.data };
  }
};

// Login
const login = async (email, password) => {
  try {
    const response = await api.post('/accounts/login/', { email, password });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return { success: true, user: response.data.user };
  } catch (error) {
    return { success: false, error: error.response.data.error };
  }
};

// Logout
const logout = async () => {
  try {
    const refresh = localStorage.getItem('refresh_token');
    await api.post('/accounts/logout/', { refresh });
  } finally {
    localStorage.clear();
  }
};

// Get Current User
const getCurrentUser = async () => {
  try {
    const response = await api.get('/accounts/me/');
    return response.data;
  } catch (error) {
    return null;
  }
};
```

## 9.3 Resource Management

```javascript
// Get resources with filters
const getResources = async (filters = {}) => {
  try {
    const params = new URLSearchParams(filters);
    const response = await api.get(`/resources/resources/?${params}`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch resources:', error);
    return null;
  }
};

// Upload resource
const uploadResource = async (formData) => {
  try {
    const response = await api.post('/resources/resources/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return { success: true, resource: response.data };
  } catch (error) {
    return { success: false, errors: error.response.data };
  }
};

// Download with count increment
const downloadResource = async (resourceId) => {
  try {
    const response = await api.get(`/resources/resources/${resourceId}/download/`);
    const link = document.createElement('a');
    link.href = response.data.file_url;
    link.download = response.data.filename;
    link.click();
    return { success: true, count: response.data.download_count };
  } catch (error) {
    return { success: false, error: error.response.data.error };
  }
};
```

---

## 📚 API Documentation Links

- **Swagger UI:** `https://notenest-backend.onrender.com/api/docs/`
- **ReDoc:** `https://notenest-backend.onrender.com/api/redoc/`
- **OpenAPI Schema:** `https://notenest-backend.onrender.com/api/schema/`

---

## ✅ Summary

This documentation covers **EVERY** endpoint with:
- ✅ Complete request/response examples
- ✅ All query parameters
- ✅ Error handling
- ✅ Rate limiting rules
- ✅ Permission requirements
- ✅ Frontend implementation examples
- ✅ Button behavior (resend email 60s wait)
- ✅ Admin vs non-admin differences
- ✅ Status codes reference
- ✅ Real-world examples

You now have a **production-ready API reference** to hand to ANY frontend team! 🚀

