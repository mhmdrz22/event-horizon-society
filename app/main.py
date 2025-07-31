from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

if settings.BACKEND_CORS_ORIGINS_LIST:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url} Headers: {request.headers}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code} Headers: {dict(response.headers)}")
    return response

from app.routers import (
    auth as auth_router,
    news as news_router,
    article as article_router,
    event as event_router,
    comment as comment_router,
    membership_request as membership_request_router,
    event_registration as event_registration_router,
    user as user_router,
    notification as notification_router,
)

app.include_router(auth_router.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(news_router.router, prefix=f"{settings.API_V1_STR}/news", tags=["news"])
app.include_router(article_router.router, prefix=f"{settings.API_V1_STR}/articles", tags=["articles"])
app.include_router(event_router.router, prefix=f"{settings.API_V1_STR}/events", tags=["events"])
app.include_router(comment_router.router, prefix=f"{settings.API_V1_STR}/comments", tags=["comments"])
app.include_router(membership_request_router.router, prefix=f"{settings.API_V1_STR}/membership-requests", tags=["membership-requests"])
app.include_router(event_registration_router.router, prefix=f"{settings.API_V1_STR}", tags=["event-registrations"])
app.include_router(user_router.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(notification_router.router, prefix=f"{settings.API_V1_STR}/notifications", tags=["notifications"])

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
