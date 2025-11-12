# Woodshop - Workout Tracking App Development Plan

## Project Overview

A full-stack workout tracking application that allows users to:
- Log workouts with exercises, sets, reps, and weights
- Subscribe to and follow structured workout programs
- Track progress over time with visual graphs
- Monitor strength increases and performance metrics

**Tech Stack:**
- Backend: Django REST Framework (DRF)
- Frontend: React
- Database: PostgreSQL (recommended for production)
- Additional: JWT authentication, Chart.js/Recharts for graphs

---

## Phase 1: Project Setup & Core Infrastructure

### 1.1 Backend Setup
- [ ] Initialize Django project with Django REST Framework
- [ ] Configure PostgreSQL database
- [ ] Set up virtual environment and dependencies
- [ ] Configure Django settings (CORS, REST framework, static files)
- [ ] Set up Git workflow and .env for secrets
- [ ] Create base project structure with apps:
  - `users` - User management and authentication
  - `workouts` - Core workout tracking functionality
  - `programs` - Workout program/template system
  - `analytics` - Progress tracking and statistics

### 1.2 Frontend Setup
- [ ] Initialize React app (Vite or Create React App)
- [ ] Set up project structure (components, pages, services, hooks)
- [ ] Configure API client (Axios/Fetch)
- [ ] Set up routing (React Router)
- [ ] Configure state management (Context API or Redux Toolkit)
- [ ] Set up base styling system (Tailwind CSS or Material-UI)

### 1.3 Development Environment
- [ ] Docker setup for consistent dev environment (optional but recommended)
- [ ] Configure hot reload for both frontend and backend
- [ ] Set up API documentation (Swagger/OpenAPI)
- [ ] Create README with setup instructions

**Deliverable:** Working development environment with frontend and backend communicating

---

## Phase 2: User Authentication & Authorization

### 2.1 Backend Authentication
- [ ] Create User model (extend Django AbstractUser if needed)
- [ ] Implement JWT token authentication (djangorestframework-simplejwt)
- [ ] Create authentication endpoints:
  - POST `/api/auth/register/` - User registration
  - POST `/api/auth/login/` - Login and token generation
  - POST `/api/auth/refresh/` - Token refresh
  - POST `/api/auth/logout/` - Logout
  - GET `/api/auth/me/` - Get current user profile
- [ ] Add user profile fields (name, email, preferences)
- [ ] Implement permission classes for protected routes

### 2.2 Frontend Authentication
- [ ] Create authentication context/state management
- [ ] Build registration page/form with validation
- [ ] Build login page/form
- [ ] Implement token storage (localStorage/sessionStorage)
- [ ] Create protected route wrapper component
- [ ] Add automatic token refresh logic
- [ ] Build user profile page
- [ ] Implement logout functionality

**Deliverable:** Complete user authentication system with protected routes

---

## Phase 3: Core Workout Tracking System

### 3.1 Database Models (Backend)

**Exercise Model:**
```python
- id
- name (e.g., "Bench Press", "Squat")
- description
- category (strength, cardio, flexibility)
- muscle_groups (ManyToMany)
- equipment_needed
- instructions
- video_url (optional)
- created_by (User FK - for custom exercises)
- is_public (bool)
```

**Workout Model:**
```python
- id
- user (FK)
- program (FK, nullable - if following a program)
- date
- name/title
- notes
- duration (optional)
- completed (bool)
- created_at
- updated_at
```

**WorkoutExercise Model (Junction table with extra data):**
```python
- id
- workout (FK)
- exercise (FK)
- order (position in workout)
- notes
```

**Set Model:**
```python
- id
- workout_exercise (FK)
- set_number
- reps (integer)
- weight (decimal)
- rpe (rate of perceived exertion, optional)
- completed (bool)
- notes
```

### 3.2 Backend API Endpoints

**Exercises:**
- GET `/api/exercises/` - List all exercises (paginated, filterable)
- GET `/api/exercises/{id}/` - Get exercise details
- POST `/api/exercises/` - Create custom exercise
- PUT `/api/exercises/{id}/` - Update custom exercise
- DELETE `/api/exercises/{id}/` - Delete custom exercise

**Workouts:**
- GET `/api/workouts/` - List user's workouts (filterable by date range)
- GET `/api/workouts/{id}/` - Get workout details with all exercises and sets
- POST `/api/workouts/` - Create new workout
- PUT `/api/workouts/{id}/` - Update workout
- DELETE `/api/workouts/{id}/` - Delete workout
- POST `/api/workouts/{id}/complete/` - Mark workout as complete

**Sets:**
- POST `/api/workouts/{workout_id}/exercises/{exercise_id}/sets/` - Add set
- PUT `/api/sets/{id}/` - Update set
- DELETE `/api/sets/{id}/` - Delete set

### 3.3 Frontend - Workout Logging UI

