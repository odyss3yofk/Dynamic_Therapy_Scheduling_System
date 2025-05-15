# Therapy Management System API

A Django REST Framework-based API for managing therapy sessions, therapists, children, and their progress.

## Features

- User authentication with JWT tokens
- Role-based access control (Admin, Therapist, Parent)
- CRUD operations for all entities
- Automated session scheduling using PuLP
- Progress tracking for therapy sessions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List all users (Admin only)
- `POST /api/users/` - Create new user (Admin only)
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Children
- `GET /api/children/` - List children (filtered by parent for parents)
- `POST /api/children/` - Create new child
- `GET /api/children/{id}/` - Get child details
- `PUT /api/children/{id}/` - Update child
- `DELETE /api/children/{id}/` - Delete child

### Therapists
- `GET /api/therapists/` - List all therapists
- `POST /api/therapists/` - Create new therapist (Admin only)
- `GET /api/therapists/{id}/` - Get therapist details
- `PUT /api/therapists/{id}/` - Update therapist
- `DELETE /api/therapists/{id}/` - Delete therapist

### Sessions
- `GET /api/sessions/` - List sessions (filtered by role)
- `POST /api/sessions/` - Create new session
- `GET /api/sessions/{id}/` - Get session details
- `PUT /api/sessions/{id}/` - Update session
- `DELETE /api/sessions/{id}/` - Delete session
- `POST /api/sessions/schedule_sessions/` - Run ILP scheduler

### Progress
- `GET /api/progress/` - List progress records (filtered by role)
- `POST /api/progress/` - Create new progress record
- `GET /api/progress/{id}/` - Get progress details
- `PUT /api/progress/{id}/` - Update progress
- `DELETE /api/progress/{id}/` - Delete progress

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. Obtain a token:
```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'
```

2. Use the token in subsequent requests:
```bash
curl http://localhost:8000/api/children/ \
     -H "Authorization: Bearer <your_token>"
```

## Session Scheduling

The system uses PuLP (Python Linear Programming) to automatically assign therapists to sessions based on:
- Therapist availability
- Session time slots
- No overlapping sessions
- Optimal assignment

To trigger the scheduler:
```bash
curl -X POST http://localhost:8000/api/sessions/schedule_sessions/ \
     -H "Authorization: Bearer <your_token>"
```

## Security Considerations

1. Change the `SECRET_KEY` in settings.py before deployment
2. Set `DEBUG = False` in production
3. Configure proper CORS settings for production
4. Use HTTPS in production
5. Implement rate limiting
6. Regular security audits 