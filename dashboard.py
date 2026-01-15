#!/usr/bin/env python3
"""
Admin dashboard web server for GradMood Bot
Provides web interface to view all user test results
"""

from app.api.app import run_dashboard

if __name__ == "__main__":
    run_dashboard(debug=True)
