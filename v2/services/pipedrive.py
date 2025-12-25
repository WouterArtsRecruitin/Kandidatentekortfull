"""
Pipedrive CRM Service - Organizations, Persons, Deals, Notes.
"""

import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass
from ..config import (
    PIPEDRIVE_API_TOKEN, PIPEDRIVE_BASE_URL,
    PIPELINE_ID, STAGE_ID, OWNER_ID,
    FIELD_RAPPORT_VERZONDEN, FIELD_EMAIL_SEQUENCE_STATUS, FIELD_LAATSTE_EMAIL,
    CUSTOM_FIELD_SCORE, CUSTOM_FIELD_ANALYSIS_DATE
)
from ..utils import get_logger, retry_with_backoff

logger = get_logger("pipedrive")


@dataclass
class PipedriveResult:
    """Result of a Pipedrive operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class PipedriveService:
    """Service for Pipedrive CRM operations."""

    def __init__(self, api_token: str = None):
        self.api_token = api_token or PIPEDRIVE_API_TOKEN
        self.base_url = PIPEDRIVE_BASE_URL

    def _get_url(self, endpoint: str) -> str:
        """Build API URL with token."""
        return f"{self.base_url}/{endpoint}?api_token={self.api_token}"

    @retry_with_backoff(max_attempts=3, initial_delay=1.0, exceptions=(requests.RequestException,))
    def _request(self, method: str, endpoint: str, data: Dict = None) -> PipedriveResult:
        """Make API request to Pipedrive."""
        if not self.api_token:
            return PipedriveResult(success=False, error="API token not configured")

        url = self._get_url(endpoint)

        try:
            if method == "POST":
                response = requests.post(url, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=30)
            elif method == "GET":
                response = requests.get(url, timeout=30)
            else:
                return PipedriveResult(success=False, error=f"Unknown method: {method}")

            result = response.json()

            if result.get('success'):
                return PipedriveResult(success=True, data=result.get('data'))
            else:
                error = result.get('error', 'Unknown error')
                logger.error(f"Pipedrive error: {error}")
                return PipedriveResult(success=False, error=error)

        except requests.RequestException as e:
            logger.error(f"Pipedrive request failed: {e}")
            raise  # Let retry handle it

    # =========================================================================
    # ORGANIZATIONS
    # =========================================================================

    def create_organization(self, name: str) -> Optional[int]:
        """Create organization, return ID or None."""
        if not name or name == 'Onbekend':
            return None

        result = self._request("POST", "organizations", {
            "name": name,
            "owner_id": OWNER_ID
        })

        if result.success:
            org_id = result.data.get('id')
            logger.info(f"Created organization: {name} (ID: {org_id})")
            return org_id

        return None

    # =========================================================================
    # PERSONS
    # =========================================================================

    def create_person(
        self,
        name: str,
        email: str,
        phone: str = "",
        org_id: int = None
    ) -> Optional[int]:
        """Create person, return ID or None."""
        data = {
            "name": name or "Onbekend",
            "owner_id": OWNER_ID
        }

        if email:
            data["email"] = [{"value": email, "primary": True}]
        if phone:
            data["phone"] = [{"value": phone, "primary": True}]
        if org_id:
            data["org_id"] = org_id

        result = self._request("POST", "persons", data)

        if result.success:
            person_id = result.data.get('id')
            logger.info(f"Created person: {name} (ID: {person_id})")
            return person_id

        return None

    # =========================================================================
    # DEALS
    # =========================================================================

    def create_deal(
        self,
        title: str,
        person_id: int = None,
        org_id: int = None,
        pipeline_id: int = PIPELINE_ID,
        stage_id: int = STAGE_ID
    ) -> Optional[int]:
        """Create deal, return ID or None."""
        data = {
            "title": title,
            "pipeline_id": pipeline_id,
            "stage_id": stage_id,
            "user_id": OWNER_ID,
            "status": "open"
        }

        if person_id:
            data["person_id"] = person_id
        if org_id:
            data["org_id"] = org_id

        result = self._request("POST", "deals", data)

        if result.success:
            deal_id = result.data.get('id')
            logger.info(f"Created deal: {title} (ID: {deal_id})")
            return deal_id

        return None

    def update_deal(self, deal_id: int, data: Dict) -> bool:
        """Update deal fields."""
        result = self._request("PUT", f"deals/{deal_id}", data)
        if result.success:
            logger.info(f"Updated deal {deal_id}")
        return result.success

    def update_deal_custom_fields(
        self,
        deal_id: int,
        score: float = None,
        analysis_date: str = None,
        rapport_verzonden: str = None,
        email_sequence_status: str = None,
        laatste_email: str = None
    ) -> bool:
        """Update custom fields on deal."""
        data = {}

        if score is not None and CUSTOM_FIELD_SCORE:
            data[CUSTOM_FIELD_SCORE] = score
        if analysis_date and CUSTOM_FIELD_ANALYSIS_DATE:
            data[CUSTOM_FIELD_ANALYSIS_DATE] = analysis_date
        if rapport_verzonden:
            data[FIELD_RAPPORT_VERZONDEN] = rapport_verzonden
        if email_sequence_status:
            data[FIELD_EMAIL_SEQUENCE_STATUS] = email_sequence_status
        if laatste_email:
            data[FIELD_LAATSTE_EMAIL] = laatste_email

        if not data:
            return True

        return self.update_deal(deal_id, data)

    def get_deal(self, deal_id: int) -> Optional[Dict]:
        """Get deal by ID."""
        result = self._request("GET", f"deals/{deal_id}")
        return result.data if result.success else None

    def get_deals_in_stage(self, stage_id: int = STAGE_ID, limit: int = 100) -> List[Dict]:
        """Get all deals in a specific stage."""
        # Note: This is a simplified version - production should handle pagination
        result = self._request("GET", f"deals?stage_id={stage_id}&limit={limit}")
        if result.success and result.data:
            return result.data
        return []

    # =========================================================================
    # NOTES
    # =========================================================================

    def add_note(self, deal_id: int, content: str, pinned: bool = False) -> bool:
        """Add note to deal."""
        result = self._request("POST", "notes", {
            "deal_id": deal_id,
            "content": content,
            "pinned_to_deal_flag": 1 if pinned else 0
        })

        if result.success:
            logger.info(f"Added note to deal {deal_id}")
        return result.success

    # =========================================================================
    # ACTIVITIES (Tasks)
    # =========================================================================

    def create_activity(
        self,
        deal_id: int,
        subject: str,
        due_date: str,
        activity_type: str = "task",
        note: str = ""
    ) -> Optional[int]:
        """Create activity/task for deal."""
        data = {
            "deal_id": deal_id,
            "subject": subject,
            "due_date": due_date,
            "type": activity_type,
            "user_id": OWNER_ID
        }
        if note:
            data["note"] = note

        result = self._request("POST", "activities", data)

        if result.success:
            activity_id = result.data.get('id')
            logger.info(f"Created activity for deal {deal_id}: {subject}")
            return activity_id

        return None

    # =========================================================================
    # HIGH-LEVEL HELPERS
    # =========================================================================

    def create_full_lead(
        self,
        company_name: str,
        contact_name: str,
        email: str,
        phone: str = "",
        vacancy_title: str = "",
        vacancy_text: str = "",
        source: str = "typeform"
    ) -> Dict[str, Optional[int]]:
        """
        Create complete lead: Organization + Person + Deal + Notes.

        Returns dict with org_id, person_id, deal_id
        """
        # 1. Create organization
        org_id = self.create_organization(company_name)

        # 2. Create person
        person_id = self.create_person(contact_name, email, phone, org_id)

        # 3. Create deal
        deal_title = f"Vacature Analyse - {company_name}"
        if vacancy_title:
            deal_title = f"Vacature Analyse - {vacancy_title} - {company_name}"

        deal_id = self.create_deal(deal_title, person_id, org_id)

        # 4. Add vacancy note
        if deal_id and vacancy_text:
            note_content = f"""📋 VACATURE ONTVANGEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bron: {source}
