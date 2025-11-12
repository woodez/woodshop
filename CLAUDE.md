# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Woodshop is a full-stack workout tracking application that allows users to log workouts (exercises, sets, reps, weights), subscribe to workout programs, and track progress with visual graphs.

**Tech Stack:**
- Backend: Django REST Framework (Python)
- Frontend: React + Vite
- Database: SQLite (dev), PostgreSQL (production recommended)
- Auth: JWT tokens (djangorestframework-simplejwt)

**Project Structure:**
```
woodshop/
├── backend/          # Django REST API
│   ├── users/        # User authentication and profiles
│   ├── workouts/     # Workout logging (exercises, sets, reps)
│   ├── programs/     # Workout programs and subscriptions
│   └── analytics/    # Progress tracking and statistics
└── frontend/         # React SPA
    └── src/
        ├── components/  # React components
        ├── pages/       # Top-level pages
        ├── services/    # API client
        └── context/     # State management
```

## Development Commands

### Backend Setup (Django)

**IMPORTANT: Always activate the virtual environment before running Python commands or installing pip modules.**

```bash
cd backend

# First time setup
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

pip install -r requirements.txt
cp .env.example .env  # Edit .env as needed
python manage.py migrate
python manage.py createsuperuser  # Optional: create admin user

# Run development server
python manage.py runserver
# API available at http://localhost:8000/api/
```

**Common Backend Commands:**
```bash
# Always activate venv first
cd backend
source .venv/bin/activate

# Database migrations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations  # View migration status

# Create new app
python manage.py startapp <app_name>

# Django shell
python manage.py shell

# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

### Frontend Setup (React)

```bash
cd frontend

# First time setup
npm install
cp .env.example .env  # Edit .env as needed

# Run development server
npm run dev
# App available at http://localhost:5173/
```

**Common Frontend Commands:**
```bash
cd frontend

npm run dev        # Start dev server
npm run build      # Build for production
npm run preview    # Preview production build
npm run lint       # Run ESLint

# Add new dependencies
npm install <package-name>
```

### Running Both Servers

You need to run both backend and frontend servers simultaneously during development:

**Terminal 1 (Backend):**
```bash
cd backend
source .venv/bin/activate
python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## Architecture Overview

### Backend Apps

1. **users/** - User authentication and profile management
   - Custom user model
   - JWT authentication endpoints (login, register, refresh)
   - User profile data

2. **workouts/** - Core workout tracking
   - Exercise library (public and user-created)
   - Workout sessions
   - Sets (reps/weight tracking)
   - WorkoutExercise junction model

3. **programs/** - Workout programs
   - Program templates (week → day → exercise structure)
   - User program subscriptions
   - Progress tracking through programs

4. **analytics/** - Progress and statistics
   - Personal records
   - Progress snapshots
   - Time-series data for charts
   - Volume and frequency calculations

### API Patterns

- **Authentication:** JWT tokens via `Authorization: Bearer <token>` header
- **Pagination:** Default 20 items per page
- **Filtering:** Use query params (e.g., `?date_gte=2024-01-01`)
- **Nested resources:** `/api/workouts/{id}/exercises/{exercise_id}/sets/`

### Frontend Architecture

- **Routing:** React Router for navigation
- **State:** Context API for auth, can add Redux if needed
- **API calls:** Axios with interceptors for auth
- **Charts:** Recharts library for progress visualization

## Key Development Workflows

### Creating a New Model

1. Define model in appropriate app's `models.py`
2. Create serializer in `serializers.py`
3. Create viewset in `views.py`
4. Register URL in `urls.py`
5. Run `python manage.py makemigrations`
6. Run `python manage.py migrate`

### Adding a New API Endpoint

1. Backend: Create view in appropriate app
2. Backend: Add URL pattern to app's `urls.py`
3. Frontend: Add service method in `src/services/`
4. Frontend: Use in components via hooks or directly

### Database Migrations

Always create migrations after model changes:
```bash
cd backend
source .venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

## Environment Variables

### Backend (.env in backend/)
- `SECRET_KEY` - Django secret key
- `DEBUG` - True/False
- `ALLOWED_HOSTS` - Comma-separated hosts
- `CORS_ALLOWED_ORIGINS` - Frontend URLs
- Database credentials (for PostgreSQL)

### Frontend (.env in frontend/)
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000/api)

## Testing

Backend tests use Django's TestCase:
```bash
cd backend
source .venv/bin/activate
python manage.py test
python manage.py test workouts  # Test specific app
```

## Common Issues

1. **CORS errors:** Ensure frontend URL is in `CORS_ALLOWED_ORIGINS` in backend settings
2. **401 Unauthorized:** Check JWT token is being sent correctly
3. **Migration conflicts:** Run `python manage.py migrate --fake-initial` if needed
4. **Port conflicts:** Backend uses 8000, frontend uses 5173

## Next Development Steps

See [plan.md](plan.md) for the complete development roadmap organized by phases.
