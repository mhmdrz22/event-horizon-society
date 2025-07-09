from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base import Base # Import Base and all models
# Potentially, you might need to explicitly import all your models here
# if app.db.base doesn't robustly import them due to load order,
# though app.db.base is designed to handle this.

# Create the database engine
# The connect_args is often needed for SQLite, but usually not for PostgreSQL
# For PostgreSQL, psycopg2 is the default driver if not specified in URI
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

def create_tables():
    # This will create all tables defined in models that inherit from Base
    # It's generally recommended to use Alembic for migrations in production
    # But for development and initial setup, create_all is fine.
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
async def app_startup():
    # This is one way to ensure tables are created when the app starts.
    # Be cautious with this in production if using a more robust migration tool.
    create_tables()
    print("Database tables created (if they didn't exist).")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
