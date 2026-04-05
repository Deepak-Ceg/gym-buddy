from __future__ import annotations

from datetime import date, datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, Response, status

from app.db.database import database
from app.models.schemas import (
    BuddyPair,
    CoachInsight,
    DailyCheckIn,
    DailyCheckInSubmission,
    DailyCheckInUpsertResponse,
    DailyScore,
    HealthMetric,
    HealthSyncPayload,
    KnowledgeDocument,
    LoginRequest,
    MealGuidance,
    Milestone,
    StreakState,
    User,
    UserProfile,
    VoiceCheckInRequest,
    VoiceCheckInResponse,
    WorkoutPlan,
)
from app.core.config import settings
from app.services.auth import new_session_token, session_expiry, verify_password
from app.services.coach import build_coach_insight, parse_voice_checkin
from app.services.scoring import build_leaderboard, score_day
from app.services.seed_data import MEAL_GUIDANCE, TODAY, WORKOUT_PLAN


router = APIRouter(prefix="/api")


def to_user_profile(user: User) -> UserProfile:
    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        timezone=user.timezone,
        dietary_preferences=user.dietary_preferences,
        goal=user.goal,
        program_start_date=user.program_start_date,
    )


async def current_user_from_request(request: Request) -> User:
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    session = await database.collection("sessions").find_one({"id": token})
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session not found")
    expires_at = session.get("expires_at")
    if expires_at:
        expiry = datetime.fromisoformat(expires_at)
        if expiry <= datetime.now(timezone.utc):
            await database.collection("sessions").delete_many({"id": token})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    user_doc = await database.collection("users").find_one({"id": session["user_id"]})
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return User.model_validate(user_doc)


async def build_dashboard_payload(day: date, current_user: User) -> dict:
    users = [User.model_validate(item) for item in await database.collection("users").find_all()]
    pair_doc = next(
        (
            item
            for item in await database.collection("buddy_pairs").find_all()
            if current_user.id in item["member_ids"]
        ),
        None,
    )
    if not pair_doc:
        raise HTTPException(status_code=404, detail="Buddy pair not found")
    buddy_pair = BuddyPair.model_validate(pair_doc)
    metrics = [HealthMetric.model_validate(item) for item in await database.collection("health_metrics").find_all()]
    checkins = [DailyCheckIn.model_validate(item) for item in await database.collection("checkins").find_all()]
    streaks = [StreakState.model_validate(item) for item in await database.collection("streaks").find_all()]
    milestones = [Milestone.model_validate(item) for item in await database.collection("milestones").find_all()]
    knowledge = [
        KnowledgeDocument.model_validate(item) for item in await database.collection("knowledge_documents").find_all()
    ]

    scores: list[DailyScore] = []
    updated_streaks: list[StreakState] = []
    for streak in streaks:
        if streak.user_id not in buddy_pair.member_ids:
            continue
        checkin = next((item for item in checkins if item.user_id == streak.user_id and item.date == day), None)
        score, updated = score_day(
            user_id=streak.user_id,
            buddy_pair_id=buddy_pair.id,
            day=day,
            checkin=checkin,
            metrics=metrics,
            streak_state=streak,
        )
        scores.append(score)
        updated_streaks.append(updated)

    leaderboard = build_leaderboard(pair=buddy_pair, users=users, scores=scores, streaks=updated_streaks, week_of=day)
    insights: list[CoachInsight] = []
    for checkin in checkins:
        if checkin.user_id not in buddy_pair.member_ids:
            continue
        insights.append(build_coach_insight(checkin.user_id, checkin, knowledge))

    buddy_user_id = next(member_id for member_id in buddy_pair.member_ids if member_id != current_user.id)
    buddy_user = next(user for user in users if user.id == buddy_user_id)
    my_score = next((score for score in scores if score.user_id == current_user.id), None)
    buddy_score = next((score for score in scores if score.user_id == buddy_user.id), None)
    my_checkin = next((checkin for checkin in checkins if checkin.user_id == current_user.id and checkin.date == day), None)
    my_milestones = [milestone for milestone in milestones if milestone.user_id == current_user.id]
    buddy_milestones = [milestone for milestone in milestones if milestone.user_id == buddy_user.id]
    my_insight = next((insight for insight in insights if insight.user_id == current_user.id), None)
    buddy_insight = next((insight for insight in insights if insight.user_id == buddy_user.id), None)

    return {
        "generated_for": day.isoformat(),
        "current_user": to_user_profile(current_user).model_dump(mode="json"),
        "buddy_user": to_user_profile(buddy_user).model_dump(mode="json"),
        "buddy_pair": buddy_pair.model_dump(),
        "my_score": my_score.model_dump(mode="json") if my_score else None,
        "buddy_score": buddy_score.model_dump(mode="json") if buddy_score else None,
        "leaderboard": leaderboard.model_dump(mode="json"),
        "my_checkin": my_checkin.model_dump(mode="json") if my_checkin else None,
        "my_milestones": [milestone.model_dump(mode="json") for milestone in my_milestones],
        "buddy_milestones": [milestone.model_dump(mode="json") for milestone in buddy_milestones],
        "workout_plan": WORKOUT_PLAN,
        "meal_guidance": MEAL_GUIDANCE,
        "my_coach_insight": my_insight.model_dump() if my_insight else None,
        "buddy_coach_insight": buddy_insight.model_dump() if buddy_insight else None,
    }


