from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from app.services.auth import hash_password

TODAY = date(2026, 4, 5)
NOW = datetime(2026, 4, 5, 12, 0, tzinfo=timezone.utc)


WORKOUT_PLAN = {
    "id": "plan-90-day-core",
    "title": "90-Day Core Cut Program",
    "focus": "Reduce belly fat through consistency, structured lifting, and ab-focused conditioning.",
    "days": [
        {
            "day": "Monday",
            "theme": "Push",
            "duration_minutes": 90,
            "exercises": [
                {"name": "Barbell Bench Press", "sets": "4", "reps": "6-8"},
                {"name": "Incline Dumbbell Press", "sets": "3", "reps": "8-10"},
                {"name": "Overhead Press", "sets": "3", "reps": "8-10"},
                {"name": "Cable Crunch", "sets": "4", "reps": "15"},
            ],
        },
        {
            "day": "Tuesday",
            "theme": "Pull",
            "duration_minutes": 90,
            "exercises": [
                {"name": "Lat Pulldown", "sets": "4", "reps": "8-10"},
                {"name": "Seated Row", "sets": "3", "reps": "10-12"},
                {"name": "Face Pull", "sets": "3", "reps": "12-15"},
                {"name": "Hanging Knee Raise", "sets": "4", "reps": "12"},
            ],
        },
        {
            "day": "Wednesday",
            "theme": "Legs",
            "duration_minutes": 90,
            "exercises": [
                {"name": "Back Squat", "sets": "4", "reps": "6-8"},
                {"name": "Romanian Deadlift", "sets": "3", "reps": "8-10"},
                {"name": "Walking Lunges", "sets": "3", "reps": "12 each side"},
                {"name": "Plank", "sets": "3", "reps": "60 sec"},
            ],
        },
        {
            "day": "Thursday",
            "theme": "Core + Conditioning",
            "duration_minutes": 90,
            "exercises": [
                {"name": "Air Bike Intervals", "sets": "10", "reps": "45s on / 45s off"},
                {"name": "Ab Wheel Rollout", "sets": "4", "reps": "10-12"},
                {"name": "Mountain Climbers", "sets": "3", "reps": "45 sec"},
                {"name": "Russian Twist", "sets": "3", "reps": "20"},
            ],
        },
        {
            "day": "Friday",
            "theme": "Upper Hypertrophy",
            "duration_minutes": 90,
            "exercises": [
                {"name": "Incline Bench", "sets": "4", "reps": "10"},
                {"name": "Chest Supported Row", "sets": "4", "reps": "10"},
                {"name": "Lateral Raise", "sets": "4", "reps": "15"},
                {"name": "Cable Woodchop", "sets": "3", "reps": "12 each side"},
            ],
        },
        {
            "day": "Saturday",
            "theme": "Lower + Abs",
            "duration_minutes": 90,
            "exercises": [
                {"name": "Leg Press", "sets": "4", "reps": "10-12"},
                {"name": "Bulgarian Split Squat", "sets": "3", "reps": "10 each side"},
                {"name": "Hanging Leg Raise", "sets": "4", "reps": "12"},
                {"name": "Farmer Carry", "sets": "4", "reps": "30 meters"},
            ],
        },
        {
            "day": "Sunday",
            "theme": "Rest / Recovery",
            "duration_minutes": 30,
            "exercises": [
                {"name": "Mobility Flow", "sets": "1", "reps": "20 min"},
                {"name": "Easy Walk", "sets": "1", "reps": "20-30 min"},
            ],
        },
    ],
}


MEAL_GUIDANCE = [
    {
        "id": "meal-1",
        "title": "High-Protein Tamil Breakfast",
        "meal_type": "breakfast",
        "items": ["Ragi dosa", "Sambar", "Greek yogurt", "Sprouted green gram salad"],
        "tags": ["tamil-veg", "high-protein", "high-fiber"],
        "avoid": ["Sugar-loaded coffee", "Bakery sweets"],
    },
    {
        "id": "meal-2",
        "title": "Balanced Lunch Plate",
        "meal_type": "lunch",
        "items": ["Red rice", "Keerai kootu", "Sundal", "Curd", "Vegetable poriyal"],
        "tags": ["tamil-veg", "satiety", "cholesterol-aware"],
        "avoid": ["Deep-fried sides", "Sweetened beverages"],
    },
    {
        "id": "meal-3",
        "title": "Light Dinner for Fat Loss",
        "meal_type": "dinner",
        "items": ["Vegetable soup", "Paneer pepper fry", "Chapati", "Cucumber salad"],
        "tags": ["low-sugar", "fat-loss", "protein-focus"],
        "avoid": ["Late-night sweets", "Heavy parotta meals"],
    },
]


