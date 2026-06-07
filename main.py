from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import entries, moods, skills, auth

app = FastAPI(title="Lamppost API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://lamppost-frontend.vercel.app",
        "https://lamppost-frontend-79p0k1n2b-serena-hall-s-projects.vercel.app",
        "https://lamppost-frontend-ey98u2q6m-serena-hall-s-projects.vercel.app",
        'https://lamppost-frontend-ey98u2q6m-serena-hall-s-projects.vercel.app/login',
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,    prefix="/auth",    tags=["auth"])
app.include_router(entries.router, prefix="/entries", tags=["entries"])
app.include_router(moods.router,   prefix="/moods",   tags=["moods"])
app.include_router(skills.router,  prefix="/skills",  tags=["skills"])

@app.get("/")
def root():
    return {"status": "Lamppost API is running"}

