from __future__ import annotations

from datetime import date, datetime, timezone

from app.models.schemas import (
    BuddyPair,
    DailyCheckIn,
    DailyScore,
    HealthMetric,
    LeaderboardEntry,
    LeaderboardPeriod,
    LeaderboardSnapshot,
    ScoreBreakdown,
    StreakState,
    User,
)


STEPS_TARGET = 8000
PENALTY_POINTS = -30


def _steps_points(metrics: list[HealthMetric], user_id: str, day: date) -> int:
    steps = sum(
        metric.value
        for metric in metrics
        if metric.user_id == user_id and metric.date == day and metric.metric_type.value == "steps"
    )
    if steps >= STEPS_TARGET:
        return 25
    if steps >= 5000:
        return 15
    if steps > 0:
        return 5
    return 0


def _diet_points(checkin: DailyCheckIn) -> int:
    flags = [
        checkin.diet.sugar_free,
        checkin.diet.low_fried_food,
        checkin.diet.hydration_goal_met,
        checkin.diet.protein_focus_met,
        checkin.diet.fiber_focus_met,
    ]
    return int(20 * (sum(flags) / len(flags)))


def score_day(
    *,
    user_id: str,
    buddy_pair_id: str,
    day: date,
    checkin: DailyCheckIn | None,
    metrics: list[HealthMetric],
    streak_state: StreakState,
) -> tuple[DailyScore, StreakState]:
    steps_points = _steps_points(metrics, user_id, day)
    workout_points = 30 if checkin and checkin.workout_completed else 0
    diet_points = _diet_points(checkin) if checkin else 0
    recovery_points = 10 if checkin and checkin.recovery_completed else 0

    missed_day = checkin is None or not checkin.workout_completed
    consecutive_misses = streak_state.consecutive_misses + 1 if missed_day else 0
    current_streak = streak_state.current_streak + 1 if not missed_day else 0

    penalty_applied = consecutive_misses >= 3
    penalty_points = PENALTY_POINTS if penalty_applied else 0
    recovery_days = 3 if penalty_applied else max(streak_state.recovery_mode_days_left - 1, 0)

    if penalty_applied:
        consecutive_misses = 0
        current_streak = 0

    streak_bonus = 15 if not missed_day else 0
    breakdown = ScoreBreakdown(
        steps_activity=steps_points,
        workout_completion=workout_points,
        diet_adherence=diet_points,
        recovery_checkin=recovery_points,
        streak_bonus=streak_bonus,
        penalties=penalty_points,
    )
    total = (
        breakdown.steps_activity
        + breakdown.workout_completion
        + breakdown.diet_adherence
        + breakdown.recovery_checkin
        + breakdown.streak_bonus
        + breakdown.penalties
    )
    new_streak = StreakState(
        user_id=user_id,
        current_streak=current_streak,
        consecutive_misses=consecutive_misses,
        recovery_mode_days_left=recovery_days,
    )
    score = DailyScore(
        id=f"score-{user_id}-{day.isoformat()}",
        user_id=user_id,
        buddy_pair_id=buddy_pair_id,
        date=day,
        breakdown=breakdown,
        total=total,
        missed_day=missed_day,
        penalty_applied=penalty_applied,
        computed_at=datetime.now(timezone.utc),
    )
    return score, new_streak


def build_leaderboard(
    *,
    pair: BuddyPair,
    users: list[User],
    scores: list[DailyScore],
    streaks: list[StreakState],
    week_of: date,
) -> LeaderboardSnapshot:
    entries: list[LeaderboardEntry] = []
    lookup = {user.id: user for user in users}
    streak_lookup = {streak.user_id: streak for streak in streaks}

    for member_id in pair.member_ids:
        user = lookup[member_id]
        member_scores = [score for score in scores if score.user_id == member_id]
        total_points = sum(score.total for score in member_scores)
        penalties = sum(score.breakdown.penalties for score in member_scores)
        streak = streak_lookup[member_id]
        entries.append(
            LeaderboardEntry(
                user_id=member_id,
                user_name=user.name,
                total_points=total_points,
                current_streak=streak.current_streak,
                penalties=penalties,
                rank=0,
            )
        )

    entries.sort(key=lambda entry: entry.total_points, reverse=True)
    if len(entries) >= 2:
        delta = entries[0].total_points - entries[1].total_points
        entries[0].score_delta = delta
        entries[1].score_delta = -delta
    for index, entry in enumerate(entries, start=1):
        entry.rank = index

    return LeaderboardSnapshot(
        id=f"leaderboard-{pair.id}-{week_of.isoformat()}",
        buddy_pair_id=pair.id,
        period=LeaderboardPeriod.weekly,
        week_of=week_of,
        entries=entries,
        generated_at=datetime.now(timezone.utc),
    )
