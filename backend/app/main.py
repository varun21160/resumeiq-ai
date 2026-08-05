from fastapi import FastAPI

from app.core.config import settings
from app.api import auth_router, users_router
from app.api.resume import router as resume_router
from app.api.ats import router as ats_router
from app.api.ai import router as ai_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    users_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    resume_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    ats_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    ai_router,
    prefix=settings.API_V1_PREFIX,
)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }