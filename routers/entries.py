from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from database import supabase
from auth_utils import get_current_user
from models.schemas import EntryCreate, EntryUpdate, EntryResponse

router = APIRouter()

@router.get("/", response_model=list[EntryResponse])
def list_entries(
    search: Optional[str] = Query(None),
    tag:    Optional[str] = Query(None),
    limit:  int           = Query(20, le=100),
    offset: int           = Query(0),
    user_id: str = Depends(get_current_user),
):
    query = (
        supabase.table("entries")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
    )
    if search:
        query = query.text_search("fts", search)
    if tag:
        query = query.contains("tags", [tag])
    result = query.execute()
    return result.data

@router.post("/", response_model=EntryResponse, status_code=201)
def create_entry(entry: EntryCreate, user_id: str = Depends(get_current_user)):
    result = (
        supabase.table("entries")
        .insert({
            "user_id": user_id,
            "title":   entry.title,
            "body":    entry.body,
            "tags":    entry.tags,
        })
        .execute()
    )
    return result.data[0]

@router.get("/{entry_id}/", response_model=EntryResponse)
def get_entry(entry_id: str, user_id: str = Depends(get_current_user)):
    result = (
        supabase.table("entries")
        .select("*")
        .eq("id", entry_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Entry not found")
    return result.data

@router.patch("/{entry_id}/", response_model=EntryResponse)
def update_entry(entry_id: str, updates: EntryUpdate, user_id: str = Depends(get_current_user)):
    payload = {k: v for k, v in updates.model_dump().items() if v is not None}
    if not payload:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = (
        supabase.table("entries")
        .update(payload)
        .eq("id", entry_id)
        .eq("user_id", user_id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Entry not found")
    return result.data[0]

@router.delete("/{entry_id}/", status_code=204)
def delete_entry(entry_id: str, user_id: str = Depends(get_current_user)):
    supabase.table("entries").delete().eq("id", entry_id).eq("user_id", user_id).execute()
