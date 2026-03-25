import logging

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine

# IMPORTANT: import model so SQLAlchemy sees it before create_all()
from app.models.address import Address  # noqa: F401

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A minimal FastAPI address book application.",
)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting application...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified successfully.")


@app.get("/health")
def health_check() -> dict[str, str]:
    logger.info("Health check endpoint called.")
    return {"status": "ok"}