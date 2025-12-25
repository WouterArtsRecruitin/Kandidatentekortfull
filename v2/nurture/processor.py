"""
Nurture Email Processor - Sends scheduled nurture emails.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from flask import jsonify

from ..config import (
    NURTURE_ACTIVE_STAGE,
    FIELD_EMAIL_SEQUENCE_STATUS,
    FIELD_LAATSTE_EMAIL
)
from ..services import PipedriveService, EmailService
from ..utils import get_logger
from .scheduler import get_next_email_for_deal
from .templates import get_nurture_email_html, get_nurture_email_subject

logger = get_logger("nurture_processor")


class NurtureProcessor:
    """Processes and sends nurture emails."""

    def __init__(self):
        self.pipedrive = PipedriveService()
        self.email_service = EmailService()

    def get_eligible_deals(self) -> List[Dict]:
        """Get all deals eligible for nurture emails."""
        deals = self.pipedrive.get_deals_in_stage(NURTURE_ACTIVE_STAGE)
        logger.info(f"Found {len(deals)} deals in stage {NURTURE_ACTIVE_STAGE}")
        return deals

    def process_deal(self, deal: Dict) -> Dict[str, Any]:
        """
        Process a single deal for nurture email.

        Returns dict with status and details.
        """
        deal_id = deal.get('id')

        # Check if email is due
        next_email = get_next_email_for_deal(deal)
        if not next_email:
            return {
                'deal_id': deal_id,
                'status': 'skipped',
                'reason': 'No email due'
            }

        email_num = next_email['email_num']

        # Get recipient info from deal
        person = deal.get('person_id', {})
        if isinstance(person, dict):
            email_address = None
            person_name = person.get('name', 'daar')

            # Get email from person's emails
            emails = person.get('email', [])
            if emails and isinstance(emails, list) and len(emails) > 0:
                email_address = emails[0].get('value') if isinstance(emails[0], dict) else emails[0]
        else:
            return {
                'deal_id': deal_id,
                'status': 'error',
                'reason': 'No person linked to deal'
            }

        if not email_address:
            return {
                'deal_id': deal_id,
                'status': 'error',
                'reason': 'No email address found'
            }

        # Get job title from deal title
        deal_title = deal.get('title', '')
        functie_titel = deal_title.split(' - ')[1] if ' - ' in deal_title else 'je vacature'

        # Get email content
        voornaam = person_name.split()[0] if person_name else 'daar'
        subject = get_nurture_email_subject(email_num)
        html = get_nurture_email_html(email_num, voornaam, functie_titel)

        if not html:
            return {
                'deal_id': deal_id,
                'status': 'error',
                'reason': f'No template for email {email_num}'
            }

        # Send email
        result = self.email_service.send(email_address, subject, html)

        if result.success:
            # Update deal
            self.pipedrive.update_deal_custom_fields(
                deal_id,
                email_sequence_status=str(email_num),
                laatste_email=datetime.now().strftime('%Y-%m-%d')
            )

            # Add note
            self.pipedrive.add_note(
                deal_id,
                f"📧 Nurture Email {email_num} verzonden: {next_email['name']}"
            )

            logger.info(f"Sent nurture email {email_num} to {email_address} for deal {deal_id}")

            return {
                'deal_id': deal_id,
                'status': 'sent',
                'email_num': email_num,
                'email_name': next_email['name'],
                'recipient': email_address
            }
        else:
            logger.error(f"Failed to send email {email_num} for deal {deal_id}: {result.error}")
            return {
                'deal_id': deal_id,
                'status': 'error',
                'reason': result.error
            }

    def process_all(self) -> Dict[str, Any]:
        """
        Process all eligible deals for nurture emails.

        Returns summary of results.
        """
        deals = self.get_eligible_deals()

        results = {
            'processed': 0,
            'sent': 0,
            'skipped': 0,
            'errors': 0,
            'details': []
        }

        for deal in deals:
            result = self.process_deal(deal)
            results['processed'] += 1
            results['details'].append(result)

            if result['status'] == 'sent':
                results['sent'] += 1
            elif result['status'] == 'skipped':
                results['skipped'] += 1
            else:
                results['errors'] += 1

        logger.info(f"Nurture processing complete: {results['sent']} sent, {results['skipped']} skipped, {results['errors']} errors")

        return results


def process_pending_nurtures():
    """Flask endpoint handler for processing nurture emails."""
    try:
        processor = NurtureProcessor()
        results = processor.process_all()

        return jsonify({
            "success": True,
            **results
        }), 200

    except Exception as e:
        logger.error(f"Nurture processing error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
