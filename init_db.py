#!/usr/bin/env python3
"""Initialize database"""
from app.config.database import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")
