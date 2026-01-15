"""User service"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repository.user_repository import UserRepository


class UserService:
    """Service for user operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository
    
    def get_or_create_user(self, telegram_id: int, language: str = "en") -> User:
        """Get user or create if not exists"""
        return self.repository.get_or_create(self.db, telegram_id, language)
    
    def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        return self.repository.get_by_telegram_id(self.db, telegram_id)
    
    def update_language(self, telegram_id: int, language: str) -> Optional[User]:
        """Update user language"""
        return self.repository.update_language(self.db, telegram_id, language)
    
    def get_user_language(self, telegram_id: int) -> str:
        """Get user language"""
        user = self.get_user(telegram_id)
        return user.language if user else "en"
