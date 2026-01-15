"""Database session utility"""
from app.config.database import SessionLocal


def get_db_session():
    """Get database session"""
    return SessionLocal()
