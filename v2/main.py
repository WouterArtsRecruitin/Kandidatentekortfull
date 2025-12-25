#!/usr/bin/env python3
"""
KANDIDATENTEKORT V2 - Modular Automation Engine
================================================

Flask application entry point with all webhook handlers.

Improvements over V1:
- Modular code structure (services, handlers, templates)
- Automatic Claude analysis with async processing
- Lead scoring system
- Improved Meta Lead Ads flow with direct Typeform link
- Retry logic with exponential backoff
- Structured logging
- Better error handling

Endpoints:
    GET  /                  - Health check
    GET  /health/detailed   - Detailed health check per service
    POST /webhook/typeform  - Typeform submissions
    POST /webhook/meta-lead - Meta/Facebook Lead Ads
    POST /update-pdf-urls   - Add PDF URLs to deal
    POST /send-pdf-email    - Send PDF delivery email
    POST /nurture/process   - Process pending nurture emails
    GET  /test-email        - Test email sending

Deploy: Render.com or similar
Author: Kandidatentekort.nl
Version: 2.0
"""

from flask import Flask, jsonify
from datetime import datetime

from .config import get_config_status, validate_config
from .handlers.typeform import typeform_webhook
from .handlers.meta_lead import meta_lead_webhook
from .handlers.manual import update_pdf_urls, send_pdf_email, test_email
from .nurture.processor import process_pending_nurtures
from .utils import get_logger

logger = get_logger("main")

# =============================================================================
# FLASK APP
# =============================================================================

app = Flask(__name__)

# Log startup
logger.info("=" * 60)
logger.info("KANDIDATENTEKORT V2 STARTING")
logger.info("=" * 60)

# Validate config
config_issues = validate_config()
if config_issues:
    for issue in config_issues:
        logger.warning(f"CONFIG: {issue}")
else:
    logger.info("CONFIG: All required variables set")


# =============================================================================
# HEALTH ENDPOINTS
# =============================================================================

@app.route("/", methods=["GET"])
def home():
    """Basic health check."""
    return jsonify({
        "status": "healthy",
        "version": "2.0",
        "name": "Kandidatentekort V2",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Basic health check (alias)."""
    return home()


@app.route("/health/detailed", methods=["GET"])
def health_detailed():
    """Detailed health check with service status."""
    config = get_config_status()

    return jsonify({
        "status": "healthy",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "services": config,
        "features": {
            "auto_analysis": config.get("auto_analysis", False),
            "lead_scoring": config.get("lead_scoring", False),
            "nurture_emails": True,
            "pdf_generation": config.get("pdfmonkey", False) or True,  # ReportLab fallback
        }
    }), 200


# =============================================================================
# WEBHOOK ENDPOINTS
# =============================================================================

@app.route("/webhook/typeform", methods=["POST"])
def handle_typeform():
    """Handle Typeform webhook submissions."""
    return typeform_webhook()


@app.route("/webhook/meta-lead", methods=["POST", "GET"])
def handle_meta_lead():
    """Handle Meta/Facebook Lead Ads webhook."""
    return meta_lead_webhook()


# =============================================================================
# MANUAL PROCESSING ENDPOINTS
# =============================================================================

@app.route("/update-pdf-urls", methods=["POST"])
def handle_update_pdf_urls():
    """Update deal with PDF URLs."""
    return update_pdf_urls()


@app.route("/send-pdf-email", methods=["POST"])
def handle_send_pdf_email():
    """Send PDF delivery email."""
    return send_pdf_email()


# =============================================================================
# NURTURE ENDPOINTS
# =============================================================================

@app.route("/nurture/process", methods=["POST"])
def handle_nurture_process():
    """Process pending nurture emails for all eligible deals."""
    return process_pending_nurtures()


# =============================================================================
# TEST ENDPOINTS
# =============================================================================

@app.route("/test-email", methods=["GET"])
def handle_test_email():
    """Test email sending."""
    return test_email()


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "status": 404}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error", "status": 500}), 500


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    logger.info(f"Starting server on port {port} (debug={debug})")
    app.run(host="0.0.0.0", port=port, debug=debug)
