# Woodshop

A full-stack workout tracking application for logging workouts, following workout programs, and tracking strength progress over time.

## Features

- Log workouts with exercises, sets, reps, and weights
- Subscribe to and follow structured workout programs
- Track progress with visual graphs and charts
- Monitor personal records and strength increases
- Custom exercise library

## Tech Stack

- **Backend:** Django REST Framework (Python)
- **Frontend:** React + Vite
- **Database:** SQLite (dev), PostgreSQL (production)
- **Authentication:** JWT tokens

## Quick Start

See [SETUP_COMPLETE.md](SETUP_COMPLETE.md) for setup status and [CLAUDE.md](CLAUDE.md) for complete development guide.

### Backend
```bash
cd backend
source .venv/bin/activate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm run dev
```

## Documentation

- [CLAUDE.md](CLAUDE.md) - Development guide with all commands
- [plan.md](plan.md) - Complete development roadmap (8 phases)
- [SETUP_COMPLETE.md](SETUP_COMPLETE.md) - Phase 1 completion summary
- [backend/README.md](backend/README.md) - Backend setup
- [frontend/README.md](frontend/README.md) - Frontend setup

## Project Status

Phase 1 (Project Setup) is complete. Ready to begin Phase 2 (User Authentication).
