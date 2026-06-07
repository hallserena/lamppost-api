from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from database import supabase
from auth_utils import get_current_user
from models.schemas import SkillCreate, SkillUpdate, SkillResponse

router = APIRouter()

@router.get("/", response_model=list[SkillResponse])
def list_skills(
    tag:     Optional[str] = Query(None),
    limit:   int           = Query(50, le=200),
    offset:  int           = Query(0),
    user_id: str           = Depends(get_current_user),
):
    query = (
        supabase.table("skills_log")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
    )
    if tag:
        query = query.contains("tags", [tag])
    result = query.execute()
    return result.data

@router.post("/", response_model=SkillResponse, status_code=201)
def log_skill(skill: SkillCreate, user_id: str = Depends(get_current_user)):
    result = (
        supabase.table("skills_log")
        .insert({
            "user_id":     user_id,
            "skill":       skill.skill,
            "description": skill.description,
            "tags":        skill.tags,
        })
        .execute()
    )
    return result.data[0]

@router.patch("/{skill_id}/", response_model=SkillResponse)
def update_skill(skill_id: str, updates: SkillUpdate, user_id: str = Depends(get_current_user)):
    payload = {k: v for k, v in updates.model_dump().items() if v is not None}
    if not payload:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = (
        supabase.table("skills_log")
        .update(payload)
        .eq("id", skill_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Skill not found")
    return result.data[0]

@router.delete("/{skill_id}/", status_code=204)
def delete_skill(skill_id: str, user_id: str = Depends(get_current_user)):
    supabase.table("skills_log").delete().eq("id", skill_id).eq("user_id", user_id).execute()