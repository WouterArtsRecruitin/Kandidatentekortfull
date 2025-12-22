"""WSGI entry point for Render deployment."""
from webhook_simple import app

# Export for Gunicorn
application = app

if __name__ == "__main__":
    app.run()
