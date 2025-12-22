#!/usr/bin/env python3
"""
KANDIDATENTEKORT.NL - SIMPLE EMAIL WEBHOOK
Deploy: Render.com
Version: 1.0 - Email only, no complex integrations
"""

import os
import json
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Config
GMAIL_USER = os.getenv('GMAIL_USER', 'artsrecruitin@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD') or os.getenv('GMAIL_PASS')


def send_simple_email(to_email, company_name, contact_name):
    """Send simple confirmation email."""
    if not GMAIL_APP_PASSWORD:
        logger.error("GMAIL_APP_PASSWORD not set")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Bedankt voor je Recruitment APK aanvraag - {company_name}"
        msg['From'] = f"Recruitin <{GMAIL_USER}>"
        msg['To'] = to_email

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #FF6B35;">Bedankt {contact_name}!</h1>
            <p>We hebben je aanvraag voor de Recruitment APK voor <strong>{company_name}</strong> ontvangen.</p>
            <p>Je ontvangt binnenkort een uitgebreide analyse van je vacaturetekst met concrete verbeterpunten.</p>
            <br>
            <p>Met vriendelijke groet,</p>
            <p><strong>Het Recruitin Team</strong></p>
            <hr style="border: 1px solid #eee; margin: 20px 0;">
            <p style="color: #666; font-size: 12px;">
                Recruitin B.V. | Kandidatentekort.nl<br>
                Dit is een automatisch bericht.
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        logger.info(f"✅ Email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"❌ Email failed: {e}")
        return False


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Render."""
    return jsonify({
        "status": "healthy",
        "version": "1.0-simple",
        "email": bool(GMAIL_APP_PASSWORD),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/webhook/typeform', methods=['POST'])
def typeform_webhook():
    """Handle Typeform submissions - send confirmation email."""
    try:
        data = request.get_json()
        logger.info(f"📥 Typeform webhook received")

        # Extract data from Typeform
        answers = data.get('form_response', {}).get('answers', [])

        # Map answers (adjust field IDs as needed)
        company_name = ""
        contact_name = ""
        email = ""

        for answer in answers:
            field_ref = answer.get('field', {}).get('ref', '')

            if 'bedrijfsnaam' in field_ref.lower() or 'company' in field_ref.lower():
                company_name = answer.get('text', '')
            elif 'naam' in field_ref.lower() or 'name' in field_ref.lower():
                contact_name = answer.get('text', '')
            elif 'email' in field_ref.lower():
                email = answer.get('email', '')

        # Fallback to hidden fields if not found
        hidden = data.get('form_response', {}).get('hidden', {})
        if not email:
            email = hidden.get('email', '')
        if not company_name:
            company_name = hidden.get('company', 'Onbekend')
        if not contact_name:
            contact_name = hidden.get('name', 'daar')

        logger.info(f"📋 Data: {company_name} | {contact_name} | {email}")

        if email:
            send_simple_email(email, company_name, contact_name)
        else:
            logger.warning("⚠️ No email found in submission")

        return jsonify({"status": "received", "company": company_name}), 200

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """Home endpoint."""
    return jsonify({
        "service": "Kandidatentekort Simple Webhook",
        "version": "1.0",
        "endpoints": ["/health", "/webhook/typeform"]
    })


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
