from fastapi import FastAPI

from .config import get_settings
from .middleware import tenant_middleware
from .routers import health

settings = get_settings()

app = FastAPI(title=settings.api_title)

app.middleware("http")(tenant_middleware)
app.include_router(health.router)

