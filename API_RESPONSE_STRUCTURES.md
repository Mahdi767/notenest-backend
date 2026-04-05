# NoteNest API Response Structures & Data Models

**Backend URL:** `https://notenest-backend-hd5r.onrender.com`

**Last Updated:** April 4, 2026

---

## 📋 API RESPONSE STRUCTURES (ACTUAL LIVE DATA)

This document contains the exact response structures from the NoteNest backend APIs. Use this to understand data models and dynamic rendering patterns.

---

## 🔍 RESOURCES ENDPOINT

### Base GET /api/resources/resources/

**Endpoint:** `GET /api/resources/resources/`

**Authentication:** Optional (Bearer token affects visibility)

**Access Level:** Everyone can view, but filtering depends on user role

**Response Structure:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 14,
            "title": "Software Engineering and Design Pattern",
            "description": "Lorem Ipsum is simply dummy text...",
            "resource_type": "assignment",
            "status": "pending",
            "file": "https://res.cloudinary.com/dwowbxgjs/image/upload/v1/resources/mpoojka7ftjucxd3re4z",
            "view_count": 1,
            "download_count": 0,
            "likes_count": 1,
            "comments_count": 4,
            "bookmarks_count": 0,
            "created_at": "2026-03-31T14:48:31.398399Z",
            "updated_at": "2026-03-31T16:02:07.609468Z",
            "uploaded_by": {
                "id": 48,
                "first_name": "Test",
                "last_name": "Mehedi"
            },
            "department": {
                "id": 6,
                "name": "Computer Science & Engineering",
                "code": "CSE",
                "created_at": "2026-03-25T06:55:30.514678Z"
            },
            "course": {
                "id": 8,
                "title": "Software Engineering & Design Pattern",
                "course_code": "CSE417",
                "department": {
                    "id": 6,
                    "name": "Computer Science & Engineering",
                    "code": "CSE",
                    "created_at": "2026-03-25T06:55:30.514678Z"
                },
                "created_at": "2026-03-25T07:01:27.488221Z"
            },
            "semester": {
                "id": 15,
                "name": "Summer",
                "year": 2026,
                "is_active": false,
                "created_at": "2026-03-25T07:31:27.606393Z"
            },
            "tags": [
                {
                    "id": 2,
                    "name": "Programming"
                },
                {
                    "id": 3,
                    "name": "Python"
                },
                {
                    "id": 4,
                    "name": "Java"
                },
                {
                    "id": 5,
                    "name": "C++"
                },
                {
                    "id": 6,
                    "name": "C"
                },
                {
                    "id": 7,
                    "name": "JavaScript"
                },
                {
                    "id": 8,
                    "name": "Data Structures"
                }
            ]
        }
    ]
}
```

**Query Parameters:**
- `department` (int): Filter by department ID
- `course` (int): Filter by course ID
- `semester` (int): Filter by semester ID
- `resource_type` (string): notes, assignment, lab_report, question_bank, textbook
- `search` (string): Search by title or description
- `ordering` (string): -created_at, -view_count, -download_count, -likes_count
- `page` (int): Page number (default: 1)

**Frontend Data Points to Display:**
```javascript
{
  id,                    // Resource unique ID
  title,                 // Resource name
  description,           // Long description
  resource_type,         // Type badge
  status,                // Approval status (pending, approved, rejected)
  file,                  // Download link
  view_count,            // Number of views
  likes_count,           // Number of likes
  comments_count,        // Number of comments
  bookmarks_count,       // Number of bookmarks
  created_at,            // Upload date
  uploaded_by: {         // Author info
    id,
    first_name,
    last_name
  },
  department: {          // Department info
    id,
    name,
    code
  },
  course: {              // Course info
    id,
    title,
    course_code
  },
  semester: {            // Semester info
    id,
    name,
    year,
    is_active
  },
  tags: []               // Array of tags
}
```

---

## 🏢 ACADEMIC ENDPOINTS

### 1. GET /api/academic/departments/

**Endpoint:** `GET /api/academic/departments/`

**Access Level:** Public (No authentication required)

**Response Structure:**
```json
{
    "count": 9,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "English",
            "code": "ENG",
            "created_at": "2026-03-25T06:55:30.514678Z"
        },
        {
            "id": 2,
            "name": "Journalism & Media Studies",
            "code": "JMS",
            "created_at": "2026-03-25T06:55:30.514678Z"
        },
        {
            "id": 3,
            "name": "Law & Justice",
            "code": "LAW",
            "created_at": "2026-03-25T06:55:30.514678Z"
        },
        {
            "id": 4,
            "name": "Business Administration",
            "code": "BBA",
            "created_at": "2026-03-25T06:55:30.514678Z"
        },
        {
            "id": 5,
            "name": "Economics",
            "code": "ECO",
            "created_at": "2026-03-25T06:55:30.514678Z"
        },
        {
            "id": 6,
            "name": "Computer Science & Engineering",
            "code": "CSE",
            "created_at": "2026-03-25T06:55:30.514678Z"
        },
        {
            "id": 7,
            "name": "Software Engineering",
            "code": "SWE",
            "created_at": "2026-03-25T06:55:30.514678Z"
        },
        {
            "id": 8,
            "name": "Electrical & Electronic Engineering",
            "code": "EEE",
            "created_at": "2026-03-25T06:55:30.514678Z"
        },
        {
            "id": 9,
            "name": "Data Science",
            "code": "DS",
            "created_at": "2026-03-25T06:55:30.514678Z"
        }
    ]
}
```

**Use Case:** Populate department dropdown/list

**Frontend Pattern:**
```javascript
departments.map(dept => ({
  value: dept.id,
  label: `${dept.name} (${dept.code})`
}))
```

---

### 2. GET /api/academic/courses/

**Endpoint:** `GET /api/academic/courses/`

**Access Level:** Public (No authentication required)

**Pagination:** Yes (10 per page, see `next` URL)

**Response Structure:**
```json
{
    "count": 34,
    "next": "https://notenest-backend-hd5r.onrender.com/api/academic/courses/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Computer Graphics & Image Processing",
            "course_code": "CSE401",
            "department": {
                "id": 6,
                "name": "Computer Science & Engineering",
                "code": "CSE",
                "created_at": "2026-03-25T06:55:30.514678Z"
            },
            "created_at": "2026-03-25T07:01:27.488221Z"
        },
        {
            "id": 2,
            "title": "Computer Graphics & Image Processing Lab",
            "course_code": "CSE402",
            "department": {
                "id": 6,
                "name": "Computer Science & Engineering",
                "code": "CSE",
                "created_at": "2026-03-25T06:55:30.514678Z"
            },
            "created_at": "2026-03-25T07:01:27.488221Z"
        },
        {
            "id": 3,
            "title": "Technical Writing and Presentation",
            "course_code": "CSE429",
            "department": {
                "id": 6,
                "name": "Computer Science & Engineering",
                "code": "CSE",
                "created_at": "2026-03-25T06:55:30.514678Z"
            },
            "created_at": "2026-03-25T07:01:27.488221Z"
        },
        {
            "id": 4,
            "title": "Final Year Project/Thesis/Internship",
            "course_code": "CSE435",
            "department": {
                "id": 6,
                "name": "Computer Science & Engineering",
                "code": "CSE",
                "created_at": "2026-03-25T06:55:30.514678Z"
            },
            "created_at": "2026-03-25T07:01:27.488221Z"
        },
        {
            "id": 5,
            "title": "Final Year Project/Thesis/Internship",
            "course_code": "CSE436",
            "department": {
                "id": 6,
                "name": "Computer Science & Engineering",
                "code": "CSE",
                "created_at": "2026-03-25T06:55:30.514678Z"
            },
            "created_at": "2026-03-25T07:01:27.488221Z"
        }
    ]
}
```

**Query Parameters:**
- `department` (int): Filter by department ID
- `page` (int): Page number

**Frontend Pattern:**
```javascript
courses.map(course => ({
  value: course.id,
  label: `${course.course_code} - ${course.title}`,
  department: course.department.name
}))
```

---

### 3. GET /api/academic/semesters/

**Endpoint:** `GET /api/academic/semesters/`

**Access Level:** Admin Only ⚠️

**Note:** This is admin-only endpoint. Requires authentication with admin/staff role.

**Response Structure:**
```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 9,
            "name": "Spring",
            "year": 2024,
            "is_active": false,
            "created_at": "2026-03-25T07:31:27.606393Z"
        },
        {
            "id": 10,
            "name": "Summer",
            "year": 2024,
            "is_active": false,
            "created_at": "2026-03-25T07:31:27.606393Z"
        },
        {
            "id": 11,
            "name": "Spring",
            "year": 2025,
            "is_active": false,
            "created_at": "2026-03-25T07:31:27.606393Z"
        },
        {
            "id": 12,
            "name": "Summer",
            "year": 2025,
            "is_active": false,
            "created_at": "2026-03-25T07:31:27.606393Z"
        },
        {
            "id": 13,
            "name": "Autumn",
            "year": 2025,
            "is_active": false,
            "created_at": "2026-03-25T07:31:27.606393Z"
        },
        {
            "id": 14,
            "name": "Spring",
            "year": 2026,
            "is_active": false,
            "created_at": "2026-03-25T07:31:27.606393Z"
        },
        {
            "id": 15,
            "name": "Summer",
            "year": 2026,
            "is_active": false,
            "created_at": "2026-03-25T07:31:27.606393Z"
        },
        {
            "id": 16,
            "name": "Autumn",
            "year": 2026,
            "is_active": false,
            "created_at": "2026-03-25T07:31:27.606393Z"
        }
    ]
}
```

**Query Parameters:**
- `is_active` (bool): Filter by active/inactive semesters

**Frontend Pattern (Admin Panel):**
```javascript
semesters.map(sem => ({
  value: sem.id,
  label: `${sem.name} ${sem.year}`,
  isActive: sem.is_active,
  status: sem.is_active ? 'Active' : 'Inactive'
}))
```

---

## 💬 INTERACTIONS ENDPOINTS

### 1. GET /api/interactions/like/

**Endpoint:** `GET /api/interactions/like/`

**Authentication:** Required (Bearer token)

**Access Level:** Authenticated users (see all likes on system OR only their own)

**Response Structure:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "user": 47,
            "resource": 14,
            "created_at": "2026-03-31T15:24:59.285525Z"
        }
    ]
}
```

