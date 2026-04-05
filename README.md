# Gym Buddy

Gym Buddy is a web-first fitness accountability app for buddy pairs, with a FastAPI backend, a Next.js frontend, and an iOS HealthKit companion scaffold.

## Project Structure

- `backend/` - FastAPI app, scoring engine, seed content, and tests
- `frontend/` - Next.js app scaffold for dashboard, leaderboard, and plans
- `ios/` - SwiftUI HealthKit companion scaffold

## Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://localhost:8000` by default.

## Demo Login Credentials

- Deepak: `deepak@example.com` / `deepak123`
- Arun: `arun@example.com` / `arun123`

## Current Scope

- Buddy leaderboard and daily scoring
- 90-day six-pack program milestones
- Tamil vegetarian meal guidance
- Workout plan generation
- Voice check-in placeholder pipeline
- RAG-ready knowledge documents
- HealthKit sync API contract for the iOS companion

## Notes

- MongoDB is the primary persistence target; the backend currently includes an in-memory fallback so the app can run without database setup during early development.
- The iOS companion is a scaffold and will need to be opened in Xcode to finish signing, entitlements, and HealthKit testing.
- After backend or frontend code changes, restart both dev servers if they do not hot-reload cleanly.