- [ ] Create workout list/calendar view
- [ ] Build "Start Workout" flow:
  - Select/search exercises
  - Add exercises to workout
  - Log sets (reps/weight input)
  - Real-time set tracking
- [ ] Build workout detail view (past workouts)
- [ ] Create exercise library/browser
- [ ] Add quick-log functionality
- [ ] Implement workout templates (save workout as template for reuse)
- [ ] Build workout history page

**Deliverable:** Fully functional workout logging system

---

## Phase 4: Workout Programs & Subscriptions

### 4.1 Database Models (Backend)

**Program Model:**
```python
- id
- name (e.g., "5x5 Strength", "Push/Pull/Legs")
- description
- created_by (User FK)
- is_public (bool)
- difficulty_level
- duration_weeks
- tags (ManyToMany)
- created_at
```

**ProgramWeek Model:**
```python
- id
- program (FK)
- week_number
- description
```

**ProgramDay Model:**
```python
- id
- program_week (FK)
- day_number
- name (e.g., "Push Day", "Leg Day")
- description
```

**ProgramExercise Model:**
```python
- id
- program_day (FK)
- exercise (FK)
- order
- sets (suggested)
- reps (suggested, can be range like "8-12")
- rest_period
- notes
```

**UserProgram Model (Subscription/Enrollment):**
```python
- id
- user (FK)
- program (FK)
- start_date
- current_week
- current_day
- is_active (bool)
- completed (bool)
- created_at
```

### 4.2 Backend API Endpoints

**Programs:**
- GET `/api/programs/` - List available programs
- GET `/api/programs/{id}/` - Get program details with full structure
- POST `/api/programs/` - Create custom program
- PUT `/api/programs/{id}/` - Update program
- DELETE `/api/programs/{id}/` - Delete program
- GET `/api/programs/{id}/preview/` - Preview program structure

**User Programs (Subscriptions):**
- GET `/api/user-programs/` - List user's enrolled programs
- GET `/api/user-programs/active/` - Get current active program
- POST `/api/user-programs/` - Subscribe to a program
- PUT `/api/user-programs/{id}/` - Update progress (week/day)
- POST `/api/user-programs/{id}/complete/` - Mark program complete
- DELETE `/api/user-programs/{id}/` - Unsubscribe

**Program Workflow:**
- GET `/api/user-programs/{id}/today/` - Get today's workout from program
- POST `/api/user-programs/{id}/advance/` - Move to next day/week

### 4.3 Frontend - Program Features

- [ ] Create program browser/marketplace
- [ ] Build program detail/preview page
- [ ] Implement program subscription flow
- [ ] Create "Today's Workout" view (from active program)
- [ ] Build program progress tracker
- [ ] Show current week/day in program
- [ ] Add ability to create custom programs
- [ ] Implement program builder UI (drag-and-drop interface)

**Deliverable:** Complete program system with subscription and tracking

---

## Phase 5: Progress Tracking & Analytics

### 5.1 Backend Analytics

**Models:**
```python
PersonalRecord Model:
- id
- user (FK)
- exercise (FK)
- record_type (max_weight, max_reps, max_volume)
- value
- date_achieved
- workout (FK, optional)

ProgressSnapshot Model:
- id
- user (FK)
- date
- body_weight (optional)
- body_fat_percentage (optional)
- measurements (JSONField - chest, arms, etc.)
```

**API Endpoints:**
- GET `/api/analytics/progress/{exercise_id}/` - Get progress data for exercise
  - Returns time-series data of weight/reps over time
- GET `/api/analytics/personal-records/` - List all PRs
- GET `/api/analytics/volume/` - Total volume over time
- GET `/api/analytics/workout-frequency/` - Workouts per week/month
- POST `/api/analytics/body-metrics/` - Log body measurements

### 5.2 Frontend - Charts & Visualization

- [ ] Install charting library (Chart.js or Recharts)
- [ ] Create progress dashboard page
- [ ] Build exercise progress chart (weight over time)
- [ ] Create volume tracking chart (total volume by week)
- [ ] Build workout frequency chart
- [ ] Add personal records display
- [ ] Implement comparison views (current vs. previous cycle)
- [ ] Create body metrics tracker
- [ ] Add date range filters for all charts

### 5.3 Calculations & Insights

- [ ] Calculate 1RM (one-rep max) estimates
- [ ] Track progressive overload (increase from previous session)
- [ ] Show suggested weight increases
- [ ] Calculate total volume per workout/week
- [ ] Identify strength plateaus
- [ ] Generate workout summaries and insights

**Deliverable:** Comprehensive analytics dashboard with visual progress tracking

---

## Phase 6: Enhanced Features & UX

### 6.1 Mobile Responsiveness
- [ ] Ensure all pages work on mobile devices
- [ ] Optimize workout logging for mobile (large touch targets)
- [ ] Add mobile-specific navigation (bottom nav bar)
- [ ] Test on various screen sizes

