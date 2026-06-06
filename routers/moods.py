from fastapi import APIRouter, Depends, Query
from datetime import datetime, timedelta
from collections import defaultdict
from database import supabase
from auth_utils import get_current_user
from models.schemas import MoodCreate, MoodResponse

router = APIRouter()

MOOD_SCORE = {"great": 5, "good": 4, "neutral": 3, "low": 2, "terrible": 1}

@router.post("/", response_model=MoodResponse, status_code=201)
def log_mood(mood: MoodCreate, user_id: str = Depends(get_current_user)):
    result = (
        supabase.table("mood_logs")
        .insert({"user_id": user_id, "mood": mood.mood, "note": mood.note})
        .execute()
    )
    return result.data[0]

@router.get("/", response_model=list[MoodResponse])
def list_moods(
    days: int = Query(30),
    user_id: str = Depends(get_current_user),
):
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    result = (
        supabase.table("mood_logs")
        .select("*")
        .eq("user_id", user_id)
        .gte("logged_at", since)
        .order("logged_at")
        .execute()
    )
    return result.data

@router.get("/charts")
def mood_charts(
    days: int = Query(90),
    user_id: str = Depends(get_current_user),
):
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    result = (
        supabase.table("mood_logs")
        .select("mood, logged_at")
        .eq("user_id", user_id)
        .gte("logged_at", since)
        .order("logged_at")
        .execute()
    )
    rows = result.data

    timeline = [
        {"date": r["logged_at"], "mood": r["mood"], "score": MOOD_SCORE[r["mood"]]}
        for r in rows
    ]

    daily_scores = defaultdict(list)
    for r in rows:
        day = r["logged_at"][:10]
        daily_scores[day].append(MOOD_SCORE[r["mood"]])

    trend = [
        {"date": day, "avg_score": round(sum(scores) / len(scores), 2)}
        for day, scores in sorted(daily_scores.items())
    ]

    daily_counts = defaultdict(int)
    for r in rows:
        day = r["logged_at"][:10]
        daily_counts[day] += 1

    heatmap = [
        {"date": day, "count": count}
        for day, count in sorted(daily_counts.items())
    ]

    return {"timeline": timeline, "trend": trend, "heatmap": heatmap}