"""
Meta/Facebook Lead Ads Webhook Handler.
V2: Includes direct Typeform link for higher conversion.
"""

import os
from typing import Dict, Any
from flask import request, jsonify

from ..config import META_VERIFY_TOKEN, TYPEFORM_ID
from ..services import PipedriveService, EmailService, LeadScorer
from ..templates import get_meta_welcome_email
from ..utils import get_logger

logger = get_logger("meta_lead_handler")


def parse_meta_lead_data(data: Dict) -> Dict[str, Any]:
    """
    Parse Meta Lead Ads data.
    Supports both direct Facebook webhooks and Zapier-formatted data.
    """
    # Format 1: Zapier flat structure
    if 'email' in data:
        full_name = data.get('full_name', '')
        name_parts = full_name.split() if full_name else []

        return {
            'email': data.get('email', ''),
            'voornaam': data.get('voornaam', data.get('first_name', name_parts[0] if name_parts else '')),
            'achternaam': data.get('achternaam', data.get('last_name', ' '.join(name_parts[1:]) if len(name_parts) > 1 else '')),
            'contact': full_name or f"{data.get('voornaam', '')} {data.get('achternaam', '')}".strip(),
            'bedrijf': data.get('bedrijf', data.get('company_name', data.get('company', ''))),
            'telefoon': data.get('telefoon', data.get('phone_number', data.get('phone', ''))),
            'lead_id': data.get('lead_id', data.get('leadgen_id', '')),
            'form_id': data.get('form_id', ''),
            'source': 'meta_lead_ads'
        }

    # Format 2: Direct Facebook webhook (nested)
    if 'entry' in data:
        try:
            changes = data['entry'][0]['changes'][0]['value']
            field_data = {f['name']: f['values'][0] for f in changes.get('field_data', [])}
            full_name = field_data.get('full_name', '')
            name_parts = full_name.split() if full_name else []

            return {
                'email': field_data.get('email', ''),
                'voornaam': name_parts[0] if name_parts else '',
                'achternaam': ' '.join(name_parts[1:]) if len(name_parts) > 1 else '',
                'contact': full_name,
                'bedrijf': field_data.get('company_name', field_data.get('company', '')),
                'telefoon': field_data.get('phone_number', ''),
                'lead_id': changes.get('leadgen_id', ''),
                'form_id': changes.get('form_id', ''),
                'source': 'meta_lead_ads'
            }
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing Facebook webhook: {e}")

    # Fallback
    return {
        'email': data.get('email', ''),
        'voornaam': data.get('voornaam', data.get('name', '').split()[0] if data.get('name') else ''),
        'achternaam': '',
        'contact': data.get('name', data.get('voornaam', '')),
        'bedrijf': data.get('bedrijf', data.get('company', '')),
        'telefoon': data.get('telefoon', data.get('phone', '')),
        'lead_id': '',
        'form_id': '',
        'source': 'meta_lead_ads'
    }


def meta_lead_webhook():
    """
    Handle Meta/Facebook Lead Ads webhook.

    GET: Facebook webhook verification
    POST: Process lead data

    V2 improvements:
    - Direct Typeform link in welcome email
    - Lead scoring
    - Better tracking
    """
    # GET: Webhook verification
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == META_VERIFY_TOKEN:
            logger.info("Meta webhook verified")
            return challenge, 200
        else:
            logger.warning(f"Meta verification failed: mode={mode}")
            return "Verification failed", 403

    # POST: Process lead
    logger.info("META LEAD WEBHOOK RECEIVED")

    try:
        data = request.get_json(force=True, silent=True) or {}
        logger.info(f"Keys: {list(data.keys())}")

        # Parse lead data
        lead = parse_meta_lead_data(data)
        logger.info(f"Parsed lead: {lead}")

        # Validate email
        if not lead['email'] or '@' not in lead['email']:
            logger.error(f"No valid email: {lead}")
            return jsonify({"error": "No valid email", "parsed": lead}), 400

        voornaam = lead['voornaam'] or (lead['contact'].split()[0] if lead['contact'] else 'daar')

        # Calculate lead score
        scorer = LeadScorer()
        lead_score = scorer.score_from_meta_lead(lead)
        logger.info(f"Lead score: {lead_score.total_score} ({lead_score.category})")

        # Send welcome email with Typeform link
        email_service = EmailService()
        welcome_html = get_meta_welcome_email(
            voornaam=voornaam,
            bedrijf=lead['bedrijf'],
            email=lead['email'],
            typeform_prefill=True
        )

        email_sent = email_service.send(
            lead['email'],
            "👋 Welkom! Stuur je vacature voor gratis analyse",
            welcome_html
        ).success

        logger.info(f"Welcome email sent: {email_sent}")

        # Create Pipedrive records
        pipedrive = PipedriveService()

        org_id = None
        if lead['bedrijf']:
            org_id = pipedrive.create_organization(lead['bedrijf'])

        person_id = pipedrive.create_person(
            name=lead['contact'] or voornaam,
            email=lead['email'],
            phone=lead['telefoon'],
            org_id=org_id
        )

        # Create deal with note
        deal_note = f"""📱 LEAD VIA META/FACEBOOK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 GEGEVENS:
• Contact: {lead['contact']}
• Email: {lead['email']}
• Telefoon: {lead['telefoon'] or 'Niet opgegeven'}
• Bedrijf: {lead['bedrijf'] or 'Niet opgegeven'}
• Lead ID: {lead['lead_id']}
• Lead Score: {lead_score.total_score} ({lead_score.category})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 STATUS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Welkom email verstuurd (met Typeform link)
⏳ Wacht op vacaturetekst van contact

💡 Typeform link in email: kandidaat kan direct uploaden
"""

        deal_id = pipedrive.create_deal(
            title=f"Meta Lead - {lead['bedrijf'] or voornaam}",
            person_id=person_id,
            org_id=org_id
        )

        if deal_id:
            pipedrive.add_note(deal_id, deal_note, pinned=True)

        logger.info(f"Lead processed: email={email_sent}, deal={deal_id}")

        return jsonify({
            "success": True,
            "source": "meta_lead_ads",
            "email_sent": email_sent,
            "lead_score": lead_score.total_score,
            "lead_category": lead_score.category,
            "org_id": org_id,
            "person_id": person_id,
            "deal_id": deal_id
        }), 200

    except Exception as e:
        logger.error(f"Meta lead error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
