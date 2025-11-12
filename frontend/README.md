# Woodshop Frontend

React frontend for the Woodshop workout tracking application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Run development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173/`

## Project Structure

- `src/components/` - Reusable React components
  - `auth/` - Authentication components
  - `workouts/` - Workout logging components
  - `programs/` - Program browsing and tracking
  - `analytics/` - Charts and progress tracking
  - `common/` - Shared UI components
- `src/pages/` - Top-level page components
- `src/services/` - API client and service layer
- `src/hooks/` - Custom React hooks
- `src/context/` - React context providers
- `src/utils/` - Utility functions

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
