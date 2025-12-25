"""
Manual Processing Handlers - PDF URLs, email sending, etc.
For cases where automated flow needs human intervention.
"""

from datetime import datetime, timedelta
from flask import request, jsonify

from ..config import PIPEDRIVE_BASE_URL, PIPEDRIVE_API_TOKEN
from ..services import PipedriveService, EmailService
from ..templates import get_pdf_delivery_email
from ..utils import get_logger

logger = get_logger("manual_handler")


def update_pdf_urls():
    """
    Update Pipedrive deal with PDF URLs and create reminder task.

    POST JSON:
    {
        "deal_id": 12345,
        "vacature_pdf_url": "https://...",
        "rapport_pdf_url": "https://..."
    }
    """
    try:
        data = request.get_json(force=True, silent=True) or {}

        deal_id = data.get('deal_id')
        vacature_url = data.get('vacature_pdf_url', '')
        rapport_url = data.get('rapport_pdf_url', '')

        if not deal_id:
            return jsonify({"error": "deal_id is required"}), 400

        if not vacature_url and not rapport_url:
            return jsonify({"error": "At least one PDF URL is required"}), 400

        pipedrive = PipedriveService()

        # Add note with PDF URLs
        note_content = f"""✅ PDF DOCUMENTEN GEREED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Verbeterde Vacaturetekst:
{vacature_url if vacature_url else '(niet beschikbaar)'}

📊 Analyse Rapport:
{rapport_url if rapport_url else '(niet beschikbaar)'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Actie: Review en verstuur naar klant
   Endpoint: POST /send-pdf-email met deal_id={deal_id}
"""

        pipedrive.add_note(deal_id, note_content, pinned=True)

        # Create reminder task for tomorrow
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        pipedrive.create_activity(
            deal_id=deal_id,
            subject=f"📧 Verstuur PDF rapport naar klant",
            due_date=tomorrow,
            note=f"PDFs staan klaar. Verstuur via /send-pdf-email of handmatig."
        )

        logger.info(f"PDF URLs added to deal {deal_id}, reminder created for {tomorrow}")

        return jsonify({
            "success": True,
            "deal_id": deal_id,
            "note_added": True,
            "reminder_date": tomorrow,
            "next_step": f"POST /send-pdf-email with deal_id={deal_id}"
        }), 200

    except Exception as e:
        logger.error(f"Update PDF URLs error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def send_pdf_email():
    """
    Send PDF delivery email to customer.

    POST JSON:
    {
        "deal_id": 12345,
        "vacature_pdf_url": "https://...",  # Optional if already in notes
        "rapport_pdf_url": "https://...",   # Optional if already in notes
        "recipient_email": "...",           # Optional, fetched from deal
        "recipient_name": "...",            # Optional
        "functie_titel": "...",             # Optional
        "bedrijf": "..."                    # Optional
    }
    """
    try:
        data = request.get_json(force=True, silent=True) or {}

        deal_id = data.get('deal_id')
        if not deal_id:
            return jsonify({"error": "deal_id is required"}), 400

        pipedrive = PipedriveService()

        # Get deal details
        deal = pipedrive.get_deal(deal_id)
        if not deal:
            return jsonify({"error": f"Deal {deal_id} not found"}), 404

        # Extract info from deal or use provided values
        recipient_email = data.get('recipient_email')
        recipient_name = data.get('recipient_name', 'daar')
        functie_titel = data.get('functie_titel', 'je vacature')
        bedrijf = data.get('bedrijf', 'je bedrijf')

        # Try to get email from deal's person
        if not recipient_email:
            person_id = deal.get('person_id', {}).get('value') if isinstance(deal.get('person_id'), dict) else deal.get('person_id')
            if person_id:
                # Note: Would need to fetch person details here
                pass

        if not recipient_email:
            return jsonify({"error": "recipient_email is required (not found in deal)"}), 400

        # Get PDF URLs from request or need to be provided
        vacature_url = data.get('vacature_pdf_url', '')
        rapport_url = data.get('rapport_pdf_url', '')

        if not vacature_url and not rapport_url:
            return jsonify({"error": "At least one PDF URL is required"}), 400

        # Send email
        email_service = EmailService()
        html = get_pdf_delivery_email(
            voornaam=recipient_name,
            functie_titel=functie_titel,
            bedrijf=bedrijf,
            vacature_pdf_url=vacature_url,
            rapport_pdf_url=rapport_url
        )

        result = email_service.send(
            to_email=recipient_email,
            subject=f"📄 Je vacature-analyse voor {bedrijf} staat klaar!",
            html_body=html
        )

        if result.success:
            # Add note to deal
            pipedrive.add_note(
                deal_id,
                f"✅ PDF email verzonden naar {recipient_email}\nDatum: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
            )

            # Trigger nurture sequence
            pipedrive.trigger_nurture(deal_id)

            logger.info(f"PDF email sent to {recipient_email} for deal {deal_id}")

            return jsonify({
                "success": True,
                "email_sent": True,
                "recipient": recipient_email,
                "deal_id": deal_id,
                "nurture_triggered": True
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result.error
            }), 500

    except Exception as e:
        logger.error(f"Send PDF email error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def test_email():
    """Test email sending."""
    to = request.args.get('to', 'artsrecruitin@gmail.com')
    template = request.args.get('template', 'confirmation')

    email_service = EmailService()

    if template == 'confirmation':
        from ..templates import get_confirmation_email
        html = get_confirmation_email("Test", "Test Bedrijf", "Test Functie")
        subject = "Test: Bevestiging"
    elif template == 'analysis':
        from ..templates import get_analysis_report_email
        html = get_analysis_report_email(
            "Test", "Test Bedrijf", 7.5,
            "Openingszin: 7/10 | Bedrijf: 8/10",
            ["Verbetering 1", "Verbetering 2", "Verbetering 3"],
            "Dit is de verbeterde vacaturetekst...",
            ["Bonus tip 1", "Bonus tip 2"]
        )
        subject = "Test: Analyse Rapport"
    elif template == 'meta':
        from ..templates import get_meta_welcome_email
        html = get_meta_welcome_email("Test", "Test Bedrijf")
        subject = "Test: Meta Welcome"
    else:
        return jsonify({"error": f"Unknown template: {template}"}), 400

    result = email_service.send(to, subject, html)

    return jsonify({
        "success": result.success,
        "to": to,
        "template": template,
        "error": result.error
    }), 200 if result.success else 500
