from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.base import Base

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" # Ensures OpenAPI spec is under API prefix
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

from app.routers import auth as auth_router

app.include_router(auth_router.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
