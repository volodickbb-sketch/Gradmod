"""Test service"""
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.test_result import TestResult
from app.repository.test_result_repository import TestResultRepository


class TestService:
    """Service for test operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = TestResultRepository
    
    def calculate_scores(self, answers: List[int]) -> Dict[str, float]:
        """Calculate burnout scores from answers"""
        # Item 10 (index 9) is reverse scored
        reversed_answers = answers.copy()
        reversed_answers[9] = 100 - reversed_answers[9]
        
        # Personal burnout (items 1-6, indices 0-5)
        personal_scores = reversed_answers[0:6]
        personal_burnout = sum(personal_scores) / len(personal_scores)
        
        # Study-related burnout (items 7-13, indices 6-13)
        study_scores = reversed_answers[6:13]
        study_burnout = sum(study_scores) / len(study_scores)
        
        # Total burnout
        total_burnout = (personal_burnout + study_burnout) / 2
        
        return {
            "personal": round(personal_burnout, 1),
            "study": round(study_burnout, 1),
            "total": round(total_burnout, 1),
        }
    
    def save_test_result(
        self,
        user_id: int,
        personal_burnout: float,
        study_burnout: float,
        total_burnout: float
    ) -> TestResult:
        """Save test result"""
        return self.repository.create(
            self.db,
            user_id,
            personal_burnout,
            study_burnout,
            total_burnout
        )
    
    def get_user_test_history(self, user_id: int, limit: int = 100) -> List[TestResult]:
        """Get user test history"""
        return self.repository.get_by_user_id(self.db, user_id, limit)
    
    def get_recent_tests(self, limit: int = 50) -> List[TestResult]:
        """Get recent tests from all users"""
        return self.repository.get_recent(self.db, limit)
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """Get user statistics"""
        return self.repository.get_statistics_by_user_id(self.db, user_id)
