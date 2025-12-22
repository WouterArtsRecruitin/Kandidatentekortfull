#!/usr/bin/env python3
"""
KANDIDATENTEKORT.NL - WEBHOOK V2
Deploy: Render.com
- Email bevestiging sturen
- Pipedrive deal aanmaken
"""

import os
import json
import logging
import smtplib
import requests
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
PIPEDRIVE_API_TOKEN = os.getenv('PIPEDRIVE_API_TOKEN')
PIPEDRIVE_BASE = "https://api.pipedrive.com/v1"

# Pipedrive settings
PIPELINE_ID = 4      # Kandidatentekort pipeline
STAGE_ID = 21        # Gekwalificeerd stage
OWNER_ID = 23957248  # Wouter


def pipedrive_request(method, endpoint, data=None):
    """Make Pipedrive API request."""
    url = f"{PIPEDRIVE_BASE}/{endpoint}?api_token={PIPEDRIVE_API_TOKEN}"
    try:
        if method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.get(url, timeout=30)

        result = response.json()
        if result.get('success'):
            return result.get('data')
        else:
            logger.error(f"Pipedrive error: {result.get('error')}")
            return None
    except Exception as e:
        logger.error(f"Pipedrive request failed: {e}")
        return None


def create_pipedrive_deal(company_name, contact_name, email, phone="", vacancy_title=""):
    """Create organization, person, and deal in Pipedrive."""
    if not PIPEDRIVE_API_TOKEN:
        logger.error("PIPEDRIVE_API_TOKEN not set")
        return None

    # 1. Create Organization
    org_data = {"name": company_name, "owner_id": OWNER_ID}
    org = pipedrive_request("POST", "organizations", org_data)
    org_id = org.get('id') if org else None
    logger.info(f"📁 Organization created: {org_id}")

    # 2. Create Person
    person_data = {
        "name": contact_name,
        "email": [email] if email else [],
        "phone": [phone] if phone else [],
        "org_id": org_id,
        "owner_id": OWNER_ID
    }
    person = pipedrive_request("POST", "persons", person_data)
    person_id = person.get('id') if person else None
    logger.info(f"👤 Person created: {person_id}")

    # 3. Create Deal
    deal_title = f"APK - {company_name}"
    if vacancy_title:
        deal_title = f"APK - {company_name} - {vacancy_title}"

    deal_data = {
        "title": deal_title,
        "org_id": org_id,
        "person_id": person_id,
        "pipeline_id": PIPELINE_ID,
        "stage_id": STAGE_ID,
        "user_id": OWNER_ID,
        "status": "open"
    }
    deal = pipedrive_request("POST", "deals", deal_data)
    deal_id = deal.get('id') if deal else None
    logger.info(f"💼 Deal created: {deal_id}")

    return deal_id


def send_confirmation_email(to_email, company_name, contact_name):
    """Send confirmation email."""
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
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "version": "2.0",
        "email": bool(GMAIL_APP_PASSWORD),
        "pipedrive": bool(PIPEDRIVE_API_TOKEN),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/webhook/typeform', methods=['POST'])
def typeform_webhook():
    """Handle Typeform submissions."""
    try:
        data = request.get_json()
        logger.info(f"📥 Typeform webhook received")

        # Extract answers
        answers = data.get('form_response', {}).get('answers', [])
        hidden = data.get('form_response', {}).get('hidden', {})

        # Initialize variables
        company_name = ""
        contact_name = ""
        email = ""
        phone = ""
        vacancy_title = ""
        vacancy_text = ""

        # Parse answers
        for answer in answers:
            field = answer.get('field', {})
            field_ref = field.get('ref', '').lower()
            field_type = answer.get('type', '')

            # Get value based on type
            if field_type == 'text':
                value = answer.get('text', '')
            elif field_type == 'email':
                value = answer.get('email', '')
            elif field_type == 'phone_number':
                value = answer.get('phone_number', '')
            elif field_type == 'long_text':
                value = answer.get('text', '')
            else:
                value = str(answer.get(field_type, ''))

            # Map to fields
            if 'bedrijf' in field_ref or 'company' in field_ref:
                company_name = value
            elif 'naam' in field_ref or 'name' in field_ref:
                if not contact_name:  # First name field
                    contact_name = value
            elif 'email' in field_ref:
                email = value
            elif 'telefoon' in field_ref or 'phone' in field_ref:
                phone = value
            elif 'functie' in field_ref or 'titel' in field_ref or 'title' in field_ref:
                vacancy_title = value
            elif 'vacature' in field_ref or 'tekst' in field_ref:
                vacancy_text = value

        # Fallback to hidden fields
        if not email:
            email = hidden.get('email', '')
        if not company_name:
            company_name = hidden.get('company', hidden.get('bedrijf', 'Onbekend'))
        if not contact_name:
            contact_name = hidden.get('name', hidden.get('naam', 'daar'))

        logger.info(f"📋 Parsed: {company_name} | {contact_name} | {email}")

        # 1. Create Pipedrive deal
        deal_id = create_pipedrive_deal(company_name, contact_name, email, phone, vacancy_title)

        # 2. Send confirmation email
        email_sent = False
        if email:
            email_sent = send_confirmation_email(email, company_name, contact_name)

        return jsonify({
            "status": "success",
            "company": company_name,
            "deal_id": deal_id,
            "email_sent": email_sent
        }), 200

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """Home endpoint."""
    return jsonify({
        "service": "Kandidatentekort Webhook",
        "version": "2.0",
        "features": ["email", "pipedrive"],
        "endpoints": ["/health", "/webhook/typeform"]
    })


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
