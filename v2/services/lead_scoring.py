"""
Lead Scoring Service - Calculate and update lead scores.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from ..config import (
    LEAD_SCORE_WEIGHTS,
    LEAD_SCORE_HOT, LEAD_SCORE_WARM, LEAD_SCORE_COLD
)
from ..utils import get_logger

logger = get_logger("lead_scoring")


@dataclass
class LeadScore:
    """Lead score result with breakdown."""
    total_score: int
    category: str  # hot, warm, cold
    breakdown: Dict[str, int]


class LeadScorer:
    """Service for calculating lead scores."""

    def __init__(self, weights: Dict = None):
        self.weights = weights or LEAD_SCORE_WEIGHTS

    def calculate(
        self,
        source: str = "",
        has_phone: bool = False,
        has_company: bool = False,
        has_vacancy_text: bool = False,
        vacancy_length: int = 0,
        email: str = "",
        engagement: Dict[str, bool] = None
    ) -> LeadScore:
        """
        Calculate lead score based on available data.

        Args:
            source: Lead source (typeform_direct, meta_lead_ads, etc.)
            has_phone: Whether phone number was provided
            has_company: Whether company name was provided
            has_vacancy_text: Whether vacancy text was provided
            vacancy_length: Length of vacancy text in characters
            email: Email address (to check domain type)
            engagement: Dict of engagement flags (email_opened, clicked, etc.)

        Returns:
            LeadScore with total, category, and breakdown
        """
        breakdown = {}
        total = 0

        # Source score
        source_score = self.weights['source'].get(source, self.weights['source'].get('organic', 7))
        breakdown['source'] = source_score
        total += source_score

        # Has phone
        if has_phone:
            score = self.weights['has_phone']
            breakdown['has_phone'] = score
            total += score

        # Has company
        if has_company:
            score = self.weights['has_company']
            breakdown['has_company'] = score
            total += score

        # Has vacancy text
        if has_vacancy_text:
            score = self.weights['has_vacancy_text']
            breakdown['has_vacancy_text'] = score
            total += score

            # Vacancy length bonus
            if vacancy_length > 1500:
                length_score = self.weights['vacancy_length']['long']
            elif vacancy_length > 500:
                length_score = self.weights['vacancy_length']['medium']
            else:
                length_score = self.weights['vacancy_length']['short']
            breakdown['vacancy_length'] = length_score
            total += length_score

        # Email domain
        if email:
            personal_domains = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'live.nl', 'ziggo.nl']
            domain = email.split('@')[-1].lower() if '@' in email else ''

            if domain and domain not in personal_domains:
                score = self.weights['email_domain']['corporate']
                breakdown['email_domain'] = score
                total += score

        # Engagement
        if engagement:
            engagement_total = 0
            for action, occurred in engagement.items():
                if occurred and action in self.weights['engagement']:
                    engagement_total += self.weights['engagement'][action]
            if engagement_total:
                breakdown['engagement'] = engagement_total
                total += engagement_total

        # Determine category
        if total >= LEAD_SCORE_HOT:
            category = 'hot'
        elif total >= LEAD_SCORE_WARM:
            category = 'warm'
        else:
            category = 'cold'

        logger.info(f"Lead score calculated: {total} ({category}) - {breakdown}")

        return LeadScore(
            total_score=total,
            category=category,
            breakdown=breakdown
        )

    def score_from_typeform(self, parsed_data: Dict) -> LeadScore:
        """Calculate score from parsed Typeform data."""
        vacancy_text = parsed_data.get('vacature', '')

        return self.calculate(
            source='typeform_prefilled' if parsed_data.get('prefilled') else 'typeform_direct',
            has_phone=bool(parsed_data.get('telefoon')),
            has_company=bool(parsed_data.get('bedrijf') and parsed_data['bedrijf'] != 'Onbekend'),
            has_vacancy_text=bool(vacancy_text),
            vacancy_length=len(vacancy_text) if vacancy_text else 0,
            email=parsed_data.get('email', '')
        )

    def score_from_meta_lead(self, lead_data: Dict) -> LeadScore:
        """Calculate score from Meta Lead Ads data."""
        return self.calculate(
            source='meta_lead_ads',
            has_phone=bool(lead_data.get('telefoon')),
            has_company=bool(lead_data.get('bedrijf')),
            has_vacancy_text=False,  # Meta leads don't have vacancy text initially
            email=lead_data.get('email', '')
        )


# Convenience function
def calculate_lead_score(
    source: str = "",
    has_phone: bool = False,
    has_company: bool = False,
    has_vacancy_text: bool = False,
    vacancy_length: int = 0,
    email: str = ""
) -> LeadScore:
    """Calculate lead score using default scorer."""
    scorer = LeadScorer()
    return scorer.calculate(
        source=source,
        has_phone=has_phone,
        has_company=has_company,
        has_vacancy_text=has_vacancy_text,
        vacancy_length=vacancy_length,
        email=email
    )
