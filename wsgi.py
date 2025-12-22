"""WSGI entry point for Render deployment."""
from kandidatentekort_auto import app

# Export for Gunicorn
application = app

if __name__ == "__main__":
    app.run()
