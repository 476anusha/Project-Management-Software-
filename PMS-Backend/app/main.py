from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, onboarding, workspaces, projects, issues, teams, sprints, labels, timeline

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# ✅ TEMP DEV-FRIENDLY CORS (FIXES AUTH IMMEDIATELY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api")
app.include_router(onboarding.router, prefix="/api")
app.include_router(workspaces.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(issues.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(sprints.router, prefix="/api")
app.include_router(labels.router, prefix="/api")
app.include_router(timeline.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to PMS API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