@router.get("/dashboard")
async def dashboard(request: Request) -> dict:
    current_user = await current_user_from_request(request)
    return await build_dashboard_payload(TODAY, current_user)


@router.post("/auth/login")
async def login(payload: LoginRequest, response: Response) -> dict:
    user_doc = await database.collection("users").find_one({"email": payload.email})
    if not user_doc or not verify_password(payload.password, user_doc.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = new_session_token()
    expires_at = session_expiry()
    await database.collection("sessions").replace_one(
        {"id": token},
        {"id": token, "user_id": user_doc["id"], "expires_at": expires_at.isoformat()},
    )
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=settings.session_ttl_days * 24 * 60 * 60,
    )
    user = User.model_validate(user_doc)
    return {"user": to_user_profile(user).model_dump(mode="json")}


@router.post("/auth/logout")
async def logout(request: Request, response: Response) -> dict[str, str]:
    token = request.cookies.get(settings.session_cookie_name)
    if token:
        await database.collection("sessions").delete_many({"id": token})
    response.delete_cookie(settings.session_cookie_name)
    return {"status": "logged_out"}


@router.get("/auth/me")
async def auth_me(request: Request) -> dict:
    current_user = await current_user_from_request(request)
    return {"user": to_user_profile(current_user).model_dump(mode="json")}


@router.get("/workout-plan", response_model=WorkoutPlan)
async def workout_plan() -> WorkoutPlan:
    return WorkoutPlan.model_validate(WORKOUT_PLAN)


@router.get("/meal-guidance", response_model=list[MealGuidance])
async def meal_guidance() -> list[MealGuidance]:
    return [MealGuidance.model_validate(item) for item in MEAL_GUIDANCE]


@router.get("/knowledge", response_model=list[KnowledgeDocument])
async def knowledge_documents() -> list[KnowledgeDocument]:
    docs = await database.collection("knowledge_documents").find_all()
    return [KnowledgeDocument.model_validate(item) for item in docs]


@router.post("/voice-checkin", response_model=VoiceCheckInResponse)
async def voice_checkin(payload: VoiceCheckInRequest) -> VoiceCheckInResponse:
    return parse_voice_checkin(payload.transcript)


@router.post("/checkins", response_model=DailyCheckInUpsertResponse)
async def upsert_checkin(payload: DailyCheckInSubmission, request: Request) -> DailyCheckInUpsertResponse:
    current_user = await current_user_from_request(request)
    pair_doc = next(
        (
            item
            for item in await database.collection("buddy_pairs").find_all()
            if current_user.id in item["member_ids"]
        ),
        None,
    )
    if not pair_doc:
        raise HTTPException(status_code=404, detail="Buddy pair not found")
    pair = BuddyPair.model_validate(pair_doc)

    checkin = DailyCheckIn(
        id=f"checkin-{current_user.id}-{payload.date.isoformat()}",
        user_id=current_user.id,
        date=payload.date,
        workout_completed=payload.workout_completed,
        recovery_completed=payload.recovery_completed,
        mood=payload.mood,
        soreness=payload.soreness,
        notes=payload.notes,
        voice_transcript=payload.voice_transcript,
        diet=payload.diet,
    )
    await database.collection("checkins").replace_one(
        {"user_id": current_user.id, "date": payload.date.isoformat()},
        checkin.model_dump(mode="json"),
    )

    metrics = [HealthMetric.model_validate(item) for item in await database.collection("health_metrics").find_all()]
    streaks = [StreakState.model_validate(item) for item in await database.collection("streaks").find_all()]
    streak = next((item for item in streaks if item.user_id == current_user.id), None)
    if not streak:
        streak = StreakState(user_id=current_user.id, current_streak=0, consecutive_misses=0, recovery_mode_days_left=0)

    score, updated_streak = score_day(
        user_id=current_user.id,
        buddy_pair_id=pair.id,
        day=payload.date,
        checkin=checkin,
        metrics=metrics,
        streak_state=streak,
    )

    await database.collection("streaks").replace_one({"user_id": current_user.id}, updated_streak.model_dump(mode="json"))
    await database.collection("daily_scores").replace_one(
        {"user_id": current_user.id, "date": payload.date.isoformat()},
        score.model_dump(mode="json"),
    )

    refreshed = await build_dashboard_payload(payload.date, current_user)
    snapshot = refreshed["leaderboard"]
    await database.collection("leaderboard_snapshots").replace_one(
        {"buddy_pair_id": pair.id, "week_of": payload.date.isoformat()},
        snapshot,
    )

    return DailyCheckInUpsertResponse(checkin=checkin, score=score, streak=updated_streak)


@router.post("/health-sync")
async def health_sync(payload: HealthSyncPayload) -> dict[str, str | int]:
    collection = database.collection("health_metrics")
    await collection.insert_many([metric.model_dump(mode="json") for metric in payload.metrics])
    return {"status": "accepted", "metrics_received": len(payload.metrics)}


@router.get("/users/{user_id}/coach-insight", response_model=CoachInsight)
async def coach_insight(user_id: str) -> CoachInsight:
    checkins = [DailyCheckIn.model_validate(item) for item in await database.collection("checkins").find_all()]
    knowledge = [
        KnowledgeDocument.model_validate(item) for item in await database.collection("knowledge_documents").find_all()
    ]
    checkin = next((item for item in checkins if item.user_id == user_id), None)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    return build_coach_insight(user_id, checkin, knowledge)


@router.get("/users/{user_id}/milestones", response_model=list[Milestone])
async def user_milestones(user_id: str) -> list[Milestone]:
    milestones = [Milestone.model_validate(item) for item in await database.collection("milestones").find_all()]
    return [milestone for milestone in milestones if milestone.user_id == user_id]


@router.get("/leaderboard/{buddy_pair_id}")
async def leaderboard(buddy_pair_id: str, on_date: date | None = None) -> dict:
    day = on_date or TODAY
    users = [User.model_validate(item) for item in await database.collection("users").find_all()]
    pair_data = await database.collection("buddy_pairs").find_one({"id": buddy_pair_id})
    if not pair_data:
        raise HTTPException(status_code=404, detail="Buddy pair not found")
    pair = BuddyPair.model_validate(pair_data)
    metrics = [HealthMetric.model_validate(item) for item in await database.collection("health_metrics").find_all()]
    checkins = [DailyCheckIn.model_validate(item) for item in await database.collection("checkins").find_all()]
    streaks = [StreakState.model_validate(item) for item in await database.collection("streaks").find_all()]

    scores: list[DailyScore] = []
    updated_streaks: list[StreakState] = []
    for streak in streaks:
        checkin = next((item for item in checkins if item.user_id == streak.user_id and item.date == day), None)
        score, updated = score_day(
            user_id=streak.user_id,
            buddy_pair_id=pair.id,
            day=day,
            checkin=checkin,
            metrics=metrics,
            streak_state=streak,
        )
        scores.append(score)
        updated_streaks.append(updated)

    snapshot = build_leaderboard(pair=pair, users=users, scores=scores, streaks=updated_streaks, week_of=day)
    return snapshot.model_dump(mode="json")