Functie: {vacancy_title or 'Niet opgegeven'}
Bedrijf: {company_name}
Contact: {contact_name}
Email: {email}
Telefoon: {phone or 'Niet opgegeven'}
Ontvangen: {datetime.now().strftime('%d-%m-%Y %H:%M')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 VACATURETEKST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{vacancy_text[:3000]}
"""
            self.add_note(deal_id, note_content, pinned=True)

        return {
            "org_id": org_id,
            "person_id": person_id,
            "deal_id": deal_id
        }

    def add_analysis_to_deal(
        self,
        deal_id: int,
        analysis_result,
        rapport_url: str = "",
        vacature_url: str = ""
    ) -> bool:
        """Add analysis results to deal as note + update custom fields."""
        if not deal_id:
            return False

        # Build note content
        note_content = f"""🎯 VACATURE ANALYSE RAPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Geanalyseerd: {datetime.now().strftime('%d-%m-%Y %H:%M')}
Score: {analysis_result.score}/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SCORES:
{analysis_result.score_section}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TOP 3 VERBETERPUNTEN:
"""
        for i, improvement in enumerate(analysis_result.top_3_improvements, 1):
            note_content += f"{i}. {improvement}\n"

        if rapport_url or vacature_url:
            note_content += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 PDF DOCUMENTEN:
Rapport: {rapport_url or 'Niet beschikbaar'}
Vacature: {vacature_url or 'Niet beschikbaar'}
"""

        # Add note
        self.add_note(deal_id, note_content, pinned=True)

        # Update custom fields
        self.update_deal_custom_fields(
            deal_id,
            score=analysis_result.score,
            analysis_date=datetime.now().strftime('%Y-%m-%d')
        )

        logger.info(f"Analysis added to deal {deal_id}")
        return True

    def trigger_nurture(self, deal_id: int) -> bool:
        """Mark deal as ready for nurture sequence."""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.update_deal_custom_fields(
            deal_id,
            rapport_verzonden=today,
            email_sequence_status="1"  # Starting sequence
        )
