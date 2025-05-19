# Therapy Management System API
- User authentication with JWT tokens
- Role-based access control (Admin, Therapist, Parent)
- CRUD operations for all entities
- Automated session scheduling using PuLP
- Progress tracking for therapy sessions



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


## Session Scheduling

The system uses PuLP (Python Linear Programming) to automatically assign therapists to sessions based on:
- Therapist availability
- Session time slots
- No overlapping sessions
- Optimal assignment

## Adding therapist and child registration endpoints.
- Allow parents to register children only if authenticated.
- Adding email validation and password confirmation.