**Frontend Usage:**
```javascript
// Check if current user liked a resource
const isLiked = likes.some(like => like.user === currentUserId && like.resource === resourceId);

// Show like count
const likeCount = resourceData.likes_count;
```

---

### 2. GET /api/interactions/comment/

**Endpoint:** `GET /api/interactions/comment/`

**Authentication:** Required (Bearer token)

**Access Level:** Authenticated users (view all comments)

**Note:** Server-side filtering by resource not implemented. Filter client-side by `resource` field.

**Response Structure:**
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 8,
            "resource": 14,
            "user": 47,
            "content": "Nice.. PDF",
            "created_at": "2026-03-31T15:27:11.994894Z",
            "parent": null
        },
        {
            "id": 9,
            "resource": 14,
            "user": 47,
            "content": "Nice.. PDF",
            "created_at": "2026-03-31T15:29:52.144776Z",
            "parent": null
        },
        {
            "id": 10,
            "resource": 14,
            "user": 47,
            "content": "Nice.. PDF",
            "created_at": "2026-03-31T15:31:43.560838Z",
            "parent": null
        },
        {
            "id": 11,
            "resource": 14,
            "user": 47,
            "content": "Nice.. PDF",
            "created_at": "2026-03-31T15:33:01.689197Z",
            "parent": null
        }
    ]
}
```

**Frontend Pattern:**
```javascript
// Filter comments for a specific resource (client-side)
const filterCommentsByResource = (allComments, resourceId) => {
    return allComments.filter(comment => comment.resource === resourceId);
};

