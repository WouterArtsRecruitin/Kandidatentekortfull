#!/usr/bin/env python3
"""
KANDIDATENTEKORT.NL - WEBHOOK V6
Deploy: Render.com

Features:
- Claude AI vacature analyse
- Mooie HTML email rapporten
- Pipedrive met custom fields + notes
- Async processing voor snelle response
"""

import os
import json
import logging
import smtplib
import requests
import threading
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
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
PIPEDRIVE_BASE = "https://api.pipedrive.com/v1"

# Pipedrive settings
PIPELINE_ID = 4      # Kandidatentekort pipeline
STAGE_ID = 21        # Gekwalificeerd stage
OWNER_ID = 23957248  # Wouter

# Custom field IDs (update after checking Pipedrive)
CUSTOM_FIELD_SCORE = os.getenv('PD_FIELD_SCORE', '')
CUSTOM_FIELD_ANALYSIS_DATE = os.getenv('PD_FIELD_ANALYSIS_DATE', '')


def pipedrive_request(method, endpoint, data=None):
    """Make Pipedrive API request."""
    url = f"{PIPEDRIVE_BASE}/{endpoint}?api_token={PIPEDRIVE_API_TOKEN}"
    try:
        if method == "POST":
            response = requests.post(url, json=data, timeout=30)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=30)
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


def add_pipedrive_note(deal_id, content, pinned=False):
    """Add a note to a Pipedrive deal."""
    note_data = {
        "deal_id": deal_id,
        "content": content,
        "pinned_to_deal_flag": 1 if pinned else 0
    }
    return pipedrive_request("POST", "notes", note_data)


def update_deal_custom_fields(deal_id, score=None, analysis_date=None):
    """Update custom fields on a deal."""
    update_data = {}
    if score and CUSTOM_FIELD_SCORE:
        update_data[CUSTOM_FIELD_SCORE] = score
    if analysis_date and CUSTOM_FIELD_ANALYSIS_DATE:
        update_data[CUSTOM_FIELD_ANALYSIS_DATE] = analysis_date

    if update_data:
        return pipedrive_request("PUT", f"deals/{deal_id}", update_data)
    return None


def create_pipedrive_deal(company_name, contact_name, email, phone="", vacancy_title="", vacancy_text=""):
    """Create organization, person, and deal in Pipedrive with enhanced data."""
    if not PIPEDRIVE_API_TOKEN:
        logger.error("PIPEDRIVE_API_TOKEN not set")
        return None

    # 1. Create Organization
    org_data = {"name": company_name, "owner_id": OWNER_ID}
    org = pipedrive_request("POST", "organizations", org_data)
    org_id = org.get('id') if org else None
    logger.info(f"Organization created: {org_id}")

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
    logger.info(f"Person created: {person_id}")

    # 3. Create Deal
    deal_title = f"Vacature Analyse - {company_name}"
    if vacancy_title:
        deal_title = f"Vacature Analyse - {company_name} - {vacancy_title}"

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
    logger.info(f"Deal created: {deal_id}")

    # 4. Add vacancy text as pinned note
    if deal_id and vacancy_text:
        note_content = f"""📝 ORIGINELE VACATURETEKST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Functie: {vacancy_title or 'Niet opgegeven'}
Bedrijf: {company_name}
Ingediend: {datetime.now().strftime('%d-%m-%Y %H:%M')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{vacancy_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        add_pipedrive_note(deal_id, note_content, pinned=True)
        logger.info(f"Vacancy note added to deal {deal_id}")

    return deal_id


def add_analysis_to_pipedrive(deal_id, analysis_result, score=None):
    """Add the Claude analysis result as a note and update custom fields."""
    if not deal_id:
        return

    # Add analysis as note
    note_content = f"""🎯 VACATURE ANALYSE RAPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Geanalyseerd: {datetime.now().strftime('%d-%m-%Y %H:%M')}
Score: {score}/100 punten

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{analysis_result}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    add_pipedrive_note(deal_id, note_content, pinned=True)

    # Update custom fields
    update_deal_custom_fields(deal_id, score=score, analysis_date=datetime.now().strftime('%Y-%m-%d'))
    logger.info(f"Analysis added to deal {deal_id}")


