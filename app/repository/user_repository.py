"""User repository"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    """Repository for user operations"""
    
    @staticmethod
    def get_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        return db.query(User).filter(User.telegram_id == telegram_id).first()
    
    @staticmethod
    def create(db: Session, telegram_id: int, language: str = "en") -> User:
        """Create new user"""
        user = User(telegram_id=telegram_id, language=language)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_language(db: Session, telegram_id: int, language: str) -> Optional[User]:
        """Update user language"""
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.language = language
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def get_or_create(db: Session, telegram_id: int, language: str = "en") -> User:
        """Get user or create if not exists"""
        user = UserRepository.get_by_telegram_id(db, telegram_id)
        if not user:
            user = UserRepository.create(db, telegram_id, language)
        return user
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        """Get all users"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def count(db: Session) -> int:
        """Count all users"""
        return db.query(User).count()
