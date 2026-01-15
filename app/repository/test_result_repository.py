"""Test result repository"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.test_result import TestResult


class TestResultRepository:
    """Repository for test result operations"""
    
    @staticmethod
    def create(
        db: Session,
        user_id: int,
        personal_burnout: float,
        study_burnout: float,
        total_burnout: float
    ) -> TestResult:
        """Create new test result"""
        test_result = TestResult(
            user_id=user_id,
            personal_burnout=personal_burnout,
            study_burnout=study_burnout,
            total_burnout=total_burnout
        )
        db.add(test_result)
        db.commit()
        db.refresh(test_result)
        return test_result
    
    @staticmethod
    def get_by_user_id(db: Session, user_id: int, limit: int = 100) -> List[TestResult]:
        """Get test results by user ID"""
        return (
            db.query(TestResult)
            .filter(TestResult.user_id == user_id)
            .order_by(desc(TestResult.created_at))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_recent(db: Session, limit: int = 50) -> List[TestResult]:
        """Get recent test results from all users"""
        return (
            db.query(TestResult)
            .order_by(desc(TestResult.created_at))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_by_id(db: Session, test_id: int) -> Optional[TestResult]:
        """Get test result by ID"""
        return db.query(TestResult).filter(TestResult.id == test_id).first()
    
    @staticmethod
    def count_by_user_id(db: Session, user_id: int) -> int:
        """Count test results for user"""
        return db.query(TestResult).filter(TestResult.user_id == user_id).count()
    
    @staticmethod
    def count_all(db: Session) -> int:
        """Count all test results"""
        return db.query(TestResult).count()
    
    @staticmethod
    def get_statistics_by_user_id(db: Session, user_id: int) -> dict:
        """Get statistics for user"""
        results = TestResultRepository.get_by_user_id(db, user_id)
        
        if not results:
            return {
                "avg_personal_burnout": 0.0,
                "avg_study_burnout": 0.0,
                "avg_total_burnout": 0.0,
                "total_tests": 0,
            }
        
        personal_scores = [r.personal_burnout for r in results]
        study_scores = [r.study_burnout for r in results]
        total_scores = [r.total_burnout for r in results]
        
        return {
            "avg_personal_burnout": round(sum(personal_scores) / len(personal_scores), 1),
            "avg_study_burnout": round(sum(study_scores) / len(study_scores), 1),
            "avg_total_burnout": round(sum(total_scores) / len(total_scores), 1),
            "total_tests": len(results),
        }
    
    @staticmethod
    def get_global_statistics(db: Session) -> dict:
        """Get global statistics"""
        results = db.query(TestResult).all()
        
        if not results:
            return {
                "avg_personal_burnout": 0.0,
                "avg_study_burnout": 0.0,
                "avg_total_burnout": 0.0,
                "total_tests": 0,
            }
        
        personal_scores = [r.personal_burnout for r in results]
        study_scores = [r.study_burnout for r in results]
        total_scores = [r.total_burnout for r in results]
        
        return {
            "avg_personal_burnout": round(sum(personal_scores) / len(personal_scores), 1),
            "avg_study_burnout": round(sum(study_scores) / len(study_scores), 1),
            "avg_total_burnout": round(sum(total_scores) / len(total_scores), 1),
            "total_tests": len(results),
        }