// Display comments with nesting (parent/child)
const displayComments = (comments) => {
    return comments.map(comment => ({
        id: comment.id,
        author: comment.user,           // User ID - need to fetch user details separately
        content: comment.content,
        timestamp: comment.created_at,
        replies: comments.filter(c => c.parent === comment.id),
        isReply: comment.parent !== null
    }));
};
```

---

### 3. GET /api/interactions/bookmark/

**Endpoint:** `GET /api/interactions/bookmark/`

**Authentication:** Required (Bearer token)

**Access Level:** Authenticated users (see only their own bookmarks)

**Response Structure (when user has bookmarks):**
```json
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

**Frontend Usage:**
```javascript
// Check if user bookmarked a resource
const isBookmarked = userBookmarks.some(bookmark => bookmark.resource === resourceId);

// Display bookmarked resources
const bookmarkList = userBookmarks.map(bookmark => ({
    id: bookmark.id,
    resourceId: bookmark.resource,
    addedDate: bookmark.created_at
}));
```

---

## 🛡️ MODERATION ENDPOINTS

### 1. GET /api/moderation/action/

**Endpoint:** `GET /api/moderation/action/`

**Authentication:** Required (Bearer token)

**Access Level:** Admin/Moderators Only ⚠️

**Note:** Only staff members can view and manage moderation actions.

