import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routes import router as address_router
from app.api.v1.auth import router as auth_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.db.base import Base
from app.db.session import engine

from app.models.address import Address

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified successfully.")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A minimal FastAPI address book application.",
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)
app.include_router(auth_router)
app.include_router(address_router)
register_exception_handlers(app)


@app.get("/health")
def health_check() -> dict[str, str]:
    logger.info("Health check endpoint called.")
    return {"status": "ok"}