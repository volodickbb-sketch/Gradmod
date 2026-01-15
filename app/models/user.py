"""User model"""
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    language = Column(String(2), default="en", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    test_results = relationship("TestResult", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, language={self.language})>"