**Response Structure:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 21,
            "resource": {
                "id": 14,
                "title": "Software Engineering and Design Pattern",
                "file": "https://res.cloudinary.com/dwowbxgjs/image/upload/v1/resources/mpoojka7ftjucxd3re4z",
                "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry...",
                "resource_type": "assignment"
            },
            "action": "approved",
            "feedback": "Wow.. Wonderful works",
            "created_at": "2026-03-31T15:05:18.811640Z"
        },
        {
            "id": 22,
            "resource": {
                "id": 14,
                "title": "Software Engineering and Design Pattern",
                "file": "https://res.cloudinary.com/dwowbxgjs/image/upload/v1/resources/mpoojka7ftjucxd3re4z",
                "description": "Lorem Ipsum is simply dummy text...",
                "resource_type": "assignment"
            },
            "action": "approved",
            "feedback": "Wow.. Wonderful works",
            "created_at": "2026-03-31T15:13:00.535757Z"
        }
    ]
}
```

**Query Parameters:**
- `resource__status` (string): pending, approved, rejected - Filter by resource status
- `action` (string): pending, approved, rejected - Filter by action status

**Admin Dashboard Pattern:**
```javascript
// Show pending resources for moderation
const pendingReview = actions.filter(action => action.action === 'pending');

// Show action history
const actionHistory = actions.map(action => ({
    id: action.id,
    resourceId: action.resource.id,
    resourceTitle: action.resource.title,
    action: action.action,
    feedback: action.feedback,
    timestamp: action.created_at
}));
```

---

### 2. GET /api/moderation/report/

**Endpoint:** `GET /api/moderation/report/`

**Authentication:** Required (Bearer token)

**Access Level:** 
- **Reporting:** Authenticated users can report resources
- **Viewing:** Admin/Moderators only ⚠️

**Note:** Regular users can report inappropriate content. Only staff can view and manage reports.

**Response Structure:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "resource_details": {
                "id": 14,
                "title": "Software Engineering and Design Pattern",
                "file": "https://res.cloudinary.com/dwowbxgjs/image/upload/v1/resources/mpoojka7ftjucxd3re4z",
                "description": "Lorem Ipsum is simply dummy text...",
                "resource_type": "assignment"
            },
            "reported_by": "mehedi49891@gmail.com",
            "reason": "very bad",
            "status": "open",
            "created_at": "2026-03-31T15:53:20.931684Z"
        }
    ]
}
```

