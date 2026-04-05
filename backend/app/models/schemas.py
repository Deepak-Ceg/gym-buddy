from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class MetricType(str, Enum):
    steps = "steps"
    active_energy = "active_energy"
    workout_minutes = "workout_minutes"
    sleep_hours = "sleep_hours"
    exercise_minutes = "exercise_minutes"


class LeaderboardPeriod(str, Enum):
    weekly = "weekly"


class User(BaseModel):
    id: str
    name: str
    email: str
    timezone: str
    dietary_preferences: list[str]
    goal: str
    program_start_date: date


class BuddyPair(BaseModel):
    id: str
    member_ids: list[str]
    invite_status: Literal["accepted", "pending"]
    competition_style: Literal["supportive"]


class HealthMetric(BaseModel):
    id: str
    user_id: str
    source: Literal["apple_health", "manual"]
    date: date
    metric_type: MetricType
    value: float
    unit: str
    synced_at: datetime


class DietChecklist(BaseModel):
    sugar_free: bool
    low_fried_food: bool
    hydration_goal_met: bool
    protein_focus_met: bool
    fiber_focus_met: bool


class DailyCheckIn(BaseModel):
    id: str
    user_id: str
    date: date
    workout_completed: bool
    recovery_completed: bool
    mood: str
    soreness: str
    notes: str
    voice_transcript: str | None = None
    diet: DietChecklist


class ScoreBreakdown(BaseModel):
    steps_activity: int
    workout_completion: int
    diet_adherence: int
    recovery_checkin: int
    streak_bonus: int
    penalties: int = 0


class DailyScore(BaseModel):
    id: str
    user_id: str
    buddy_pair_id: str
    date: date
    breakdown: ScoreBreakdown
    total: int
    missed_day: bool
    penalty_applied: bool
    computed_at: datetime


class LeaderboardEntry(BaseModel):
    user_id: str
    user_name: str
    total_points: int
    current_streak: int
    penalties: int
    rank: int
    score_delta: int = 0


class LeaderboardSnapshot(BaseModel):
    id: str
    buddy_pair_id: str
    period: LeaderboardPeriod
    week_of: date
    entries: list[LeaderboardEntry]
    generated_at: datetime


class StreakState(BaseModel):
    user_id: str
    current_streak: int
    consecutive_misses: int
    recovery_mode_days_left: int


class Milestone(BaseModel):
    id: str
    user_id: str
    title: str
    target_date: date
    status: Literal["upcoming", "earned"]
    bonus_points: int


class WorkoutExercise(BaseModel):
    name: str
    sets: str
    reps: str


class WorkoutDay(BaseModel):
    day: str
    theme: str
    duration_minutes: int
    exercises: list[WorkoutExercise]


class WorkoutPlan(BaseModel):
    id: str
    title: str
    focus: str
    days: list[WorkoutDay]


class MealGuidance(BaseModel):
    id: str
    title: str
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"]
    items: list[str]
    tags: list[str]
    avoid: list[str]


class CoachInsight(BaseModel):
    id: str
    user_id: str
    summary: str
    next_actions: list[str]
    sources: list[str]


class KnowledgeDocument(BaseModel):
    id: str
    title: str
    category: Literal["workout", "diet", "program_rules"]
    content: str


class HealthSyncPayload(BaseModel):
    user_id: str
    metrics: list[HealthMetric]


class VoiceCheckInRequest(BaseModel):
    user_id: str
    transcript: str = Field(min_length=5)


class VoiceCheckInResponse(BaseModel):
    summary: str
    extracted_signals: dict[str, str]


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=7)


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    timezone: str
    dietary_preferences: list[str]
    goal: str
    program_start_date: date


class DailyCheckInSubmission(BaseModel):
    user_id: str
    date: date
    workout_completed: bool
    recovery_completed: bool
    mood: str = Field(min_length=2, max_length=50)
    soreness: str = Field(min_length=2, max_length=50)
    notes: str = ""
    voice_transcript: str | None = None
    diet: DietChecklist


class DailyCheckInUpsertResponse(BaseModel):
    checkin: DailyCheckIn
    score: DailyScore
    streak: StreakState
