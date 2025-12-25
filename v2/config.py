"""
KANDIDATENTEKORT V2 - Configuration
All environment variables and constants in one place.
"""

import os

# =============================================================================
# API KEYS & CREDENTIALS
# =============================================================================

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY') or os.getenv('CLAUDE_API_KEY')
PIPEDRIVE_API_TOKEN = os.getenv('PIPEDRIVE_API_TOKEN')
TYPEFORM_API_TOKEN = os.getenv('TYPEFORM_API_TOKEN')
GMAIL_USER = os.getenv('GMAIL_USER', 'artsrecruitin@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD') or os.getenv('GMAIL_PASS')

# PDFMonkey
PDFMONKEY_API_KEY = os.getenv('PDFMONKEY_API_KEY', '')
PDFMONKEY_TEMPLATE_ANALYSE = os.getenv('PDFMONKEY_TEMPLATE_ANALYSE', '')
PDFMONKEY_TEMPLATE_VACATURE = os.getenv('PDFMONKEY_TEMPLATE_VACATURE', '')

# Meta/Facebook
META_VERIFY_TOKEN = os.getenv('META_VERIFY_TOKEN', 'kandidatentekort_verify_2024')
FB_ACCESS_TOKEN = os.getenv('FB_ACCESS_TOKEN', '')
FB_PIXEL_ID = os.getenv('FB_PIXEL_ID', '238226887541404')

# =============================================================================
# PIPEDRIVE SETTINGS
# =============================================================================

PIPEDRIVE_BASE_URL = "https://api.pipedrive.com/v1"
PIPELINE_ID = 4           # Kandidatentekort pipeline
STAGE_ID = 21             # Gekwalificeerd stage
OWNER_ID = 23957248       # Wouter

# Custom field IDs for nurture tracking
FIELD_RAPPORT_VERZONDEN = "337f9ccca15334e6e4f937ca5ef0055f13ed0c63"
FIELD_EMAIL_SEQUENCE_STATUS = "22d33c7f119119e178f391a272739c571cf2e29b"
FIELD_LAATSTE_EMAIL = "753f37a1abc8e161c7982c1379a306b21fae1bab"
FIELD_LEAD_SCORE = os.getenv('PD_FIELD_LEAD_SCORE', '')

# Custom field IDs for analysis
CUSTOM_FIELD_SCORE = os.getenv('PD_FIELD_SCORE', '')
CUSTOM_FIELD_ANALYSIS_DATE = os.getenv('PD_FIELD_ANALYSIS_DATE', '')

# =============================================================================
# TYPEFORM SETTINGS
# =============================================================================

TYPEFORM_ID = "kalFRTCA"
TYPEFORM_FULL_ID = "01KD5GQP5AVY7E5X0NK9HJN5QN"

# =============================================================================
# EMAIL NURTURE SCHEDULE
# =============================================================================

# Days after rapport verzonden -> email number and template
EMAIL_SCHEDULE = {
    1: {"day": 1, "template_id": 55, "name": "Check-in"},
    2: {"day": 3, "template_id": 56, "name": "Is het gelukt"},
    3: {"day": 5, "template_id": 57, "name": "Resultaten"},
    4: {"day": 8, "template_id": 58, "name": "Tip Functietitel"},
    5: {"day": 11, "template_id": 59, "name": "Tip Salaris"},
    6: {"day": 14, "template_id": 60, "name": "Tip Opening"},
    7: {"day": 21, "template_id": 61, "name": "Gesprek Aanbod"},
    8: {"day": 30, "template_id": 62, "name": "Final Check-in"},
}

# Only send nurture to deals in this stage
NURTURE_ACTIVE_STAGE = 21  # Gekwalificeerd

# =============================================================================
# LEAD SCORING WEIGHTS
# =============================================================================

LEAD_SCORE_WEIGHTS = {
    'source': {
        'typeform_direct': 10,
        'typeform_prefilled': 12,  # Came from quick analyzer
        'meta_lead_ads': 5,
        'linkedin_lead_ads': 8,
        'organic': 7,
        'referral': 15,
    },
    'has_phone': 5,
    'has_company': 5,
    'has_vacancy_text': 10,
    'vacancy_length': {  # chars
        'short': 2,      # < 500
        'medium': 5,     # 500-1500
        'long': 8,       # > 1500
    },
    'email_domain': {
        'corporate': 5,   # Not gmail/hotmail/etc
        'personal': 0,
    },
    'engagement': {
        'email_opened': 2,
        'email_clicked': 5,
        'calendly_clicked': 10,
        'whatsapp_clicked': 8,
    }
}

# Lead score thresholds
LEAD_SCORE_HOT = 25      # Priority follow-up
LEAD_SCORE_WARM = 15     # Standard nurture
LEAD_SCORE_COLD = 0      # Low priority

# =============================================================================
# URLS
# =============================================================================

CALENDLY_URL = "https://calendly.com/wouter-arts-/vacature-analyse-advies"
WHATSAPP_URL = "https://wa.me/31614314593"
WEBSITE_URL = "https://kandidatentekort.nl"

# =============================================================================
# FEATURE FLAGS
# =============================================================================

USE_PDFMONKEY = bool(PDFMONKEY_API_KEY and PDFMONKEY_TEMPLATE_ANALYSE)
ENABLE_AUTO_ANALYSIS = True  # V2: Re-enabled!
ENABLE_LEAD_SCORING = True
ENABLE_ASYNC_PROCESSING = True

# =============================================================================
# CLAUDE AI SETTINGS
# =============================================================================

CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 4000
CLAUDE_TIMEOUT = 60  # seconds

# =============================================================================
# BRAND COLORS (for PDF generation)
# =============================================================================

BRAND_COLORS = {
    'orange': "#FF6B35",
    'dark': "#111827",
    'navy': "#1E3A5F",
    'light': "#F8FAFC",
    'light_orange': "#FFF7ED",
    'green': "#059669",
    'blue': "#2563EB",
    'yellow': "#D97706",
    'red': "#DC2626",
}

# =============================================================================
# VALIDATION
# =============================================================================

def validate_config():
    """Check if critical config is set."""
    issues = []

    if not ANTHROPIC_API_KEY:
        issues.append("ANTHROPIC_API_KEY not set - Claude analysis will fail")
    if not PIPEDRIVE_API_TOKEN:
        issues.append("PIPEDRIVE_API_TOKEN not set - CRM integration disabled")
    if not GMAIL_APP_PASSWORD:
        issues.append("GMAIL_APP_PASSWORD not set - Email sending disabled")

    return issues

def get_config_status():
    """Return config status for health check."""
    return {
        "claude": bool(ANTHROPIC_API_KEY),
        "pipedrive": bool(PIPEDRIVE_API_TOKEN),
        "email": bool(GMAIL_APP_PASSWORD),
        "typeform": bool(TYPEFORM_API_TOKEN),
        "pdfmonkey": USE_PDFMONKEY,
        "auto_analysis": ENABLE_AUTO_ANALYSIS,
        "lead_scoring": ENABLE_LEAD_SCORING,
    }