**Query Parameters (Admin Only):**
- `status` (string): open, resolved, closed
- `ordering` (string): -created_at

**Admin Dashboard Pattern:**
```javascript
// Show open reports
const openReports = reports.filter(report => report.status === 'open');

// Report details for review
const reportAnalysis = openReports.map(report => ({
    id: report.id,
    resourceId: report.resource_details.id,
    resourceTitle: report.resource_details.title,
    reportedBy: report.reported_by,
    reason: report.reason,
    status: report.status,
    timestamp: report.created_at,
    action: 'Take Action'  // Button to approve/reject resource
}));
```

---

## 🔔 NOTIFICATIONS ENDPOINT

### GET /api/notifications/

**Endpoint:** `GET /api/notifications/`

**Authentication:** Required (Bearer token)

**Access Level:** Authenticated users (see only their own notifications)

**Response Structure:**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 27,
            "user": 28,
            "title": "New resource report",
            "message": "'Software Engineering and Design Pattern' has been reported by Mahdi139. Reason: very bad...",
            "is_read": false,
            "created_at": "2026-03-31T15:53:21.994390Z",
            "link_type": "resource",
            "link_id": 14
        },
        {
            "id": 20,
            "user": 28,
            "title": "Resource Approved",
            "message": "Your resource 'Machine Learning' has been approved. Nice",
            "is_read": false,
            "created_at": "2026-03-26T11:04:21.031017Z",
            "link_type": "resource",
            "link_id": 12
        },
        {
            "id": 3,
            "user": 28,
            "title": "Resource rejected",
            "message": "Your resource 'Test' has been rejected. fake",
            "is_read": false,
            "created_at": "2026-03-25T07:51:48.254988Z",
            "link_type": null,
            "link_id": null
        },
        {
            "id": 2,
            "user": 28,
            "title": "Resource rejected",
            "message": "Your resource 'Test' has been rejected. fake",
            "is_read": false,
            "created_at": "2026-03-25T07:51:30.654765Z",
            "link_type": null,
            "link_id": null
        },
        {
            "id": 1,
            "user": 28,
            "title": "Resource approved",
            "message": "Your resource 'Machine Learning' has been approved. Nice",
            "is_read": false,
            "created_at": "2026-03-25T07:38:09.062361Z",
            "link_type": null,
            "link_id": null
        }
    ]
}
```

**Notification Types:**
1. **Resource Approved** - When moderator approves uploaded resource
2. **Resource Rejected** - When moderator rejects uploaded resource
3. **New resource report** - When admin's resource gets reported (admin notification)
4. **Like** - When someone likes your resource
5. **Comment Reply** - When someone replies to your comment

**Query Parameters:**
- `is_read` (bool): Filter by read/unread
- `ordering` (string): -created_at (default)

**Frontend Pattern:**
```javascript
// Get unread count for badge
const unreadCount = notifications.filter(n => !n.is_read).length;

// Display notification list
const notificationList = notifications.map(notif => ({
    id: notif.id,
    title: notif.title,
    message: notif.message,
    isRead: notif.is_read,
    linkType: notif.link_type,  // 'resource', 'comment', null
    linkId: notif.link_id,       // ID to navigate to
    timestamp: notif.created_at,
    icon: getNotificationIcon(notif.title)  // Resource, Comment, Report, etc.
}));

