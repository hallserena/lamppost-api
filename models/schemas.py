from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class MoodOption(str, Enum):
    great     = "great"
    good      = "good"
    neutral   = "neutral"
    low       = "low"
    terrible  = "terrible"


class EntryCreate(BaseModel):
    title:   Optional[str] = None
    body:    str
    tags:    list[str] = []

class EntryUpdate(BaseModel):
    title:   Optional[str] = None
    body:    Optional[str] = None
    tags:    Optional[list[str]] = None

class EntryResponse(BaseModel):
    id:         str
    user_id:    str
    title:      Optional[str]
    body:       str
    tags:       list[str]
    created_at: datetime
    updated_at: datetime


class MoodCreate(BaseModel):
    mood:  MoodOption
    note:  Optional[str] = None

class MoodResponse(BaseModel):
    id:         str
    user_id:    str
    mood:       MoodOption
    note:       Optional[str]
    logged_at:  datetime


class SkillCreate(BaseModel):
    skill:       str
    description: Optional[str] = None
    tags:        list[str] = []

class SkillUpdate(BaseModel):
    skill:       Optional[str] = None
    description: Optional[str] = None
    tags:        Optional[list[str]] = None

class SkillResponse(BaseModel):
    id:          str
    user_id:     str
    skill:       str
    description: Optional[str]
    tags:        list[str]
    created_at:  datetime


class SignUp(BaseModel):
    email:    str
    password: str

class SignIn(BaseModel):
    email:    str
    password: str
