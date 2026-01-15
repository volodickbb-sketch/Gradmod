"""API routes"""
from flask import Blueprint, jsonify, render_template
from app.utils.db_session import get_db_session
from app.services.statistics_service import StatisticsService
from app.services.test_service import TestService
from app.repository.user_repository import UserRepository

api_bp = Blueprint("api", __name__)


@api_bp.route("/")
def index():
    """Main dashboard page"""
    return render_template("dashboard.html")


@api_bp.route("/api/users")
def api_users():
    """API endpoint to get all users data"""
    db = get_db_session()
    try:
        user_repo = UserRepository
        test_service = TestService(db)
        
        users = user_repo.get_all(db)
        
        formatted_users = []
        for user in users:
            test_results = test_service.get_user_test_history(user.id)
            
            formatted_user = {
                "user_id": str(user.telegram_id),
                "language": user.language,
                "tests_count": len(test_results),
                "tests": []
            }
            
            for test in test_results:
                formatted_test = {
                    "date": test.created_at.isoformat(),
                    "scores": {
                        "personal": test.personal_burnout,
                        "study": test.study_burnout,
                        "total": test.total_burnout,
                    },
                }
                formatted_user["tests"].append(formatted_test)
            
            formatted_users.append(formatted_user)
        
        return jsonify(formatted_users)
    finally:
        db.close()


@api_bp.route("/api/statistics")
def api_statistics():
    """API endpoint to get overall statistics"""
    db = get_db_session()
    try:
        stats_service = StatisticsService(db)
        stats = stats_service.get_global_statistics()
        return jsonify(stats)
    finally:
        db.close()


@api_bp.route("/api/recent-tests")
def api_recent_tests():
    """API endpoint to get recent tests from all users"""
    db = get_db_session()
    try:
        test_service = TestService(db)
        
        recent_tests = test_service.get_recent_tests(limit=50)
        
        formatted_tests = []
        for test in recent_tests:
            formatted_tests.append({
                "user_id": str(test.user.telegram_id),
                "date": test.created_at.isoformat(),
                "scores": {
                    "personal": test.personal_burnout,
                    "study": test.study_burnout,
                    "total": test.total_burnout,
                },
            })
        
        return jsonify(formatted_tests)
    finally:
        db.close()
