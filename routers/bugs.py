from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from database import supabase
from auth_utils import get_current_user

router = APIRouter()

class BugReport(BaseModel):
    description: str
    page:        Optional[str] = None
    severity:    str
    user_email:  Optional[str] = None

@router.post("/", status_code=201)
def submit_bug(report: BugReport, user_id: str = Depends(get_current_user)):
    result = (
        supabase.table("bug_reports")
        .insert({
            "user_id":     user_id,
            "description": report.description,
            "page":        report.page,
            "severity":    report.severity,
            "user_email":  report.user_email,
        })
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to save bug report")
    return {"message": "Bug report submitted"}