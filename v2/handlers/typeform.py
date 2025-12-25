"""
Typeform Webhook Handler - Main lead capture endpoint.
V2: Re-enables automatic Claude analysis with async processing.
"""

import threading
from typing import Dict, Any, Optional
from flask import request, jsonify
from datetime import datetime

from ..config import ENABLE_AUTO_ANALYSIS, ENABLE_ASYNC_PROCESSING
from ..services import (
    PipedriveService,
    analyze_vacancy,
    EmailService,
    PDFGenerator,
    LeadScorer
)
from ..templates import get_confirmation_email, get_analysis_report_email
from ..utils import get_logger, extract_text_from_file

logger = get_logger("typeform_handler")


def parse_typeform_data(webhook_data: Dict) -> Dict[str, Any]:
    """
    Parse Typeform webhook data into structured format.
    Handles all field types robustly.
    """
    result = {
        'email': '',
        'voornaam': 'daar',
        'contact': 'Onbekend',
        'telefoon': '',
        'bedrijf': 'Onbekend',
        'vacature': '',
        'functie': 'vacature',
        'sector': '',
        'file_url': '',
        'prefilled': False  # Was data pre-filled from quick analyzer?
    }

    try:
        form_response = webhook_data.get('form_response', {})
        answers = form_response.get('answers', [])
        hidden_fields = form_response.get('hidden', {})

        logger.info(f"Parsing {len(answers)} answers")

        # Check for pre-filled data (from quick analyzer)
        if hidden_fields.get('source') == 'quick_analyzer':
            result['prefilled'] = True

        # Collect short_text values
        texts = []

        for answer in answers:
            if not isinstance(answer, dict):
                continue

            field = answer.get('field', {})
            field_type = field.get('type', '')

            # Email
            if field_type == 'email':
                result['email'] = answer.get('email', '')
                logger.info(f"Found email: {result['email']}")

            # Phone
            elif field_type == 'phone_number':
                result['telefoon'] = answer.get('phone_number', '')

            # Short text (name, company, etc)
            elif field_type == 'short_text':
                texts.append(answer.get('text', ''))

            # Long text (vacancy)
            elif field_type == 'long_text':
                text = answer.get('text', '')
                result['vacature'] = text
                # Extract function title from first line
                if text:
                    first_line = text.split('\n')[0][:50]
                    result['functie'] = first_line

            # Multiple choice (sector)
            elif field_type == 'multiple_choice':
                choice = answer.get('choice', {})
                if isinstance(choice, dict):
                    result['sector'] = choice.get('label', '')

            # File upload
            elif field_type == 'file_upload':
                result['file_url'] = answer.get('file_url', '')
                logger.info(f"Found file upload")

            # Contact info block
            elif field_type == 'contact_info':
                info = answer.get('contact_info', {})
                if isinstance(info, dict):
                    if info.get('email'):
                        result['email'] = info['email']
                    if info.get('first_name'):
                        result['voornaam'] = info['first_name']
                        result['contact'] = f"{info.get('first_name', '')} {info.get('last_name', '')}".strip()
                    if info.get('phone_number'):
                        result['telefoon'] = info['phone_number']
                    if info.get('company'):
                        result['bedrijf'] = info['company']

        # Process collected text fields (typically: voornaam, achternaam, bedrijf)
        if texts:
            if len(texts) >= 1 and result['voornaam'] == 'daar':
                result['voornaam'] = texts[0]
                result['contact'] = texts[0]
            if len(texts) >= 2:
                result['contact'] = f"{texts[0]} {texts[1]}".strip()
            if len(texts) >= 3 and result['bedrijf'] == 'Onbekend':
                result['bedrijf'] = texts[2]

        logger.info(f"Parsed: email={result['email']}, contact={result['contact']}, bedrijf={result['bedrijf']}")

    except Exception as e:
        logger.error(f"Parse error: {e}", exc_info=True)

    return result


