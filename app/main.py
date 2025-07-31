from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.routers import event, auth, user, notification, news
import logging
from fastapi.responses import FileResponse
from fastapi import Request

app = FastAPI()

# تنظیم لاگ‌ها
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# مونت کردن فایل‌های استاتیک
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# لاگ کردن درخواست‌ها
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url} Headers: {request.headers}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code} Headers: {dict(response.headers)}")
    return response

# شامل کردن routerها
app.include_router(event.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(notification.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")

# route پیش‌فرض
@app.get("/")
async def root():
    return {"message": "Welcome to Event Horizon Society"}
