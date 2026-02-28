import logging
from datetime import datetime
from edutracker.infrastructure.db.Auth.auth_database import SessionLocal
from edutracker.application.services.auth.auth_service import AuthService

logger = logging.getLogger(__name__)


def run_refresh_cleanup():
    db = SessionLocal()
    try:
        service = AuthService(db)
        deleted = service.cleanup_refresh_token()
        logger.info("Cleanup refresh tokens: deleted=%s at=%s", deleted, datetime.utcnow())
    finally:
        db.close()
