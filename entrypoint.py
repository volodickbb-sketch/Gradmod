#!/usr/bin/env python3
"""Entrypoint script for Docker container"""
import os
import sys
import time
import subprocess
from app.config.database import init_db

def wait_for_db():
    """Wait for database to be ready"""
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    
    print(f"Waiting for database at {db_host}:{db_port}...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", db_host, "-p", db_port, "-U", db_user],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Database is ready!")
                return True
        except FileNotFoundError:
            # pg_isready not available, try to connect directly
            try:
                from app.config.database import engine
                with engine.connect() as conn:
                    print("✅ Database is ready!")
                    return True
            except Exception:
                pass
        
        retry_count += 1
        time.sleep(1)
    
    print("❌ Database is not ready after 30 seconds")
    return False

if __name__ == "__main__":
    if not wait_for_db():
        sys.exit(1)
    
    print("Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
        # Continue anyway, tables might already exist
    
    print("Starting bot...")
    # Start the bot
    from bot import main
    main()
