"""Repository module"""
from app.repository.user_repository import UserRepository
from app.repository.test_result_repository import TestResultRepository

__all__ = ["UserRepository", "TestResultRepository"]
