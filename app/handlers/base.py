"""Base handler with database session"""
from app.utils.db_session import get_db_session
from app.services.user_service import UserService
from app.services.test_service import TestService


class BaseHandler:
    """Base handler with common functionality"""
    
    def __init__(self):
        self.db = get_db_session()
        self.user_service = UserService(self.db)
        self.test_service = TestService(self.db)
    
    def __del__(self):
        """Close database session"""
        if hasattr(self, 'db'):
            self.db.close()
