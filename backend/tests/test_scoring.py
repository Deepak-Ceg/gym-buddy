from datetime import date

from app.models.schemas import DailyCheckIn, DietChecklist, HealthMetric, MetricType, StreakState
from app.services.scoring import score_day


def _checkin(workout_completed: bool) -> DailyCheckIn:
    return DailyCheckIn(
        id="checkin-test",
        user_id="user-1",
        date=date(2026, 4, 5),
        workout_completed=workout_completed,
        recovery_completed=True,
        mood="good",
        soreness="low",
        notes="Test",
        diet=DietChecklist(
            sugar_free=True,
            low_fried_food=True,
            hydration_goal_met=True,
            protein_focus_met=True,
            fiber_focus_met=True,
        ),
    )


def test_score_day_rewards_full_completion() -> None:
    metrics = [
        HealthMetric(
            id="m1",
            user_id="user-1",
            source="apple_health",
            date=date(2026, 4, 5),
            metric_type=MetricType.steps,
            value=9000,
            unit="count",
            synced_at="2026-04-05T12:00:00Z",
        )
    ]
    streak = StreakState(user_id="user-1", current_streak=4, consecutive_misses=0, recovery_mode_days_left=0)
    score, updated = score_day(
        user_id="user-1",
        buddy_pair_id="pair-1",
        day=date(2026, 4, 5),
        checkin=_checkin(workout_completed=True),
        metrics=metrics,
        streak_state=streak,
    )
    assert score.total == 100
    assert updated.current_streak == 5
    assert not score.penalty_applied


def test_score_day_penalizes_third_miss() -> None:
    streak = StreakState(user_id="user-1", current_streak=2, consecutive_misses=2, recovery_mode_days_left=0)
    score, updated = score_day(
        user_id="user-1",
        buddy_pair_id="pair-1",
        day=date(2026, 4, 5),
        checkin=_checkin(workout_completed=False),
        metrics=[],
        streak_state=streak,
    )
    assert score.penalty_applied
    assert score.breakdown.penalties == -30
    assert updated.recovery_mode_days_left == 3
    assert updated.current_streak == 0
