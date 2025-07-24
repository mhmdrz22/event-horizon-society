from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS_LIST:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
    admin as admin_router,
)

app.include_router(auth_router.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(admin_router.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(news_router.router, prefix=f"{settings.API_V1_STR}/news", tags=["news"])
app.include_router(article_router.router, prefix=f"{settings.API_V1_STR}/articles", tags=["articles"])
app.include_router(event_router.router, prefix=f"{settings.API_V1_STR}/events", tags=["events"])
app.include_router(comment_router.router, prefix=f"{settings.API_V1_STR}/comments", tags=["comments"])
app.include_router(membership_request_router.router, prefix=f"{settings.API_V1_STR}/membership-requests", tags=["membership-requests"])
app.include_router(event_registration_router.router, prefix=f"{settings.API_V1_STR}", tags=["event-registrations"]) # No prefix for this one as it has its own
app.include_router(user_router.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(notification_router.router, prefix=f"{settings.API_V1_STR}/notifications", tags=["notifications"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
