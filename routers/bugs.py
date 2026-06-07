from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from database import supabase
from auth_utils import get_current_user
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

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
        msg = MIMEMultipart()
        msg['From']    = os.getenv("GMAIL_USER")
        msg['To']      = os.getenv("GMAIL_USER")
        msg['Subject'] = f"[{report.severity.upper()}] New Lamppost bug report"

        body = f"""
New Bug Report

Severity: {report.severity}
Page: {report.page or 'Not specified'}
User email: {report.user_email or 'Not provided'}

Description:
{report.description}
        """
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
            smtp.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Email failed: {e}")

    return {"message": "Bug report submitted"}