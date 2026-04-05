from __future__ import annotations

from app.models.schemas import CoachInsight, DailyCheckIn, KnowledgeDocument, VoiceCheckInResponse


def build_coach_insight(user_id: str, checkin: DailyCheckIn, knowledge: list[KnowledgeDocument]) -> CoachInsight:
    sources = [doc.title for doc in knowledge[:2]]
    next_actions = [
        "Hit your full 90-minute session tomorrow.",
        "Stay sugar-free through the evening.",
        "Finish 8,000+ steps before dinner.",
    ]
    summary = (
        f"You are building momentum. Mood is {checkin.mood}, soreness is {checkin.soreness}, "
        "and the biggest win is keeping the diet consistent while protecting the streak."
    )
    return CoachInsight(
        id=f"insight-{user_id}-{checkin.date.isoformat()}",
        user_id=user_id,
        summary=summary,
        next_actions=next_actions,
        sources=sources,
    )


def parse_voice_checkin(transcript: str) -> VoiceCheckInResponse:
    lowered = transcript.lower()
    extracted = {
        "workout_status": "completed" if any(word in lowered for word in ["finished", "done", "completed"]) else "unclear",
        "cravings": "mentioned" if "craving" in lowered or "sweet" in lowered else "not_mentioned",
        "energy": "low" if any(word in lowered for word in ["tired", "low energy"]) else "good",
        "motivation": "high" if any(word in lowered for word in ["motivated", "strong", "confident"]) else "steady",
    }
    summary = (
        "Voice check-in captured your daily status and extracted workout, cravings, energy, and motivation signals."
    )
    return VoiceCheckInResponse(summary=summary, extracted_signals=extracted)
