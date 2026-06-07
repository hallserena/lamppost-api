from fastapi import APIRouter, HTTPException
from database import supabase
from models.schemas import SignUp, SignIn

router = APIRouter()

@router.post("/signup/")
def sign_up(data: SignUp):
    response = supabase.auth.sign_up({"email": data.email, "password": data.password})
    if response.user is None:
        raise HTTPException(status_code=400, detail="Sign-up failed")
    return {"message": "Account created — check your email to confirm"}

@router.post("/signin/")
def sign_in(data: SignIn):
    response = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    if response.user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "access_token": response.session.access_token,
        "token_type":   "bearer",
        "user_id":      response.user.id,
    }
