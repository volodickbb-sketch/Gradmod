"""Flask application"""
from flask import Flask
from app.api.routes import api_bp
from app.config.settings import settings


def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app


def run_dashboard(host=None, port=None, debug=None):
    """Run dashboard server"""
    app = create_app()
    host = host or settings.DASHBOARD_HOST
    port = port or settings.DASHBOARD_PORT
    debug = debug if debug is not None else settings.DEBUG
    
    print(f"Dashboard running on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug, use_reloader=False)