// Navigate to related content
const handleNotificationClick = (notification) => {
    if (notification.link_type === 'resource') {
        navigateTo(`/resources/${notification.link_id}`);
    } else if (notification.link_type === 'comment') {
        navigateTo(`/comments/${notification.link_id}`);
    }
};
```

---

## 🎨 FRONTEND DATA STRUCTURE RECOMMENDATIONS

### Resource Card Component
```javascript
interface ResourceCard {
    id: number;
    title: string;
    description: string;
    resourceType: 'notes' | 'assignment' | 'lab_report' | 'question_bank' | 'textbook';
    status: 'pending' | 'approved' | 'rejected';
    uploadedBy: {
        id: number;
        firstName: string;
        lastName: string;
    };
    department: {
        id: number;
        name: string;
        code: string;
    };
    course: {
        id: number;
        title: string;
        courseCode: string;
    };
    semester: {
        id: number;
        name: string;
        year: number;
        isActive: boolean;
    };
    tags: Array<{ id: number; name: string }>;
    file: string;  // URL
    stats: {
        viewCount: number;
        downloadCount: number;
        likesCount: number;
        commentsCount: number;
        bookmarksCount: number;
    };
    timestamps: {
        createdAt: string;  // ISO date
        updatedAt: string;   // ISO date
    };
}
```

### Comment Thread Structure
```javascript
interface Comment {
    id: number;
    resource: number;
    user: number;
    content: string;
    created_at: string;
    parent: number | null;  // null = top-level, number = reply to comment ID
}

// Organize into tree for display
interface CommentThread {
    root: Comment;
    replies: CommentThread[];
}
```

### Notification Structure
```javascript
interface Notification {
    id: number;
    title: string;
    message: string;
    isRead: boolean;
    linkType: 'resource' | 'comment' | null;
    linkId: number | null;
    createdAt: string;
    actionUrl?: string;  // Computed from linkType and linkId
}
```

---

## 🔐 PERMISSION MATRIX

| Endpoint | Public | Authenticated | Admin/Moderator | Notes |
|----------|--------|---------------|-----------------|-------|
| **Resources** | ✅ | ✅ | ✅ | Anyone can view, authenticated can upload |
| **Departments** | ✅ | ✅ | ✅ | Public list |
| **Courses** | ✅ | ✅ | ✅ | Public list |
| **Semesters** | ❌ | ❌ | ✅ | Admin only |
| **Likes** | ❌ | ✅ | ✅ | Authenticated users |
| **Comments** | ❌ | ✅ | ✅ | Authenticated users |
| **Bookmarks** | ❌ | ✅ | ✅ | Authenticated users (own only) |
| **Moderation Actions** | ❌ | ❌ | ✅ | Admin/Staff only |
| **Reports** | ❌ | ✅ (create) | ✅ (view all) | Users report, admins review |
| **Notifications** | ❌ | ✅ | ✅ | Authenticated users (own only) |

---

## 📱 DYNAMIC RENDERING TIPS FOR AI AGENT

### 1. **Resource Card Dynamic Rendering**
```javascript
// Determine card layout based on resource_type
const getCardStyle = (resourceType) => {
    const styles = {
        'notes': { icon: '📝', color: 'blue' },
        'assignment': { icon: '📋', color: 'orange' },
        'lab_report': { icon: '🔬', color: 'green' },
        'question_bank': { icon: '❓', color: 'purple' },
        'textbook': { icon: '📚', color: 'red' }
    };
    return styles[resourceType] || { icon: '📄', color: 'gray' };
};

// Status badge styling
const getStatusBadge = (status) => {
    return {
        'pending': { text: 'Pending Review', color: 'warning' },
        'approved': { text: 'Approved', color: 'success' },
        'rejected': { text: 'Rejected', color: 'danger' }
    }[status];
};
```

### 2. **Dynamic Lists with Pagination**
```javascript
// Use the `next` URL directly for pagination
const loadNextPage = async (nextUrl) => {
    if (!nextUrl) return;  // No more pages
    const response = await fetch(nextUrl);
    return response.json();
};

