from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from database import supabase
from auth_utils import get_current_user
import resend
import os

router = APIRouter()

resend.api_key = os.getenv("RESEND_API_KEY")

class BugReport(BaseModel):
    description: str
    page:        Optional[str] = None
    severity:    str
    user_email:  Optional[str] = None

@router.post("/", status_code=201)
def submit_bug(report: BugReport, user_id: str = Depends(get_current_user)):
    # Save to Supabase
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

    # Send email notification
    try:
        resend.Emails.send({
            "from":    "Lamppost Bugs <onboarding@resend.dev>",
            "to":      "projectlamppost.app@gmail.com",
            "subject": f"[{report.severity.upper()}] New bug report",
            "html":    f"""
                <h2>New Bug Report</h2>
                <p><strong>Severity:</strong> {report.severity}</p>
                <p><strong>Page:</strong> {report.page or 'Not specified'}</p>
                <p><strong>Description:</strong></p>
                <p>{report.description}</p>
                <p><strong>User email:</strong> {report.user_email or 'Not provided'}</p>
            """,
        })
    except Exception as e:
        print(f"Email failed: {e}")

    return {"message": "Bug report submitted"}

# Send email notification
    try:
        response = resend.Emails.send({
            "from":    "onboarding@resend.dev",
            "to":      "projectlamppost.app@gmail.com",
            "subject": f"[{report.severity.upper()}] New bug report",
            "html":    f"""
                <h2>New Bug Report</h2>
                <p><strong>Severity:</strong> {report.severity}</p>
                <p><strong>Page:</strong> {report.page or 'Not specified'}</p>
                <p><strong>Description:</strong></p>
                <p>{report.description}</p>
                <p><strong>User email:</strong> {report.user_email or 'Not provided'}</p>
            """,
        })
        print(f"Email response: {response}")
    except Exception as e:
        print(f"Email failed: {e}")