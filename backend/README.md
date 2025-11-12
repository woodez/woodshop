# Woodshop Backend

Django REST Framework API for the Woodshop workout tracking application.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Project Structure

- `users/` - User authentication and profile management
- `workouts/` - Workout logging, exercises, sets
- `programs/` - Workout programs and subscriptions
- `analytics/` - Progress tracking and statistics
- `woodshop_api/` - Main project configuration

## API Documentation

Once the server is running, API documentation will be available at:
- Browsable API: `http://localhost:8000/api/`
- Admin panel: `http://localhost:8000/admin/`