def generate_email_html(contact_name, company_name, vacancy_title, analysis_result, score=None):
    """Generate beautiful HTML email with analysis results."""

    # Score color based on value
    if score:
        if score >= 70:
            score_color = "#10B981"  # Green
            score_label = "Uitstekend"
        elif score >= 50:
            score_color = "#F59E0B"  # Orange
            score_label = "Goed"
        elif score >= 30:
            score_color = "#EF4444"  # Red
            score_label = "Verbetering nodig"
        else:
            score_color = "#DC2626"  # Dark red
            score_label = "Kritiek"
    else:
        score_color = "#6B7280"
        score_label = "Analyse"
        score = "?"

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f5;">

    <!-- Header -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, #FF6B35 0%, #FF8F5C 100%); padding: 40px 20px;">
        <tr>
            <td align="center">
                <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 600;">
                    🎯 Jouw Vacature Analyse is Klaar!
                </h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">
                    {company_name} • {vacancy_title or 'Vacature'}
                </p>
            </td>
        </tr>
    </table>

    <!-- Main Content -->
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <tr>
            <td>
                <!-- Score Card -->
                <div style="background: white; border-radius: 16px; padding: 30px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;">
                    <div style="display: inline-block; background: {score_color}; color: white; font-size: 48px; font-weight: 700; width: 100px; height: 100px; line-height: 100px; border-radius: 50%; margin-bottom: 15px;">
                        {score}
                    </div>
                    <p style="color: {score_color}; font-size: 18px; font-weight: 600; margin: 0;">
                        {score_label}
                    </p>
                    <p style="color: #6B7280; font-size: 14px; margin: 5px 0 0 0;">
                        van de 100 punten
                    </p>
                </div>

                <!-- Greeting -->
                <div style="background: white; border-radius: 16px; padding: 30px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="color: #1F2937; margin: 0 0 15px 0; font-size: 20px;">
                        Beste {contact_name},
                    </h2>
                    <p style="color: #4B5563; line-height: 1.6; margin: 0;">
                        Bedankt voor het indienen van je vacaturetekst! Onze AI heeft een uitgebreide analyse
                        gemaakt met concrete verbeterpunten om meer gekwalificeerde kandidaten aan te trekken.
                    </p>
                </div>

                <!-- Analysis Content -->
                <div style="background: white; border-radius: 16px; padding: 30px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="color: #1F2937; margin: 0 0 20px 0; font-size: 20px; border-bottom: 2px solid #FF6B35; padding-bottom: 10px;">
                        📊 Analyse Resultaten
                    </h2>
                    <div style="color: #374151; line-height: 1.8; white-space: pre-wrap; font-size: 15px;">
{analysis_result}
                    </div>
                </div>

                <!-- CTA Button -->
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://recruitin.nl/contact"
                       style="display: inline-block; background: #FF6B35; color: white; text-decoration: none;
                              padding: 16px 40px; border-radius: 8px; font-weight: 600; font-size: 16px;
                              box-shadow: 0 4px 14px rgba(255,107,53,0.4);">
                        📞 Bespreek de resultaten met een expert
                    </a>
                </div>

                <!-- What's Next -->
                <div style="background: #FFF7ED; border-radius: 16px; padding: 25px; margin: 20px 0; border-left: 4px solid #FF6B35;">
                    <h3 style="color: #9A3412; margin: 0 0 10px 0; font-size: 16px;">
                        💡 Wat nu?
                    </h3>
                    <ul style="color: #78350F; margin: 0; padding-left: 20px; line-height: 1.8;">
                        <li>Pas de verbeterpunten toe in je vacaturetekst</li>
                        <li>Test de nieuwe tekst op je doelgroep</li>
                        <li>Meet de resultaten (sollicitaties, views)</li>
                    </ul>
                </div>

            </td>
        </tr>
    </table>

    <!-- Footer -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background: #1F2937; padding: 30px 20px; margin-top: 20px;">
        <tr>
            <td align="center">
                <p style="color: #9CA3AF; font-size: 14px; margin: 0 0 10px 0;">
                    <strong style="color: white;">Recruitin B.V.</strong> | Kandidatentekort.nl
                </p>
                <p style="color: #6B7280; font-size: 12px; margin: 0;">
                    Dit is een automatisch gegenereerd rapport op basis van AI-analyse.<br>
                    Voor vragen: info@recruitin.nl
                </p>
            </td>
        </tr>
    </table>

</body>
</html>
"""
    return html


def send_confirmation_email(to_email, company_name, contact_name):
    """Send initial confirmation email."""
    if not GMAIL_APP_PASSWORD:
        logger.error("GMAIL_APP_PASSWORD not set")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"✅ Aanvraag ontvangen - {company_name}"
        msg['From'] = f"Recruitin <{GMAIL_USER}>"
        msg['To'] = to_email

        html = f"""
<!DOCTYPE html>
<html>
<body style="font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #f9fafb;">
    <div style="background: white; border-radius: 12px; padding: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h1 style="color: #FF6B35; margin: 0 0 20px 0;">✅ Aanvraag ontvangen!</h1>
        <p style="color: #374151; line-height: 1.6;">Beste {contact_name},</p>
        <p style="color: #374151; line-height: 1.6;">
            We hebben je vacaturetekst voor <strong>{company_name}</strong> ontvangen.
            Onze AI-analyse is gestart en je ontvangt binnen <strong>24 uur</strong> een uitgebreid rapport met:
        </p>
        <ul style="color: #374151; line-height: 1.8;">
            <li>📊 Score en beoordeling van je vacaturetekst</li>
            <li>🎯 Top 3 verbeterpunten</li>
            <li>✍️ Verbeterde versie van je vacature</li>
            <li>💡 Bonus tips voor meer sollicitaties</li>
        </ul>
        <p style="color: #374151; line-height: 1.6;">
            Met vriendelijke groet,<br>
            <strong>Het Recruitin Team</strong>
        </p>
    </div>
    <p style="color: #9CA3AF; font-size: 12px; text-align: center; margin-top: 20px;">
        Recruitin B.V. | Kandidatentekort.nl
    </p>
