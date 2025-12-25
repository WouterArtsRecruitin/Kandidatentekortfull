"""
Nurture Email Scheduler - Determines which email to send based on timing.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from ..config import EMAIL_SCHEDULE, FIELD_RAPPORT_VERZONDEN, FIELD_EMAIL_SEQUENCE_STATUS
from ..utils import get_logger

logger = get_logger("nurture_scheduler")


def get_next_email_for_deal(deal: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Determine which nurture email should be sent for a deal.

    Args:
        deal: Pipedrive deal data with custom fields

    Returns:
        Dict with email_num, template_id, name, or None if no email due
    """
    # Get rapport verzonden date
    rapport_date_str = deal.get(FIELD_RAPPORT_VERZONDEN)
    if not rapport_date_str:
        logger.debug(f"Deal {deal.get('id')}: No rapport_verzonden date")
        return None

    # Parse date
    try:
        rapport_date = datetime.strptime(rapport_date_str, '%Y-%m-%d')
    except ValueError:
        logger.error(f"Invalid rapport date format: {rapport_date_str}")
        return None

    # Get current email status
    current_status = deal.get(FIELD_EMAIL_SEQUENCE_STATUS, '0')
    try:
        current_email = int(current_status) if current_status else 0
    except ValueError:
        current_email = 0

    # Check if sequence is complete
    if current_email >= 8:
        logger.debug(f"Deal {deal.get('id')}: Sequence complete")
        return None

    # Calculate days since rapport sent
    days_elapsed = (datetime.now() - rapport_date).days

    # Find next email to send
    next_email_num = current_email + 1
    if next_email_num not in EMAIL_SCHEDULE:
        return None

    next_email = EMAIL_SCHEDULE[next_email_num]
    scheduled_day = next_email['day']

    # Check if it's time
    if days_elapsed >= scheduled_day:
        logger.info(f"Deal {deal.get('id')}: Email {next_email_num} due (day {days_elapsed} >= {scheduled_day})")
        return {
            'email_num': next_email_num,
            'template_id': next_email['template_id'],
            'name': next_email['name'],
            'days_elapsed': days_elapsed,
            'scheduled_day': scheduled_day
        }

    logger.debug(f"Deal {deal.get('id')}: Not time yet (day {days_elapsed} < {scheduled_day})")
    return None


def get_sequence_status(deal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get full nurture sequence status for a deal.

    Returns dict with:
    - current_email: Last sent email number (0-8)
    - next_email: Next email to send (or None)
    - days_since_rapport: Days since rapport was sent
    - sequence_complete: Boolean
    """
    rapport_date_str = deal.get(FIELD_RAPPORT_VERZONDEN)
    current_status = deal.get(FIELD_EMAIL_SEQUENCE_STATUS, '0')

    try:
        current_email = int(current_status) if current_status else 0
    except ValueError:
        current_email = 0

    result = {
        'current_email': current_email,
        'next_email': None,
        'days_since_rapport': None,
        'sequence_complete': current_email >= 8
    }

    if rapport_date_str:
        try:
            rapport_date = datetime.strptime(rapport_date_str, '%Y-%m-%d')
            result['days_since_rapport'] = (datetime.now() - rapport_date).days
        except ValueError:
            pass

    if not result['sequence_complete']:
        result['next_email'] = get_next_email_for_deal(deal)

    return result
