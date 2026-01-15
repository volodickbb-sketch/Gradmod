"""Statistics service"""
from typing import Dict
from sqlalchemy.orm import Session
from app.repository.user_repository import UserRepository
from app.repository.test_result_repository import TestResultRepository


class StatisticsService:
    """Service for statistics operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository
        self.test_repository = TestResultRepository
    
    def get_global_statistics(self) -> Dict:
        """Get global statistics"""
        total_users = self.user_repository.count(self.db)
        test_stats = self.test_repository.get_global_statistics(self.db)
        
        return {
            "total_users": total_users,
            "total_tests": test_stats["total_tests"],
            "avg_personal_burnout": test_stats["avg_personal_burnout"],
            "avg_study_burnout": test_stats["avg_study_burnout"],
            "avg_total_burnout": test_stats["avg_total_burnout"],
        }
