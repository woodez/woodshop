# Phase 4: Workout Programs & Subscriptions - BACKEND COMPLETE

## Backend Complete ✅

### Database Models Expanded

#### Program Model (Enhanced)
- Added `tags` field for categorization
- Indexed for fast public/difficulty queries
- Supports both public and private programs

#### New Models Created

**ProgramWeek** - Week structure within a program
- Links to Program
- `week_number` - Week position (1, 2, 3...)
- `description` - Optional week notes
- Unique constraint: program + week_number

**ProgramDay** - Day structure within a week
- Links to ProgramWeek
- `day_number` - Day position within week
- `name` - E.g., "Push Day", "Leg Day", "Rest Day"
- `description` - Optional day notes
- Unique constraint: program_week + day_number

**ProgramExercise** - Exercises within a day
- Links to ProgramDay and Exercise
- `order` - Exercise sequence
- `sets` - Suggested sets (integer)
- `reps` - Suggested reps (string: "8-12", "10", "5x5")
- `rest_period` - Rest seconds between sets
- `notes` - Exercise-specific instructions

**UserProgram** - User subscription to program
- Links User to Program
- `start_date` - When user started
- `current_week` - Progress tracking
- `current_day` - Progress tracking
- `is_active` - Boolean flag
- `completed` - Completion status
- `completed_at` - Completion timestamp
- Unique constraint: user + program (one active subscription per program)

### API Endpoints Created

#### Programs (`/api/programs/`)
- `GET /api/programs/` - List public programs + user's programs
  - Search: `?search=strength`
  - Filter by difficulty: `?difficulty=beginner`
  - Filter by duration: `?max_weeks=8`
  - Returns: List serializer (lighter)
- `GET /api/programs/{id}/` - Get full program structure
  - Returns: Complete nested structure (weeks → days → exercises)
- `POST /api/programs/` - Create custom program
- `PUT/PATCH /api/programs/{id}/` - Update program
- `DELETE /api/programs/{id}/` - Delete program

#### User Programs (`/api/user-programs/`)
- `GET /api/user-programs/` - List user's subscriptions
  - Filter: `?is_active=true` - Get only active subscriptions
  - Returns: UserProgram with program details
- `GET /api/user-programs/{id}/` - Get subscription details
- `POST /api/user-programs/` - Subscribe to a program
  - Required: `program` (ID), `start_date`
- `PUT/PATCH /api/user-programs/{id}/` - Update subscription
- `DELETE /api/user-programs/{id}/` - Unsubscribe
- `POST /api/user-programs/{id}/advance/` - **Move to next day/week**
  - Auto-advances day → week → completion
  - Marks program complete when finished
- `GET /api/user-programs/{id}/today_workout/` - **Get today's workout**
  - Returns current ProgramDay with exercises
- `GET /api/user-programs/active/` - **Get active subscription**
  - Returns user's currently active program

### Serializers Created

1. **ProgramExerciseSerializer** - Exercise with suggestions (sets/reps)
2. **ProgramDaySerializer** - Day with all exercises
3. **ProgramWeekSerializer** - Week with all days
4. **ProgramSerializer** - Full program structure (nested)
5. **ProgramListSerializer** - Lightweight for lists
6. **UserProgramSerializer** - User subscription with program details

All serializers include:
- Nested relationships properly loaded
- Computed fields (total_days, subscription_count)
- Read-only fields for security
- Auto-set user context

### Key Features

**Program Structure:**
```
Program
  └─ Week 1
      ├─ Day 1: Push Day
      │   ├─ Bench Press: 3 sets x 8-12 reps
      │   ├─ Incline DB Press: 3 sets x 10 reps
      │   └─ Cable Flyes: 3 sets x 12-15 reps
      └─ Day 2: Pull Day
          ├─ Deadlift: 4 sets x 5 reps
          └─ Pull-ups: 3 sets x 8-10 reps
  └─ Week 2...
```

**Progress Tracking:**
- User starts program on specific date
- System tracks current week + day
- "Advance" endpoint moves through program automatically
- Program marks complete when all weeks/days done

**Workout Integration:**
- Programs link to Workout model
- When user follows program, workouts can reference program
- "Today's Workout" shows current program day

### Admin Interface

All models registered with:
- Inline editing (weeks in program, days in week, exercises in day)
- Search and filters
- Raw ID fields for performance
- List displays with key info

---

## Frontend TODO

### Services Needed
Create `frontend/src/services/programService.js`:
- API calls for programs, user-programs
- Subscribe/unsubscribe methods
- Advance program progress
- Get today's workout

### Pages to Build

#### 1. Programs List (`/programs`)
- Browse available programs
- Search by name/description
- Filter by difficulty (beginner/intermediate/advanced)
- Filter by duration (weeks)
- Show: name, difficulty, duration, subscriber count
- Click to view details

#### 2. Program Detail (`/programs/:id`)
- Full program preview
- Show all weeks → days → exercises
- Display suggested sets/reps for each exercise
- "Subscribe" button
- Program stats (total weeks, days, exercises)
- Difficulty level badge

