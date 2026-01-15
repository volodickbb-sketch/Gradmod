"""Test result model"""
from sqlalchemy import Column, BigInteger, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base


class TestResult(Base):
    """Test result model"""
    __tablename__ = "test_results"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    personal_burnout = Column(Float, nullable=False)
    study_burnout = Column(Float, nullable=False)
    total_burnout = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="test_results")
    
    def __repr__(self):
        return f"<TestResult(user_id={self.user_id}, total_burnout={self.total_burnout})>"