KNOWLEDGE_DOCUMENTS = [
    {
        "id": "doc-1",
        "title": "Abs Are Built Through Fat Loss and Consistency",
        "category": "program_rules",
        "content": "Visible abs require sustained calorie control, regular strength training, good sleep, and patience. Ab work helps build the muscle, but body fat reduction reveals it.",
    },
    {
        "id": "doc-2",
        "title": "Tamil Vegetarian Fat-Loss Basics",
        "category": "diet",
        "content": "Focus on protein from paneer, curd, dal, channa, sprouts, tofu, and low-oil preparations. Reduce sweets, fried snacks, and sugar-heavy beverages.",
    },
    {
        "id": "doc-3",
        "title": "90-Day Accountability Rule",
        "category": "program_rules",
        "content": "Three consecutive missed days trigger a penalty, streak reset, and a three-day recovery challenge. The goal is recovery, not shame.",
    },
]


DEMO_STATE = {
    "users": [
        {
            "id": "user-1",
            "name": "Deepak",
            "email": "deepak@example.com",
            "password_hash": hash_password("deepak123"),
            "timezone": "America/Chicago",
            "dietary_preferences": ["Tamil vegetarian", "low sugar"],
            "goal": "Reduce belly fat and reveal abs in 90 days",
            "program_start_date": TODAY.isoformat(),
        },
        {
            "id": "user-2",
            "name": "Arun",
            "email": "arun@example.com",
            "password_hash": hash_password("arun123"),
            "timezone": "America/Chicago",
            "dietary_preferences": ["Tamil vegetarian", "high protein"],
            "goal": "Stay consistent, lose tummy fat, and build visible abs",
            "program_start_date": TODAY.isoformat(),
        },
    ],
    "buddy_pairs": [
        {
            "id": "pair-1",
            "member_ids": ["user-1", "user-2"],
            "invite_status": "accepted",
            "competition_style": "supportive",
        }
    ],
    "health_metrics": [
        {
            "id": "metric-1",
            "user_id": "user-1",
            "source": "apple_health",
            "date": TODAY.isoformat(),
            "metric_type": "steps",
            "value": 9800,
            "unit": "count",
            "synced_at": NOW.isoformat(),
        },
        {
            "id": "metric-2",
            "user_id": "user-2",
            "source": "apple_health",
            "date": TODAY.isoformat(),
            "metric_type": "steps",
            "value": 7600,
            "unit": "count",
            "synced_at": NOW.isoformat(),
        },
    ],
    "checkins": [
        {
            "id": "checkin-1",
            "user_id": "user-1",
            "date": TODAY.isoformat(),
            "workout_completed": True,
            "recovery_completed": True,
            "mood": "motivated",
            "soreness": "medium",
            "notes": "Strong push session and avoided sweets.",
            "voice_transcript": "I finished push day, felt strong, and stayed away from sugary snacks.",
            "diet": {
                "sugar_free": True,
                "low_fried_food": True,
                "hydration_goal_met": True,
                "protein_focus_met": True,
                "fiber_focus_met": True,
            },
        },
        {
            "id": "checkin-2",
            "user_id": "user-2",
            "date": TODAY.isoformat(),
            "workout_completed": False,
            "recovery_completed": True,
            "mood": "tired",
            "soreness": "low",
            "notes": "Missed the workout but kept meals clean.",
            "voice_transcript": "I skipped the gym today but I still ate pretty well and walked some steps.",
            "diet": {
                "sugar_free": True,
                "low_fried_food": True,
                "hydration_goal_met": False,
                "protein_focus_met": True,
                "fiber_focus_met": True,
            },
        },
    ],
    "streaks": [
        {"user_id": "user-1", "current_streak": 6, "consecutive_misses": 0, "recovery_mode_days_left": 0},
        {"user_id": "user-2", "current_streak": 1, "consecutive_misses": 2, "recovery_mode_days_left": 0},
    ],
    "milestones": [
        {
            "id": "milestone-1",
            "user_id": "user-1",
            "title": "Week 1 consistency",
            "target_date": (TODAY + timedelta(days=7)).isoformat(),
            "status": "upcoming",
            "bonus_points": 20,
        },
        {
            "id": "milestone-2",
            "user_id": "user-2",
            "title": "First monthly waist check",
            "target_date": (TODAY + timedelta(days=30)).isoformat(),
            "status": "upcoming",
            "bonus_points": 40,
        },
    ],
    "sessions": [],
    "knowledge_documents": KNOWLEDGE_DOCUMENTS,
    "leaderboard_snapshots": [],
    "daily_scores": [],
}