### 6.2 Quality of Life Features
- [ ] Add workout timer/rest timer
- [ ] Implement exercise substitutions
- [ ] Create workout notes and comments
- [ ] Add exercise favorites/bookmarks
- [ ] Build search functionality across all features
- [ ] Implement notifications (workout reminders)
- [ ] Add dark mode toggle
- [ ] Create onboarding flow for new users

### 6.3 Social Features (Optional)
- [ ] Share workout programs with other users
- [ ] Community program library
- [ ] Add friends and compare progress
- [ ] Workout sharing on social media

### 6.4 Data Management
- [ ] Export workout data (CSV/PDF)
- [ ] Import workouts from other apps
- [ ] Backup and restore functionality
- [ ] Data visualization exports

**Deliverable:** Polished, user-friendly application

---

## Phase 7: Testing, Optimization & Deployment

### 7.1 Testing
- [ ] Write backend unit tests (Django TestCase)
- [ ] Test API endpoints (DRF APITestCase)
- [ ] Write frontend component tests (Jest + React Testing Library)
- [ ] End-to-end testing (Playwright or Cypress)
- [ ] Test authentication flows
- [ ] Test data integrity and edge cases
- [ ] Performance testing (load testing APIs)

### 7.2 Optimization
- [ ] Backend: Database query optimization (select_related, prefetch_related)
- [ ] Add database indexes on frequently queried fields
- [ ] Implement API pagination for large datasets
- [ ] Frontend: Code splitting and lazy loading
- [ ] Optimize bundle size
- [ ] Add caching (Redis for API responses)
- [ ] Image optimization (if using exercise images)

### 7.3 Security
- [ ] Security audit (SQL injection, XSS, CSRF)
- [ ] Rate limiting on API endpoints
- [ ] Secure password requirements
- [ ] HTTPS enforcement
- [ ] Environment variable security
- [ ] API key protection

### 7.4 Deployment
- [ ] Set up production database (PostgreSQL)
- [ ] Configure production Django settings
- [ ] Set up static file serving (WhiteNoise or CDN)
- [ ] Deploy backend (Heroku, Railway, DigitalOcean, AWS)
- [ ] Deploy frontend (Vercel, Netlify, or same server)
- [ ] Configure domain and SSL
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Configure monitoring and error tracking (Sentry)
- [ ] Set up database backups

**Deliverable:** Production-ready application deployed and accessible

---

## Phase 8: Post-Launch Iteration

### 8.1 User Feedback
- [ ] Collect user feedback
- [ ] Analyze usage patterns
- [ ] Prioritize feature requests
- [ ] Fix bugs and issues

### 8.2 Advanced Features (Future)
- [ ] AI-powered workout suggestions
- [ ] Form check videos with AI feedback
- [ ] Integration with fitness trackers (Fitbit, Apple Health)
- [ ] Meal planning and nutrition tracking
- [ ] Progressive web app (PWA) for offline access
- [ ] Native mobile apps (React Native)

---

## Technical Architecture Summary

### Backend Structure
```
woodshop-backend/
├── manage.py
├── requirements.txt
├── woodshop/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── workouts/
│   ├── models.py (Exercise, Workout, WorkoutExercise, Set)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── programs/
│   ├── models.py (Program, ProgramWeek, ProgramDay, UserProgram)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── analytics/
    ├── models.py (PersonalRecord, ProgressSnapshot)
    ├── serializers.py
    ├── views.py
    └── urls.py
```

### Frontend Structure
```
woodshop-frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   ├── workouts/
│   │   ├── programs/
│   │   ├── analytics/
│   │   └── common/
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── WorkoutLog.jsx
│   │   ├── Programs.jsx
│   │   ├── Analytics.jsx
│   │   └── Profile.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── storage.js
│   ├── hooks/
│   ├── context/
│   ├── utils/
│   ├── App.jsx
│   └── main.jsx
└── package.json
```

---

## Key Design Decisions

1. **Separation of Concerns**: Backend handles all business logic and data validation; frontend is purely presentational
2. **RESTful API**: Standard REST principles for predictable endpoints
3. **JWT Authentication**: Stateless authentication for scalability
4. **Normalized Database**: Avoid data duplication with proper foreign keys
5. **Component-Based UI**: Reusable React components for consistency
6. **Progressive Enhancement**: Start with core features, add advanced features iteratively

---

## Estimated Timeline

- **Phase 1**: 1 week
- **Phase 2**: 1 week
- **Phase 3**: 2-3 weeks
- **Phase 4**: 2 weeks
- **Phase 5**: 2 weeks
- **Phase 6**: 2 weeks
- **Phase 7**: 2 weeks
- **Total**: ~12-14 weeks for MVP with full features

---

## Next Steps

1. Review and approve this plan
2. Set up development environment (Phase 1.1 and 1.2)
3. Begin with user authentication (Phase 2)
4. Iteratively build each phase, testing thoroughly before moving forward
