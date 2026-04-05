# NoteNest Backend API

<div align="center">

![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.14%2B-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Token%20Auth-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A Secure, Scalable Academic Resource Sharing Platform**

[Live API](https://notenest-backend-hd5r.onrender.com/) • [Documentation](#-api-reference) • [Contributing](#-contributing)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [API Reference](#-api-reference)
- [Architecture](#architecture)
- [Deployment](#deployment)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**NoteNest** is an enterprise-grade REST API backend for a university resource sharing platform. Designed with security, scalability, and user experience at its core, it enables students and faculty to securely upload, discover, and collaborate on academic materials within a centralized repository.

### Key Capabilities

| Feature | Description |
|---------|-------------|
| **Secure Authentication** | JWT-based token authentication with email verification |
| **Academic Organization** | Hierarchical structure (Departments → Courses → Semesters) |
| **Content Moderation** | Two-tier approval workflow ensuring content quality |
| **Social Features** | Commenting, liking, bookmarking, and reputation tracking |
| **Advanced Search** | Full-text search with multi-dimensional filtering |
| **Analytics** | Real-time tracking of downloads, views, and engagement |
| **Email Notifications** | Transactional emails via Brevo API integration |
| **File Management** | Secure file uploads with validation and Cloudinary integration |

### Compliance & Security

- ✅ University email domain verification
- ✅ Role-Based Access Control (RBAC)
- ✅ End-to-end encrypted authentication
- ✅ CORS protection and CSRF mitigation
- ✅ SQL injection prevention via ORM
- ✅ Rate limiting and DDoS protection

---

## Getting Started

### System Requirements

```plaintext
Python:     3.9 or higher
PostgreSQL: 12 or higher (15+ recommended)
Node/npm:   Latest stable (for frontend integration)
Disk Space: 2GB minimum
```

### Installation & Setup

#### 1. Clone Repository

```bash
git clone https://github.com/your-org/NoteNest-Backend.git
cd Note_nest_backend
```

#### 2. Virtual Environment Configuration

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Environment Configuration

Create `.env` file in project root directory:

```env
# === Django Configuration ===
SECRET_KEY=django-insecure-your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# === Database ===
DATABASE_URL=sqlite:///db.sqlite3
# Production: postgresql://username:password@localhost:5432/notenest_db

# === JWT Authentication ===
JWT_SECRET_KEY=your-jwt-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=1h
JWT_REFRESH_TOKEN_LIFETIME=7d

# === Email Service (Brevo) ===
BREVO_API_KEY=your-brevo-api-key-here
DEFAULT_FROM_EMAIL=support@notenest.com
DEFAULT_FROM_NAME=NoteNest

# === File Storage (Cloudinary) ===
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# === CORS Settings ===
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://frontend.notenest.com

# === Security ===
SECURE_SSL_REDIRECT=False  # Set to True in production
SESSION_COOKIE_SECURE=False  # Set to True in production
```

#### 5. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load initial data (optional)
python manage.py loaddata fixtures/initial_data.json
```

#### 6. Create Administrator Account

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

#### 7. Launch Development Server

```bash
python manage.py runserver
```

**API will be available at:** `http://127.0.0.1:8000/api/`  
**Admin panel:** `http://127.0.0.1:8000/admin/`

---

## 📡 API Reference

### Base URL

| Environment | URL |
|------------|-----|
| **Development** | `http://localhost:8000/api/` |
| **Production** | `https://notenest-backend-hd5r.onrender.com/api/` |

### Authentication

All authenticated endpoints require the JWT access token in the Authorization header:

```http
Authorization: Bearer <your_access_token>
```

### Response Format

All API responses follow a standardized format:

```json
{
  "status": "success|error",
  "data": {},
  "message": "Human-readable message",
  "errors": {}
}
```

---

### Account Management

#### Register New Account

```http
POST /accounts/register/
Content-Type: application/json

{
  "username": "john.doe",
  "email": "john.doe@student.metrouni.ac.bd",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

**Success Response (201 Created)**

```json
{
  "status": "success",
  "message": "Registration successful. Please verify your email.",
  "data": {
    "user_id": 1,
    "email": "john.doe@student.metrouni.ac.bd"
  }
}
```

**Validation Errors (400 Bad Request)**

```json
{
  "status": "error",
  "errors": {
    "email": ["Only university emails are allowed"],
    "password": ["Password must be at least 8 characters"]
  }
}
```

---

#### User Login

```http
POST /accounts/login/
Content-Type: application/json

{
  "username": "john.doe",
  "password": "SecurePass123!"
}
```

**Success Response (200 OK)**

```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "username": "john.doe",
      "email": "john.doe@student.metrouni.ac.bd",
      "first_name": "John",
      "last_name": "Doe",
      "role": "student"
    },
    "tokens": {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
  }
}
```

---

#### Email Verification

```http
GET /accounts/activate/{uid64}/{token}/
```

**Success Response (200 OK)**

```json
{
  "status": "success",
  "message": "Email verified successfully. Your account is now active."
}
```

---

#### User Logout

```http
POST /accounts/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

---

### Resource Management

#### Upload Academic Resource

```http
POST /resources/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

Form Data:
- title: "Data Structures: Comprehensive Guide"
- description: "In-depth coverage of arrays, linked lists, trees, and graphs"
- file: <binary_file> (PDF, DOCX, PPT, ZIP)
- department: 1
- course: 5
- semester: 2
- resource_type: "lecture_notes"
```

**Supported File Types:** PDF, DOCX, PPTX, XLSX, ZIP (Max 100MB)

**Success Response (201 Created)**

```json
{
  "status": "success",
  "message": "Resource uploaded successfully and sent for moderation",
  "data": {
    "id": 42,
    "title": "Data Structures: Comprehensive Guide",
    "file_url": "https://res.cloudinary.com/...",
    "status": "pending_moderation",
    "created_by": "john.doe",
    "created_at": "2026-03-25T14:30:00Z"
  }
}
```

---

#### Retrieve Resources

```http
GET /resources/?limit=10&offset=0
GET /resources/?department=1&course=5&status=approved&sort=-created_at
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | int | Items per page (default: 10, max: 100) |
| `offset` | int | Pagination offset |
| `department` | int | Filter by department ID |
| `course` | int | Filter by course ID |
| `semester` | int | Filter by semester ID |
| `status` | string | Filter by approval status |
| `sort` | string | Sort field (prefix with `-` for descending) |
| `search` | string | Full-text search |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "count": 156,
    "next": "https://api.example.com/resources/?limit=10&offset=10",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Advanced Algorithms",
        "description": "Complex algorithms and analysis",
        "file_url": "https://res.cloudinary.com/...",
        "resource_type": "lecture_notes",
        "status": "approved",
        "created_by": "jane.smith",
        "created_at": "2026-03-15T08:00:00Z",
        "analytics": {
          "download_count": 47,
          "view_count": 123,
          "like_count": 12
        }
      }
    ]
  }
}
```

---

#### Search Resources

```http
GET /resources/search/?q=algorithms&department=1&type=lecture_notes
```

---

#### Get Resource Details

```http
GET /resources/{id}/
```

---

#### Update Resource

```http
PATCH /resources/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description"
}
```

---

#### Delete Resource

```http
DELETE /resources/{id}/
Authorization: Bearer <access_token>
```

**Note:** Only resource creators and administrators can delete resources.

---

### Academic Structure

#### List Departments

```http
GET /academic/departments/
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Computer Science & Engineering",
      "code": "CSE",
      "description": "Faculty dedicated to computing education"
    }
  ]
}
```

---

#### List Courses

```http
GET /academic/courses/?department=1
```

---

#### List Semesters

```http
GET /academic/semesters/?course=1
```

---

### User Interactions

#### Add Like to Resource

```http
POST /interactions/like/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resource": 42
}
```

---

#### Remove Like

```http
DELETE /interactions/like/{like_id}/
Authorization: Bearer <access_token>
```

---

#### Add Comment

```http
POST /interactions/comment/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resource": 42,
  "text": "Excellent resource! Very well organized.",
  "parent_comment": null
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "user": "john.doe",
    "resource": 42,
    "text": "Excellent resource! Very well organized.",
    "parent_comment": null,
    "created_at": "2026-03-25T14:45:00Z",
    "replies": []
  }
}
```

---

#### Get Comments on Resource

```http
GET /interactions/comments/{resource_id}/
```

---

#### Bookmark Resource

```http
POST /interactions/bookmark/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resource": 42
}
```

---

#### Retrieve Bookmarks

```http
GET /interactions/bookmarks/
Authorization: Bearer <access_token>
```

---

### Content Moderation

#### List Pending Resources (Moderator Only)

```http
GET /moderation/pending/
Authorization: Bearer <moderator_token>
```

---

#### Approve Resource

```http
POST /moderation/{resource_id}/approve/
Authorization: Bearer <moderator_token>
Content-Type: application/json

{
  "notes": "Content is appropriate and well-formatted."
}
```

---

#### Reject Resource

```http
POST /moderation/{resource_id}/reject/
Authorization: Bearer <moderator_token>
Content-Type: application/json

{
  "reason": "copyright_violation",
  "notes": "This appears to be copyrighted material. Please replace with original work."
}
```

**Valid Reasons:**
- `inappropriate_content`
- `copyright_violation`
- `spam`
- `low_quality`
- `other`

---

#### Report Content

```http
POST /moderation/report/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resource": 42,
  "reason": "inappropriate_content",
  "description": "This resource contains offensive language"
}
```

---

### Notifications

#### Retrieve User Notifications

```http
GET /notifications/?unread=true
Authorization: Bearer <access_token>
```

---

#### Mark Notification as Read

```http
POST /notifications/{notification_id}/mark-as-read/
Authorization: Bearer <access_token>
```

---

## Architecture

### Microservices Structure

```
Note_nest_backend/
│
├── accounts/
│   ├── models.py              # User model with role management
│   ├── views.py               # Auth endpoints
│   ├── serializers.py         # User serializers
│   ├── email_service.py       # Brevo API integration
│   ├── urls.py                # Auth routes
│   └── migrations/
│
├── academic/
│   ├── models.py              # Department, Course, Semester
│   ├── views.py               # Academic endpoints
│   ├── serializers.py         # Academic serializers
│   ├── urls.py
│   └── migrations/
│
├── resources/
│   ├── models.py              # Resource, ResourceFile
│   ├── views.py               # Resource CRUD, search
│   ├── serializers.py         # Resource serializers
│   ├── validators.py          # File validation
│   ├── urls.py
│   └── migrations/
│
├── interactions/
│   ├── models.py              # Like, Comment, Bookmark
│   ├── views.py               # Interaction endpoints
│   ├── serializers.py         # Interaction serializers
│   ├── urls.py
│   └── migrations/
│
├── moderation/
│   ├── models.py              # ModerationAction, Report
│   ├── views.py               # Moderation endpoints
│   ├── serializers.py         # Moderation serializers
│   ├── urls.py
│   └── migrations/
│
├── notifications/
│   ├── models.py              # Notification model
│   ├── views.py               # Notification endpoints
│   ├── signals.py             # Event listeners
│   ├── serializers.py
│   ├── urls.py
│   └── migrations/
│
├── core/
│   ├── models.py              # Base model classes
│   ├── views.py               # Shared views
│   └── utils.py               # Utilities
│
├── Note_nest_backend/
│   ├── settings.py            # Configuration
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # Production server
│   ├── asgi.py                # WebSocket support
│   └── celery.py              # Task queue
│
├── manage.py
├── requirements.txt
├── .env
└── .gitignore
```

### Database Schema (Key Models)

```
User (Extended from Django User)
├── role: student | moderator | admin
├── is_verified: boolean
├── university_email: string

Department
├── name: string
├── code: string
└── description: text

Course
├── department: ForeignKey(Department)
├── name: string
├── code: string
└── credit_hours: integer

Semester
├── course: ForeignKey(Course)
├── number: integer
└── year: integer

Resource
├── creator: ForeignKey(User)
├── title: string
├── description: text
├── department: ForeignKey(Department)
├── course: ForeignKey(Course)
├── semester: ForeignKey(Semester)
├── status: pending | approved | rejected
├── downloads: integer
├── views: integer
└── created_at: datetime

Like
├── user: ForeignKey(User)
├── resource: ForeignKey(Resource)
└── created_at: datetime

Comment
├── user: ForeignKey(User)
├── resource: ForeignKey(Resource)
├── text: text
├── parent_comment: ForeignKey(Comment, null=True)
└── created_at: datetime

Notification
├── user: ForeignKey(User)
├── title: string
├── message: text
├── is_read: boolean
└── created_at: datetime
```

---

## Deployment

### Production Checklist

- [ ] **Security**
  - [ ] `DEBUG = False` in settings.py
  - [ ] Update `SECRET_KEY` with strong random value
  - [ ] Enable `SECURE_SSL_REDIRECT = True`
  - [ ] Set `SESSION_COOKIE_SECURE = True`
  - [ ] Configure CORS for production domain only

- [ ] **Database**
  - [ ] PostgreSQL instance configured and secured
  - [ ] DATABASE_URL environment variable set
  - [ ] Database backups automated
  - [ ] Migrations applied successfully

- [ ] **Integration**
  - [ ] Brevo API credentials validated
  - [ ] Cloudinary account configured
  - [ ] SMTP settings tested

- [ ] **Deployment**
  - [ ] Static files collected
  - [ ] HTTPS certificate installed
  - [ ] Health check endpoint configured
  - [ ] Error monitoring (Sentry) setup
  - [ ] Log aggregation configured

### Deploying to Render

#### Step 1: Prepare Repository

```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore

# Commit changes
git add .
git commit -m "Production-ready deployment"
git push origin main
```

#### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Configure build and start commands:

   **Build Command:**
   ```bash
   pip install -r requirements.txt && python manage.py migrate
   ```

   **Start Command:**
   ```bash
   gunicorn Note_nest_backend.wsgi
   ```

#### Step 3: Configure Environment Variables

Add to Render dashboard:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_HOSTS=notenest-backend-hd5r.onrender.com
BREVO_API_KEY=your-api-key
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
```

#### Step 4: Complete Deployment

- Render will automatically build and deploy
- Monitor deployment logs
- Test all endpoints after deployment

**Live API:** https://notenest-backend-hd5r.onrender.com/

---

## Development Guide

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test resources

# With verbose output
python manage.py test --verbosity=2

# With coverage report
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report in htmlcov/
```

### Code Quality

```bash
# Format with Black
pip install black
black .

# Lint with Flake8
pip install flake8
flake8 . --max-line-length=100

# Static analysis with Pylint
pip install pylint
pylint accounts resources
```

### Database Migrations

```bash
# Create new migration
python manage.py makemigrations accounts

# View migration status
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate accounts 0001

# Create empty migration
python manage.py makemigrations --empty accounts --name add_new_field
```

### Creating Fixtures

```bash
# Export data
python manage.py dumpdata > fixtures/backup.json

# Load data
python manage.py loaddata fixtures/backup.json
```

---

## Troubleshooting

### Common Issues & Solutions

**Issue: 404 Error on /api/**

**Solutions:**
- Verify `ALLOWED_HOSTS` includes your domain
- Check URL routing in `urls.py`
- Restart Django development server

---

**Issue: JWT Token Expired**

**Solutions:**
```bash
# Use refresh endpoint
POST /accounts/token/refresh/
{ "refresh": "your-refresh-token" }

# Check JWT_ACCESS_TOKEN_LIFETIME in settings
# Default is 1 hour
```

---

**Issue: Email Verification Not Working**

**Solutions:**
- Verify Brevo API key in `.env`
- Check email templates in `accounts/templates/`
- Enable "Less Secure App Access" for email service
- Check spam/junk folder for verification email

---

**Issue: File Upload Fails**

**Solutions:**
- Check file size (max 100MB)
- Verify Cloudinary credentials
- Ensure file type is in whitelist (PDF, DOCX, PPTX, ZIP)
- Check `MEDIA_ROOT` directory permissions

---

**Issue: Database Connection Error**

**Solutions:**
```bash
# Verify PostgreSQL is running
psql -U username -d database_name

# Check DATABASE_URL format
postgresql://user:password@localhost:5432/notenest_db

# Test connection
python manage.py dbshell
```

---

**Issue: CORS Errors from Frontend**

**Solutions:**
- Add frontend URL to `CORS_ALLOWED_ORIGINS` in settings
- For local development: `http://localhost:3000`
- Ensure `Content-Type: application/json` header is set

---

## Contributing

We welcome contributions from the community. Please follow these guidelines:

### Development Workflow

1. **Fork Repository**
   ```bash
   # On GitHub, click "Fork"
   ```

2. **Clone & Setup**
   ```bash
   git clone https://github.com/your-username/NoteNest-Backend.git
   cd Note_nest_backend
   ```

3. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature with description"
   ```

5. **Push & Create PR**
   ```bash
   git push origin feature/amazing-feature
   ```

### Code Standards

- Follow [PEP 8](https://pep8.org/) style guide
- Write meaningful commit messages
- Add tests for new features
- Update documentation
- Run `flake8` and `black` before committing

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

## Support & Contact

- **Issues:** [GitHub Issues](https://github.com/your-org/NoteNest-Backend/issues)
- **Email:** support@notenest.com
- **Documentation:** [Full API Docs](https://docs.notenest.com)
- **Discord:** [Join Community](https://discord.gg/notenest)

---

## Acknowledgments

- Django & Django REST Framework communities
- Render cloud platform
- Brevo email services
- Cloudinary file storage
- All contributors and supporters

---

<div align="center">

**Made with ❤️ for the academic community**

[⬆ Back to Top](#notenest-backend-api)

---

**Last Updated:** March 25, 2026  
**Version:** 1.0.0  
**Status:** Production Ready

</div>