</body>
</html>
"""

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Confirmation email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Email failed: {e}")
        return False


def send_analysis_email(to_email, contact_name, company_name, vacancy_title, analysis_result, score=None):
    """Send the analysis report email."""
    if not GMAIL_APP_PASSWORD:
        logger.error("GMAIL_APP_PASSWORD not set")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🎯 Vacature Analyse Rapport - {company_name}"
        msg['From'] = f"Recruitin <{GMAIL_USER}>"
        msg['To'] = to_email

        html = generate_email_html(contact_name, company_name, vacancy_title, analysis_result, score)
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Analysis email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Analysis email failed: {e}")
        return False


def analyze_vacancy_with_claude(vacancy_text, company_name, vacancy_title=""):
    """Analyze vacancy using Claude API."""
    if not CLAUDE_API_KEY:
        logger.warning("CLAUDE_API_KEY not set, using placeholder")
        return None, None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        # Use the master prompt (this would be replaced with actual prompt)
        prompt = f"""Analyseer deze vacaturetekst en geef een score (0-100) plus concrete verbeterpunten.

VACATURE:
Bedrijf: {company_name}
Functie: {vacancy_title}

TEKST:
{vacancy_text}

Geef je analyse in dit format:
1. SCORE: [nummer]/100
2. TOP 3 VERBETERPUNTEN
3. VERBETERDE VACATURETEKST
4. BONUS TIPS"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = message.content[0].text

        # Extract score from analysis
        score = None
        if "SCORE:" in analysis:
            try:
                score_line = analysis.split("SCORE:")[1].split("\n")[0]
                score = int(''.join(filter(str.isdigit, score_line.split("/")[0])))
            except:
                score = 50  # Default if parsing fails

        return analysis, score

    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return None, None


def process_analysis_async(email, contact_name, company_name, vacancy_title, vacancy_text, deal_id):
    """Process analysis in background thread."""
    try:
        logger.info(f"Starting async analysis for {company_name}")

        # Perform Claude analysis
        analysis_result, score = analyze_vacancy_with_claude(vacancy_text, company_name, vacancy_title)

        if analysis_result:
            # Send analysis email
            send_analysis_email(email, contact_name, company_name, vacancy_title, analysis_result, score)

            # Add to Pipedrive
            add_analysis_to_pipedrive(deal_id, analysis_result, score)

            logger.info(f"Async analysis completed for {company_name}")
        else:
            logger.warning(f"No analysis result for {company_name}")

    except Exception as e:
        logger.error(f"Async analysis failed: {e}")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "version": "6.0",
        "features": {
            "email": bool(GMAIL_APP_PASSWORD),
            "pipedrive": bool(PIPEDRIVE_API_TOKEN),
            "claude": bool(CLAUDE_API_KEY)
        },
        "timestamp": datetime.now().isoformat()
    })


@app.route('/webhook/typeform', methods=['POST'])
def typeform_webhook():
    """Handle Typeform submissions with async processing."""
    try:
        data = request.get_json()
        logger.info("Typeform webhook received")

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
                if not contact_name:
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

        logger.info(f"Parsed: {company_name} | {contact_name} | {email}")

        # 1. Create Pipedrive deal (sync - fast)
        deal_id = create_pipedrive_deal(company_name, contact_name, email, phone, vacancy_title, vacancy_text)

        # 2. Send confirmation email (sync - fast)
        email_sent = False
        if email:
            email_sent = send_confirmation_email(email, company_name, contact_name)

        # 3. Start async analysis (background - slow)
        if email and vacancy_text:
            thread = threading.Thread(
                target=process_analysis_async,
                args=(email, contact_name, company_name, vacancy_title, vacancy_text, deal_id)
            )
            thread.daemon = True
            thread.start()
            logger.info("Async analysis thread started")

        # Return fast response
        return jsonify({
            "status": "success",
            "company": company_name,
            "deal_id": deal_id,
            "email_sent": email_sent,
            "analysis": "processing_async"
        }), 200

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """Direct API endpoint for analysis (for testing)."""
    try:
        data = request.get_json()
        vacancy_text = data.get('vacancy_text', '')
        company_name = data.get('company', 'Test')
        vacancy_title = data.get('title', '')

        if not vacancy_text:
            return jsonify({"error": "vacancy_text required"}), 400

        analysis, score = analyze_vacancy_with_claude(vacancy_text, company_name, vacancy_title)

        return jsonify({
            "status": "success",
            "score": score,
            "analysis": analysis
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """Home endpoint."""
    return jsonify({
        "service": "Kandidatentekort Webhook",
        "version": "6.0",
        "features": ["email", "pipedrive", "claude-ai", "async-processing"],
        "endpoints": ["/health", "/webhook/typeform", "/api/analyze"]
    })


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