// Or calculate from count and current page
const calculatePages = (totalCount, pageSize = 10) => {
    return Math.ceil(totalCount / pageSize);
};
```

### 3. **Comment Threading**
```javascript
// Build comment tree from flat list
const buildCommentTree = (comments, parentId = null) => {
    return comments
        .filter(c => c.parent === parentId)
        .map(c => ({
            ...c,
            replies: buildCommentTree(comments, c.id)
        }));
};

// Render nested comments recursively
const CommentThread = ({ comment, depth = 0 }) => (
    <div style={{ marginLeft: `${depth * 20}px` }}>
        <Comment data={comment} />
        {comment.replies?.map(reply => (
            <CommentThread key={reply.id} comment={reply} depth={depth + 1} />
        ))}
    </div>
);
```

### 4. **Dynamic Filter Dropdowns**
```javascript
// Chain API calls: Departments → Courses → Resources
const handleDepartmentChange = async (deptId) => {
    const coursesRes = await fetch(`/api/academic/courses/?department=${deptId}`);
    const courses = await coursesRes.json();
    setAvailableCourses(courses.results);
    setSelectedCourse(null);  // Reset course selection
};

const handleCourseChange = async (courseId) => {
    const resourcesRes = await fetch(`/api/resources/resources/?course=${courseId}`);
    const resources = await resourcesRes.json();
    setFilteredResources(resources.results);
};
```

---

## ✅ DEVELOPER CHECKLIST FOR FRONTEND

- [ ] **Resource Display**
  - [ ] Render resource cards with type icon and status badge
  - [ ] Show statistics (views, likes, comments, bookmarks)
  - [ ] Handle pending/approved/rejected status visually
  - [ ] Display uploader name and department

- [ ] **Academic Data**
  - [ ] Create department dropdown list
  - [ ] Create course dropdown (filtered by department)
  - [ ] Show semester if available
  - [ ] Display course code with title

- [ ] **Interactions**
  - [ ] Implement like/unlike toggle
  - [ ] Build comment system with threading
  - [ ] Add bookmark functionality
  - [ ] Show counts dynamically

- [ ] **Admin Features**
  - [ ] Moderation dashboard for pending resources
  - [ ] Report management interface
  - [ ] Semester management (CRUD)
  - [ ] View all reports with severity

- [ ] **Notifications**
  - [ ] Display notification badge with unread count
  - [ ] Show notification list sorted by date
  - [ ] Make notifications clickable (navigate to resource/comment)
  - [ ] Mark as read on click
  - [ ] Handle null link_id gracefully

- [ ] **Client-Side Filtering**
  - [ ] Filter comments by resource on client (API doesn't support server-side filtering)
  - [ ] Handle pagination with `next` URL
  - [ ] Implement infinite scroll if desired

---

## 🚀 SAMPLE INTEGRATION CODE

```javascript
import axios from 'axios';

const API_BASE_URL = 'https://notenest-backend-hd5r.onrender.com/api';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: { 'Content-Type': 'application/json' }
});

// Interceptor for auth token
apiClient.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

export const apiServices = {
    // Resources
    getResources: (params) => apiClient.get('/resources/resources/', { params }),
    getResourceById: (id) => apiClient.get(`/resources/resources/${id}/`),
    
    // Academic
    getDepartments: () => apiClient.get('/academic/departments/'),
    getCourses: (params) => apiClient.get('/academic/courses/', { params }),
    getSemesters: () => apiClient.get('/academic/semesters/'),  // Admin only
    
    // Interactions
    getLikes: () => apiClient.get('/interactions/like/'),
    getComments: () => apiClient.get('/interactions/comment/'),
    getBookmarks: () => apiClient.get('/interactions/bookmark/'),
    
    // Moderation (Admin only)
    getModerationActions: (params) => apiClient.get('/moderation/action/', { params }),
    getReports: (params) => apiClient.get('/moderation/report/', { params }),
    
    // Notifications
    getNotifications: (params) => apiClient.get('/notifications/', { params }),
};
```

---

**Ready for frontend development with real data structures! 🎉**