def process_analysis_async(
    deal_id: int,
    vacancy_text: str,
    email: str,
    voornaam: str,
    bedrijf: str,
    functie: str
):
    """
    Background task: Analyze vacancy, generate PDFs, send email.
    This runs in a separate thread to not block the webhook response.
    """
    try:
        logger.info(f"[ASYNC] Starting analysis for deal {deal_id}")

        # 1. Run Claude analysis
        analysis = analyze_vacancy(vacancy_text, bedrijf)

        if not analysis.success:
            logger.error(f"[ASYNC] Analysis failed for deal {deal_id}: {analysis.error}")
            # Add note to Pipedrive about failure
            pipedrive = PipedriveService()
            pipedrive.add_note(deal_id, f"⚠️ Automatische analyse mislukt: {analysis.error}")
            return

        logger.info(f"[ASYNC] Analysis complete: score={analysis.score}")

        # 2. Generate PDF
        pdf_gen = PDFGenerator()
        pdf_result = pdf_gen.generate_analysis_report(
            bedrijf, voornaam, functie, analysis
        )

        # 3. Add analysis to Pipedrive
        pipedrive = PipedriveService()
        pipedrive.add_analysis_to_deal(deal_id, analysis)

        # 4. Send analysis email
        email_service = EmailService()
        html = get_analysis_report_email(
            voornaam=voornaam,
            bedrijf=bedrijf,
            score=analysis.score,
            score_section=analysis.score_section,
            improvements=analysis.top_3_improvements,
            improved_text=analysis.improved_text,
            bonus_tips=analysis.bonus_tips,
            original_text=vacancy_text[:500]
        )

        attachments = []
        if pdf_result.success and pdf_result.pdf_bytes:
            attachments.append((f"Analyse_{bedrijf}.pdf", pdf_result.pdf_bytes))

        email_service.send(
            to_email=email,
            subject=f"🎯 Jouw Vacature-Analyse voor {bedrijf} is Klaar!",
            html_body=html,
            attachments=attachments if attachments else None
        )

        # 5. Trigger nurture sequence
        pipedrive.trigger_nurture(deal_id)

        logger.info(f"[ASYNC] Complete for deal {deal_id}")

    except Exception as e:
        logger.error(f"[ASYNC] Error for deal {deal_id}: {e}", exc_info=True)


def typeform_webhook():
    """
    Handle Typeform webhook submissions.

    Flow:
    1. Parse form data
    2. Validate email
    3. Extract file content if uploaded
    4. Send confirmation email (immediate)
    5. Create Pipedrive records
    6. Calculate lead score
    7. Start async analysis (if enabled)
    """
    logger.info("TYPEFORM WEBHOOK RECEIVED")

    try:
        data = request.get_json(force=True, silent=True) or {}
        logger.info(f"Keys: {list(data.keys())}")

        # Parse data
        parsed = parse_typeform_data(data)

        # Validate email
        if not parsed['email'] or '@' not in parsed['email']:
            logger.error(f"No valid email: {parsed}")
            return jsonify({"error": "No valid email", "parsed": parsed}), 400

        # Extract file content if uploaded
        vacancy_text = parsed['vacature']
        if parsed['file_url']:
            logger.info("Extracting text from uploaded file...")
            extracted = extract_text_from_file(parsed['file_url'])
            if extracted and len(extracted) > 50:
                vacancy_text = extracted
                logger.info(f"Using extracted file text: {len(extracted)} chars")

        # Send confirmation email immediately
        email_service = EmailService()
        confirmation_html = get_confirmation_email(
            parsed['voornaam'],
            parsed['bedrijf'],
            parsed['functie']
        )
        confirmation_sent = email_service.send(
            parsed['email'],
            f"✅ Ontvangen: Vacature-analyse voor {parsed['functie']}",
            confirmation_html
        ).success

        # Create Pipedrive records
        pipedrive = PipedriveService()
        lead_result = pipedrive.create_full_lead(
            company_name=parsed['bedrijf'],
            contact_name=parsed['contact'],
            email=parsed['email'],
            phone=parsed['telefoon'],
            vacancy_title=parsed['functie'],
            vacancy_text=vacancy_text,
            source='typeform_prefilled' if parsed['prefilled'] else 'typeform'
        )

        deal_id = lead_result.get('deal_id')

        # Calculate and store lead score
        scorer = LeadScorer()
        lead_score = scorer.score_from_typeform(parsed)
        logger.info(f"Lead score: {lead_score.total_score} ({lead_score.category})")

        # Start async analysis if enabled and we have vacancy text
        analysis_started = False
        if ENABLE_AUTO_ANALYSIS and vacancy_text and len(vacancy_text) > 100 and deal_id:
            if ENABLE_ASYNC_PROCESSING:
                # Run in background thread
                thread = threading.Thread(
                    target=process_analysis_async,
                    args=(deal_id, vacancy_text, parsed['email'], parsed['voornaam'], parsed['bedrijf'], parsed['functie'])
                )
                thread.daemon = True
                thread.start()
                analysis_started = True
                logger.info(f"Async analysis started for deal {deal_id}")
            else:
                # Synchronous (blocks response)
                process_analysis_async(deal_id, vacancy_text, parsed['email'], parsed['voornaam'], parsed['bedrijf'], parsed['functie'])
                analysis_started = True

        logger.info(f"Done: confirmation={confirmation_sent}, deal={deal_id}, analysis={analysis_started}")

        return jsonify({
            "success": True,
            "confirmation_sent": confirmation_sent,
            "analysis_started": analysis_started,
            "lead_score": lead_score.total_score,
            "lead_category": lead_score.category,
            "org_id": lead_result.get('org_id'),
            "person_id": lead_result.get('person_id'),
            "deal_id": deal_id
        }), 200

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