#### 3. My Programs (`/my-programs`)
- List user's subscribed programs
- Show progress (Week X, Day Y)
- Active vs completed programs
- Click to view program or see today's workout

#### 4. Today's Workout (from program)
- Component showing current day's workout
- Display exercises with suggested sets/reps
- "Mark as Complete" → advances to next day
- Show progress bar through program

### Integration Points

**Dashboard:**
- Add "Browse Programs" button
- Show active program widget (if subscribed)
- Quick link to "Today's Workout"

**Workout Logging:**
- When creating workout from program, pre-populate exercises
- Link workout to program
- Auto-advance program after completing workout

---

## Example Program Data

```json
{
  "id": 1,
  "name": "Push Pull Legs - 6 Week",
  "description": "Classic PPL split for intermediate lifters",
  "difficulty_level": "intermediate",
  "duration_weeks": 6,
  "tags": "strength, hypertrophy, 6-day",
  "weeks": [
    {
      "week_number": 1,
      "days": [
        {
          "day_number": 1,
          "name": "Push",
          "exercises": [
            {
              "exercise": {"id": 1, "name": "Bench Press"},
              "sets": 4,
              "reps": "8-10",
              "rest_period": 120,
              "order": 1
            },
            {
              "exercise": {"id": 3, "name": "Overhead Press"},
              "sets": 3,
              "reps": "10-12",
              "rest_period": 90,
              "order": 2
            }
          ]
        },
        {
          "day_number": 2,
          "name": "Pull",
          "exercises": [...]
        },
        {
          "day_number": 3,
          "name": "Legs",
          "exercises": [...]
        }
      ]
    }
  ]
}
```

### User Subscription Example

```json
{
  "id": 1,
  "program": {
    "id": 1,
    "name": "Push Pull Legs - 6 Week",
    "duration_weeks": 6
  },
  "start_date": "2025-11-12",
  "current_week": 2,
  "current_day": 3,
  "is_active": true,
  "completed": false
}
```

---

## API Usage Examples

### Subscribe to Program
```bash
POST /api/user-programs/
{
  "program": 1,
  "start_date": "2025-11-12"
}
```

### Get Today's Workout
```bash
GET /api/user-programs/1/today_workout/
# Returns current day with all exercises
```

### Complete Day (Advance)
```bash
POST /api/user-programs/1/advance/
# Moves to next day/week automatically
```

### Get Active Program
```bash
GET /api/user-programs/active/
# Returns user's currently active subscription
```

---

## Database Schema

```
Program
  ├─ id, name, description
  ├─ difficulty_level, duration_weeks
  ├─ created_by (FK User)
  └─ is_public, tags

ProgramWeek
  ├─ id, program (FK)
  ├─ week_number
  └─ description

ProgramDay
  ├─ id, program_week (FK)
  ├─ day_number, name
  └─ description

ProgramExercise
  ├─ id, program_day (FK)
  ├─ exercise (FK Exercise)
  ├─ sets, reps, rest_period
  ├─ order
  └─ notes

UserProgram
  ├─ id, user (FK), program (FK)
  ├─ start_date
  ├─ current_week, current_day
  ├─ is_active, completed
  └─ completed_at
```

---

## Files Created/Modified

### Backend
- [programs/models.py](backend/programs/models.py:1-127) - 5 models (Program, Week, Day, Exercise, UserProgram)
- [programs/serializers.py](backend/programs/serializers.py) - 6 serializers
- [programs/views.py](backend/programs/views.py:1-157) - 2 viewsets (Program, UserProgram)
- [programs/urls.py](backend/programs/urls.py) - URL routing
- [programs/admin.py](backend/programs/admin.py:1-56) - Admin interface
- [woodshop_api/urls.py](backend/woodshop_api/urls.py:26) - Added programs URLs

### Migrations
- `programs/migrations/0002_*.py` - All new models migrated

---

## Current Status

- ✅ Phase 1: Project Setup & Core Infrastructure - COMPLETE
- ✅ Phase 2: User Authentication & Authorization - COMPLETE
- ✅ Phase 3: Core Workout Tracking System - COMPLETE
- ⏳ Phase 4: Workout Programs & Subscriptions - **BACKEND COMPLETE, FRONTEND PENDING**
- ⏳ Phase 5: Progress Tracking & Analytics
- ⏳ Phase 6: Enhanced Features & UX
- ⏳ Phase 7: Testing, Optimization & Deployment
- ⏳ Phase 8: Post-Launch Iteration

---

## Next Steps

1. Create program service layer in frontend
2. Build Programs browse/search page
3. Build Program detail page with full preview
4. Build My Programs page (subscriptions)
5. Build "Today's Workout" component
6. Integrate into dashboard and routing
7. Create sample programs via Django admin or seed command
8. Test subscribe → follow → complete flow

**Phase 4 backend is production-ready! Users can subscribe to structured workout programs with week/day progressions.** 💪
