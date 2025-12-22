#!/usr/bin/env python3
"""
KANDIDATENTEKORT.NL - WEBHOOK V7
Deploy: Render.com

Features:
- Claude AI V7.0 vacature analyse met Cialdini triggers
- Regionale salarisbenchmarks
- Inclusie/bias scanning
- Mooie HTML email rapporten
- Pipedrive met custom fields + notes
- Async processing voor snelle response
"""

import os
import io
import json
import logging
import smtplib
import requests
import threading
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, jsonify

# PDF Generation imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Recruitin Brand Colors - Professional Palette
RECRUITIN_ORANGE = colors.HexColor("#FF6B35")
RECRUITIN_DARK = colors.HexColor("#111827")
RECRUITIN_NAVY = colors.HexColor("#1E3A5F")
RECRUITIN_LIGHT = colors.HexColor("#F8FAFC")
RECRUITIN_LIGHT_ORANGE = colors.HexColor("#FFF7ED")

# Score Colors - Vibrant & Clear
SCORE_GREEN = colors.HexColor("#059669")
SCORE_BLUE = colors.HexColor("#2563EB")
SCORE_YELLOW = colors.HexColor("#D97706")
SCORE_RED = colors.HexColor("#DC2626")

# UI Colors
COLOR_TEXT_PRIMARY = colors.HexColor("#111827")
COLOR_TEXT_SECONDARY = colors.HexColor("#4B5563")
COLOR_TEXT_MUTED = colors.HexColor("#9CA3AF")
COLOR_BORDER = colors.HexColor("#E5E7EB")
COLOR_BG_SUBTLE = colors.HexColor("#F9FAFB")

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


def parse_analysis_sections(analysis_result):
    """Parse the V7.0 analysis into structured sections."""
    sections = {
        'executive_summary': '',
        'scores': {},
        'quick_wins': [],
        'improved_text': '',
        'cialdini_tips': []
    }

    if not analysis_result:
        return sections

    # Extract Executive Summary
    if 'EXECUTIVE SUMMARY' in analysis_result:
        try:
            summary_part = analysis_result.split('EXECUTIVE SUMMARY')[1]
            summary_end = summary_part.find('━━━')
            if summary_end == -1:
                summary_end = summary_part.find('SCORES PER CRITERIUM')
            sections['executive_summary'] = summary_part[:summary_end].strip().strip('━').strip()
        except:
            pass

    # Extract individual scores
    score_names = [
        ('Openingszin', 'openingszin'),
        ('Bedrijf Aantrekkingskracht', 'bedrijf'),
        ('Rolklarheid', 'rolklarheid'),
        ('Vereisten Realisme', 'vereisten'),
        ('Groei-narratief', 'groei'),
        ('Inclusie', 'inclusie'),
        ('Cialdini', 'cialdini'),
        ('Salarisbenchmark', 'salaris'),
        ('CTA', 'cta'),
        ('Competitieve Delta', 'competitief'),
        ('Confidence', 'confidence'),
        ('Implementatie', 'implementatie')
    ]

    for search_term, key in score_names:
        try:
            for line in analysis_result.split('\n'):
                if search_term in line and '/10' in line:
                    score_part = line.split('/10')[0]
                    digits = ''.join(filter(str.isdigit, score_part[-3:]))
                    if digits:
                        sections['scores'][key] = int(digits)
                    break
        except:
            continue

    # Extract Quick Wins
    if 'QUICK WINS' in analysis_result:
        try:
            qw_part = analysis_result.split('QUICK WINS')[1]
            qw_end = qw_part.find('━━━')
            if qw_end == -1:
                qw_end = qw_part.find('VERBETERDE')
            qw_text = qw_part[:qw_end] if qw_end > 0 else qw_part[:500]
            for line in qw_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    clean_line = line.lstrip('0123456789.-•) ').strip()
                    if clean_line and len(clean_line) > 10:
                        sections['quick_wins'].append(clean_line)
                        if len(sections['quick_wins']) >= 3:
                            break
        except:
            pass

    # Extract Improved Text
    if 'VERBETERDE VACATURETEKST' in analysis_result:
        try:
            imp_part = analysis_result.split('VERBETERDE VACATURETEKST')[1]
            # Skip the first separator line (━━━) after header
            lines = imp_part.split('\n')
            content_lines = []
            found_content = False
            for line in lines:
                # Skip separator lines
                if '━━━' in line or line.strip() == '':
                    if found_content:
                        # If we already found content and hit a separator, we're done
                        if '━━━' in line:
                            break
                    continue
                # Skip if this is a new section header
                if 'BONUS' in line or 'CIALDINI' in line or 'POWER-UP' in line:
                    break
                found_content = True
                content_lines.append(line)
            sections['improved_text'] = '\n'.join(content_lines).strip()
        except Exception as e:
            logger.warning(f"Failed to extract improved text: {e}")

    # Extract Cialdini Tips
    if 'CIALDINI' in analysis_result and 'POWER-UP' in analysis_result:
        try:
            ci_part = analysis_result.split('CIALDINI')[1]
            if 'POWER-UP' in ci_part:
                ci_part = ci_part.split('POWER-UP')[1]
            for line in ci_part.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•') or line.startswith('"')):
                    clean_line = line.lstrip('0123456789.-•) ').strip().strip('"')
                    if clean_line and len(clean_line) > 15:
                        sections['cialdini_tips'].append(clean_line)
                        if len(sections['cialdini_tips']) >= 3:
                            break
        except:
            pass

    return sections


# ═══════════════════════════════════════════════════════════════════════════
# PROFESSIONAL PDF GENERATION - CONSULTANCY QUALITY
# ═══════════════════════════════════════════════════════════════════════════

def create_professional_score_badge(score, size=100):
    """Create a professional circular score badge with gradient-like effect."""
    d = Drawing(size, size)
    center = size / 2

    # Determine color scheme based on score
    if score >= 70:
        primary = colors.HexColor("#059669")
        secondary = colors.HexColor("#D1FAE5")
        label = "EXCELLENT"
    elif score >= 50:
        primary = colors.HexColor("#2563EB")
        secondary = colors.HexColor("#DBEAFE")
        label = "GOED"
    elif score >= 30:
        primary = colors.HexColor("#D97706")
        secondary = colors.HexColor("#FEF3C7")
        label = "MATIG"
    else:
        primary = colors.HexColor("#DC2626")
        secondary = colors.HexColor("#FEE2E2")
        label = "KRITIEK"

    # Outer ring (colored)
    d.add(Circle(center, center, size/2 - 2, fillColor=primary, strokeColor=None))
    # Inner circle (white)
    d.add(Circle(center, center, size/2 - 8, fillColor=colors.white, strokeColor=None))
    # Score number
    d.add(String(center, center - 5, str(score), fontSize=32, fontName='Helvetica-Bold',
                 fillColor=primary, textAnchor='middle'))

    return d, primary, label


def create_horizontal_bar(score, width=120, height=8):
    """Create a clean horizontal progress bar."""
    d = Drawing(width + 30, height + 4)

    # Determine color
    if score >= 8:
        fill_color = colors.HexColor("#059669")
    elif score >= 6:
        fill_color = colors.HexColor("#2563EB")
    elif score >= 4:
        fill_color = colors.HexColor("#D97706")
    else:
        fill_color = colors.HexColor("#DC2626")

    # Background bar with rounded look
    d.add(Rect(0, 2, width, height, fillColor=colors.HexColor("#E5E7EB"),
               strokeColor=None, rx=4, ry=4))

    # Filled portion
    fill_width = max(4, (score / 10) * width)
    d.add(Rect(0, 2, fill_width, height, fillColor=fill_color,
               strokeColor=None, rx=4, ry=4))

    return d


def generate_pdf_analysis_report(contact_name, company_name, vacancy_title, analysis_result, score=None, original_vacancy_text=""):
    """
    BIJLAGE 1: Professioneel Analyse Rapport (2 pagina's)
    - Consultancy-niveau design met clean layout
    - Pagina 1: Score overview + 12 criteria breakdown
    - Pagina 2: Quick Wins + Voor/Na vergelijking
    """
    from reportlab.platypus import PageBreak

    sections = parse_analysis_sections(analysis_result)
    buffer = io.BytesIO()

    # A4 document met professionele margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    page_width = A4[0] - 4*cm
    score_value = score if score else 0

    # Score classification
    if score_value >= 70:
        score_color = SCORE_GREEN
        score_label = "EXCELLENT"
        score_desc = "Uw vacature scoort bovengemiddeld"
    elif score_value >= 50:
        score_color = SCORE_BLUE
        score_label = "GOED"
        score_desc = "Solide basis met verbeterpotentieel"
    elif score_value >= 30:
        score_color = SCORE_YELLOW
        score_label = "MATIG"
        score_desc = "Significante verbeteringen mogelijk"
    else:
        score_color = SCORE_RED
        score_label = "KRITIEK"
        score_desc = "Directe aandacht vereist"

    story = []

    # ═══════════════════════════════════════════════════════════════
    # PAGINA 1: PROFESSIONAL HEADER + SCORE + CRITERIA
    # ═══════════════════════════════════════════════════════════════

    # === HEADER BAR ===
    header_data = [[
        Paragraph(
            f"<font color='#FFFFFF' size='18'><b>VACATURE ANALYSE</b></font>",
            ParagraphStyle('H1', fontName='Helvetica-Bold', leading=22)
        ),
        Paragraph(
            f"<font color='#FF6B35' size='9'>kandidatentekort.nl</font>",
            ParagraphStyle('Brand', alignment=TA_RIGHT)
        )
    ]]
    header = Table(header_data, colWidths=[page_width*0.75, page_width*0.25])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('RIGHTPADDING', (0, 0), (-1, -1), 18),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header)

    # === SUB-HEADER INFO ===
    story.append(Spacer(1, 2))
    subheader_data = [[
        Paragraph(
            f"<font color='#4B5563' size='10'>{company_name}</font>",
            ParagraphStyle('Company')
        ),
        Paragraph(
            f"<font color='#6B7280' size='9'>{datetime.now().strftime('%d %B %Y')}</font>",
            ParagraphStyle('Date', alignment=TA_RIGHT)
        )
    ]]
    subheader = Table(subheader_data, colWidths=[page_width*0.6, page_width*0.4])
    subheader.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_SUBTLE),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('RIGHTPADDING', (0, 0), (-1, -1), 18),
        ('LINEBELOW', (0, 0), (-1, -1), 1, COLOR_BORDER),
    ]))
    story.append(subheader)
    story.append(Spacer(1, 20))

    # === SCORE HERO SECTION ===
    score_badge, badge_color, badge_label = create_professional_score_badge(score_value, 90)

    score_hero_data = [[
        score_badge,
        Table([[
            Paragraph(
                f"<font size='28' color='{score_color.hexval()}'><b>{score_value}</b></font>"
                f"<font size='14' color='#9CA3AF'>/100</font>",
                ParagraphStyle('BigScore', leading=35)
            )
        ], [
            Paragraph(
                f"<font size='14' color='{score_color.hexval()}'><b>{score_label}</b></font>",
                ParagraphStyle('ScoreLabel', spaceBefore=2)
            )
        ], [
            Paragraph(
                f"<font size='9' color='#6B7280'>{score_desc}</font>",
                ParagraphStyle('ScoreDesc', spaceBefore=4)
            )
        ]], colWidths=[page_width*0.45])
    ]]

    score_hero = Table(score_hero_data, colWidths=[3.5*cm, page_width - 3.5*cm])
    score_hero.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (1, 0), (1, 0), 20),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    # Wrap in a box
    score_box = Table([[score_hero]], colWidths=[page_width])
    score_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(score_box)
    story.append(Spacer(1, 20))

    # === SECTION: SCORE PER CRITERIUM ===
    section_title = Paragraph(
        "<font size='12' color='#111827'><b>SCORE PER CRITERIUM</b></font>",
        ParagraphStyle('SectionTitle', spaceBefore=5, spaceAfter=12)
    )
    story.append(section_title)

    # 12 criteria in 2 columns
    criteria_list = [
        ('openingszin', 'Openingszin', 'Eerste indruk'),
        ('bedrijf', 'Bedrijfsprofiel', 'Werkgeversimago'),
        ('rolklarheid', 'Rolklarheid', 'Takenbeschrijving'),
        ('vereisten', 'Vereisten', 'Realistische eisen'),
        ('groei', 'Groeiperspectief', 'Ontwikkeling'),
        ('inclusie', 'Inclusiviteit', 'Bias-vrij'),
        ('cialdini', 'Overtuigingskracht', 'Cialdini principes'),
        ('salaris', 'Salarisindicatie', 'Marktconform'),
        ('cta', 'Call-to-Action', 'Sollicitatie-oproep'),
        ('competitief', 'Onderscheidend', 'Competitieve kracht'),
        ('confidence', 'Professionaliteit', 'Algehele kwaliteit'),
        ('implementatie', 'Implementatie', 'Uitvoerbaarheid'),
    ]

    # Build criteria rows - 2 columns layout
    left_criteria = criteria_list[:6]
    right_criteria = criteria_list[6:]

    def make_criteria_cell(key, label, sublabel):
        score_val = sections['scores'].get(key, 5)
        if score_val >= 8:
            s_color = "#059669"
            s_bg = "#ECFDF5"
        elif score_val >= 6:
            s_color = "#2563EB"
            s_bg = "#EFF6FF"
        elif score_val >= 4:
            s_color = "#D97706"
            s_bg = "#FFFBEB"
        else:
            s_color = "#DC2626"
            s_bg = "#FEF2F2"

        bar = create_horizontal_bar(score_val, width=80, height=6)

        cell_content = Table([
            [
                Paragraph(f"<font size='9' color='#111827'><b>{label}</b></font>",
                         ParagraphStyle('CriteriaLabel')),
                Paragraph(f"<font size='11' color='{s_color}'><b>{score_val}</b></font>",
                         ParagraphStyle('CriteriaScore', alignment=TA_RIGHT))
            ],
            [bar, ''],
        ], colWidths=[page_width*0.35, page_width*0.1])

        cell_content.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('SPAN', (0, 1), (1, 1)),
        ]))

        return cell_content

    criteria_rows = []
    for i in range(6):
        left = left_criteria[i]
        right = right_criteria[i]
        row = [
            make_criteria_cell(*left),
            Spacer(10, 1),
            make_criteria_cell(*right)
        ]
        criteria_rows.append(row)

    criteria_table = Table(
        criteria_rows,
        colWidths=[page_width*0.45, page_width*0.1, page_width*0.45]
    )
    criteria_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (0, -2), 0.5, COLOR_BORDER),
        ('LINEBELOW', (2, 0), (2, -2), 0.5, COLOR_BORDER),
    ]))

    # Wrap criteria in box
    criteria_box = Table([[criteria_table]], colWidths=[page_width])
    criteria_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(criteria_box)

    # === INSIGHT BOX ===
    story.append(Spacer(1, 15))

    all_scores = [(k, v) for k, v in sections['scores'].items()]
    sorted_scores = sorted(all_scores, key=lambda x: x[1], reverse=True)
    strengths = [s for s in sorted_scores if s[1] >= 7][:2]
    weaknesses = [s for s in sorted_scores if s[1] <= 4][:2]

    label_map = {k: v for k, v, _ in criteria_list}

    insight_parts = []
    if strengths:
        strength_names = ", ".join([label_map.get(s[0], s[0]) for s in strengths])
        insight_parts.append(f"<font color='#059669'>✓ Sterktes: {strength_names}</font>")
    if weaknesses:
        weak_names = ", ".join([label_map.get(s[0], s[0]) for s in weaknesses])
        insight_parts.append(f"<font color='#DC2626'>⚠ Focus: {weak_names}</font>")

    insight_text = "<font size='10' color='#111827'><b>Kernpunten</b></font><br/><br/>"
    insight_text += "<br/>".join([f"<font size='9'>{p}</font>" for p in insight_parts])

    insight_box = Table([[
        Paragraph(insight_text, ParagraphStyle('Insight', leading=16))
    ]], colWidths=[page_width])
    insight_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F9FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BAE6FD")),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(insight_box)

    # ═══════════════════════════════════════════════════════════════
    # PAGINA 2: QUICK WINS + VOOR/NA
    # ═══════════════════════════════════════════════════════════════
    story.append(PageBreak())

    # === PAGE 2 HEADER ===
    header2_data = [[
        Paragraph(
            "<font color='#FFFFFF' size='16'><b>VERBETERADVIES</b></font>",
            ParagraphStyle('H2', leading=20)
        ),
        Paragraph(
            "<font color='#9CA3AF' size='9'>Pagina 2/2</font>",
            ParagraphStyle('PageNum', alignment=TA_RIGHT)
        )
    ]]
    header2 = Table(header2_data, colWidths=[page_width*0.75, page_width*0.25])
    header2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('RIGHTPADDING', (0, 0), (-1, -1), 18),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header2)
    story.append(Spacer(1, 20))

    # === TOP 3 QUICK WINS ===
    story.append(Paragraph(
        "<font size='12' color='#111827'><b>TOP 3 VERBETERPUNTEN</b></font>",
        ParagraphStyle('WinsTitle', spaceAfter=12)
    ))

    if sections['quick_wins']:
        for i, win in enumerate(sections['quick_wins'][:3], 1):
            win_text = win[:200] + "..." if len(win) > 200 else win

            win_row = Table([[
                Paragraph(
                    f"<font size='16' color='#FF6B35'><b>{i}</b></font>",
                    ParagraphStyle('WinNum', alignment=TA_CENTER)
                ),
                Paragraph(
                    f"<font size='10' color='#374151'>{win_text}</font>",
                    ParagraphStyle('WinText', leading=14)
                )
            ]], colWidths=[1.2*cm, page_width - 1.2*cm])

            win_row.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#FFF7ED")),
                ('BACKGROUND', (1, 0), (1, -1), colors.white),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#FDBA74")),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(win_row)
            story.append(Spacer(1, 8))

    story.append(Spacer(1, 15))

    # === VOOR / NA VERGELIJKING ===
    story.append(Paragraph(
        "<font size='12' color='#111827'><b>VOOR &amp; NA VERGELIJKING</b></font>",
        ParagraphStyle('CompareTitle', spaceAfter=12)
    ))

    # Original text snippet
    original_snippet = original_vacancy_text[:250] + "..." if len(original_vacancy_text) > 250 else original_vacancy_text
    original_snippet = original_snippet.replace('\n', ' ').replace('<', '&lt;').replace('>', '&gt;').strip()

    # Improved text snippet
    improved_snippet = sections['improved_text'][:250] + "..." if len(sections['improved_text']) > 250 else sections['improved_text']
    improved_snippet = improved_snippet.replace('\n', ' ').replace('**', '').replace('##', '').replace('<', '&lt;').replace('>', '&gt;').strip()

    # VOOR section
    voor_content = Table([
        [Paragraph("<font size='9' color='#DC2626'><b>VOOR</b></font> <font size='8' color='#9CA3AF'>Originele tekst</font>",
                   ParagraphStyle('VoorLabel'))],
        [Paragraph(f"<font size='9' color='#6B7280'><i>\"{original_snippet or 'Originele tekst niet beschikbaar'}\"</i></font>",
                   ParagraphStyle('VoorText', leading=13, spaceBefore=6))]
    ], colWidths=[page_width])
    voor_content.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF2F2")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#FECACA")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(voor_content)
    story.append(Spacer(1, 10))

    # Arrow
    story.append(Paragraph(
        "<font size='14' color='#9CA3AF'>↓</font>",
        ParagraphStyle('Arrow', alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 10))

    # NA section
    na_content = Table([
        [Paragraph("<font size='9' color='#059669'><b>NA</b></font> <font size='8' color='#9CA3AF'>Geoptimaliseerde tekst</font>",
                   ParagraphStyle('NaLabel'))],
        [Paragraph(f"<font size='9' color='#374151'>\"{improved_snippet or 'Verbeterde tekst wordt gegenereerd...'}\"</font>",
                   ParagraphStyle('NaText', leading=13, spaceBefore=6))]
    ], colWidths=[page_width])
    na_content.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#A7F3D0")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(na_content)

    # === FOOTER ===
    story.append(Spacer(1, 25))
    footer = Table([[
        Paragraph(
            "<font color='#9CA3AF' size='8'><b>Recruitin B.V.</b> | info@recruitin.nl | kandidatentekort.nl</font>",
            ParagraphStyle('FooterLeft')
        ),
        Paragraph(
            f"<font color='#9CA3AF' size='8'>Rapport gegenereerd: {datetime.now().strftime('%d-%m-%Y %H:%M')}</font>",
            ParagraphStyle('FooterRight', alignment=TA_RIGHT)
        )
    ]], colWidths=[page_width*0.55, page_width*0.45])
    footer.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(footer)

    # Build PDF
    doc.build(story)
    pdf_content = buffer.getvalue()
    buffer.close()

    logger.info(f"Professional PDF Bijlage 1 generated for {company_name}, size: {len(pdf_content)} bytes")
    return pdf_content


# ════════════════════════════════════════════════════════════════════════════
# BIJLAGE 2: GEOPTIMALISEERDE VACATURETEKST
# ════════════════════════════════════════════════════════════════════════════

def generate_pdf_vacancy_text(company_name, vacancy_title, analysis_result):
    """
    BIJLAGE 2: Professionele Geoptimaliseerde Vacaturetekst
    - Executive-level document design
    - Ready-to-use vacaturetekst met professional formatting
    - Clean typography en branded styling
    """

    sections = parse_analysis_sections(analysis_result)

    if not sections['improved_text']:
        return None

    buffer = io.BytesIO()

    # A4 document met ruime margins voor leesbaarheid
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.2*cm,
        leftMargin=2.2*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    page_width = A4[0] - 4.4*cm

    story = []

    # ═══════════════════════════════════════════════════════════════
    # PROFESSIONAL HEADER BAR
    # ═══════════════════════════════════════════════════════════════

    header_data = [[
        Paragraph(
            "<font color='#FFFFFF' size='16'><b>VACATURETEKST</b></font>",
            ParagraphStyle('H1', fontName='Helvetica-Bold', leading=20)
        ),
        Table([[
            Paragraph(
                "<font color='#10B981' size='8'><b>✓ GEOPTIMALISEERD</b></font>",
                ParagraphStyle('Badge', alignment=TA_CENTER)
            )
        ]], colWidths=[2.8*cm])
    ]]

    header = Table(header_data, colWidths=[page_width - 3*cm, 3*cm])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_DARK),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#064E3B")),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (0, 0), 20),
        ('RIGHTPADDING', (1, 0), (1, 0), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header)

    # === SUB-HEADER MET BEDRIJFSINFO ===
    story.append(Spacer(1, 2))

    subheader_data = [[
        Paragraph(
            f"<font color='#374151' size='11'><b>{company_name}</b></font>",
            ParagraphStyle('Company')
        ),
        Paragraph(
            f"<font color='#6B7280' size='9'>{vacancy_title or 'Vacature'}</font>",
            ParagraphStyle('Role', alignment=TA_RIGHT)
        )
    ]]
    subheader = Table(subheader_data, colWidths=[page_width*0.55, page_width*0.45])
    subheader.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_SUBTLE),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 18),
        ('RIGHTPADDING', (0, 0), (-1, -1), 18),
        ('LINEBELOW', (0, 0), (-1, -1), 1, COLOR_BORDER),
    ]))
    story.append(subheader)
    story.append(Spacer(1, 20))

    # ═══════════════════════════════════════════════════════════════
    # DOCUMENT CONTENT - VACATURETEKST
    # ═══════════════════════════════════════════════════════════════

    improved_text = sections['improved_text']

    # Clean en split de tekst in secties
    paragraphs = [p.strip() for p in improved_text.split('\n\n') if p.strip()]
    if len(paragraphs) < 2:
        paragraphs = [p.strip() for p in improved_text.split('\n') if p.strip()]

    # Content container met subtiele border
    content_rows = []

    for para in paragraphs[:25]:  # Max 25 paragraphs
        # Clean markdown
        para = para.replace('**', '').replace('##', '').strip('# ').strip()

        if not para:
            continue

        # Escape HTML entities
        para = para.replace('<', '&lt;').replace('>', '&gt;')

        # Detect section headers (korte regels zonder leestekens aan eind)
        is_header = (
            len(para) < 60 and
            not para.endswith('.') and
            not para.endswith(',') and
            not para.endswith(':') and
            not para.startswith('-') and
            not para.startswith('•')
        )

        if is_header:
            # Section header styling
            content_rows.append([
                Paragraph(
                    f"<font size='11' color='#111827'><b>{para}</b></font>",
                    ParagraphStyle('SectionHead',
                                  spaceBefore=14,
                                  spaceAfter=6,
                                  borderPadding=0)
                )
            ])
        elif para.startswith('-') or para.startswith('•'):
            # Bullet point
            clean_para = para.lstrip('-•').strip()
            content_rows.append([
                Paragraph(
                    f"<font size='10' color='#374151'>• {clean_para}</font>",
                    ParagraphStyle('BulletPoint',
                                  leading=15,
                                  leftIndent=12,
                                  spaceBefore=3,
                                  spaceAfter=3)
                )
            ])
        else:
            # Normal paragraph
            content_rows.append([
                Paragraph(
                    f"<font size='10' color='#374151'>{para}</font>",
                    ParagraphStyle('BodyText',
                                  leading=15,
                                  spaceBefore=4,
                                  spaceAfter=8,
                                  alignment=TA_JUSTIFY)
                )
            ])

    if content_rows:
        content_table = Table(content_rows, colWidths=[page_width - 30])
        content_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))

        # Wrap content in styled box
        content_box = Table([[content_table]], colWidths=[page_width])
        content_box.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 18),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 18),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ]))
        story.append(content_box)

    # ═══════════════════════════════════════════════════════════════
    # PROFESSIONAL TIP BOX
    # ═══════════════════════════════════════════════════════════════
    story.append(Spacer(1, 18))

    tip_content = Table([[
        Paragraph(
            "<font size='10' color='#0369A1'><b>Klaar voor gebruik</b></font>",
            ParagraphStyle('TipTitle')
        )
    ], [
        Paragraph(
            "<font size='9' color='#0C4A6E'>Deze vacaturetekst is geoptimaliseerd op basis van 12 professionele criteria. "
            "Kopieer de tekst direct naar je ATS, LinkedIn of vacatureplatform.</font>",
            ParagraphStyle('TipText', leading=13, spaceBefore=4)
        )
    ]], colWidths=[page_width])

    tip_content.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E0F2FE")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#7DD3FC")),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(tip_content)

    # ═══════════════════════════════════════════════════════════════
    # PROFESSIONAL FOOTER
    # ═══════════════════════════════════════════════════════════════
    story.append(Spacer(1, 20))

    footer = Table([[
        Paragraph(
            "<font color='#9CA3AF' size='8'><b>Recruitin B.V.</b> | kandidatentekort.nl</font>",
            ParagraphStyle('FooterLeft')
        ),
        Paragraph(
            f"<font color='#9CA3AF' size='8'>{datetime.now().strftime('%d %B %Y')}</font>",
            ParagraphStyle('FooterRight', alignment=TA_RIGHT)
        )
    ]], colWidths=[page_width*0.5, page_width*0.5])

    footer.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(footer)

    # Build PDF
    doc.build(story)
    pdf_content = buffer.getvalue()
    buffer.close()

    logger.info(f"Professional PDF Bijlage 2 generated for {company_name}, size: {len(pdf_content)} bytes")
    return pdf_content


# Keep old function name as alias for backwards compatibility
def generate_pdf_report(contact_name, company_name, vacancy_title, analysis_result, score=None):
    """Backwards compatible wrapper - calls new analysis report function."""
    return generate_pdf_analysis_report(contact_name, company_name, vacancy_title, analysis_result, score, "")


def generate_score_bar_html(label, score, emoji="📊"):
    """Generate HTML for a visual score bar."""
    if score is None:
        score = 5

    # Color based on score
    if score >= 8:
        color = "#10B981"  # Green
    elif score >= 6:
        color = "#3B82F6"  # Blue
    elif score >= 4:
        color = "#F59E0B"  # Orange
    else:
        color = "#EF4444"  # Red

    width_pct = score * 10

    return f'''
    <tr>
        <td style="padding: 8px 0;">
            <div style="display: flex; align-items: center; margin-bottom: 4px;">
                <span style="font-size: 12px; color: #6B7280; width: 140px;">{emoji} {label}</span>
                <span style="font-size: 14px; font-weight: 600; color: {color}; margin-left: auto;">{score}/10</span>
            </div>
            <div style="background: #E5E7EB; border-radius: 4px; height: 8px; overflow: hidden;">
                <div style="background: {color}; height: 100%; width: {width_pct}%; border-radius: 4px;"></div>
            </div>
        </td>
    </tr>'''


def generate_email_html(contact_name, company_name, vacancy_title, analysis_result, score=None):
    """Generate SHORT & PUNCHY HTML email with score teaser - details in PDF attachments."""

    # Parse the analysis into sections
    sections = parse_analysis_sections(analysis_result)

    # Score color based on value
    if score:
        if score >= 70:
            score_color = "#10B981"
            score_label = "Uitstekend"
            score_emoji = "🏆"
            score_msg = "Indrukwekkend! Je vacature scoort bovengemiddeld."
        elif score >= 50:
            score_color = "#3B82F6"
            score_label = "Goed"
            score_emoji = "👍"
            score_msg = "Solide basis met duidelijke verbeterkansen."
        elif score >= 30:
            score_color = "#F59E0B"
            score_label = "Verbetering nodig"
            score_emoji = "⚠️"
            score_msg = "Met enkele aanpassingen haal je veel meer uit je vacature."
        else:
            score_color = "#EF4444"
            score_label = "Kritiek"
            score_emoji = "🔴"
            score_msg = "Je vacature mist essentiële elementen. Tijd voor actie!"
    else:
        score_color = "#6B7280"
        score_label = "Analyse"
        score_emoji = "📊"
        score_msg = "Je vacaturetekst is geanalyseerd."
        score = "?"

    # Find top strength and weaknesses from scores
    scores_dict = sections['scores']
    if scores_dict:
        sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
        top_strength = sorted_scores[0] if sorted_scores else None
        weaknesses = [s for s in sorted_scores if s[1] <= 5][:2]
    else:
        top_strength = None
        weaknesses = []

    # Map score keys to readable labels
    score_labels = {
        'openingszin': 'Openingszin',
        'bedrijf': 'Bedrijfsprofiel',
        'rolklarheid': 'Rolklarheid',
        'vereisten': 'Vereisten',
        'groei': 'Groeiperspectief',
        'inclusie': 'Inclusiviteit',
        'cialdini': 'Overtuigingskracht',
        'salaris': 'Salaris',
        'cta': 'Call-to-Action',
        'competitief': 'Onderscheidend vermogen',
        'confidence': 'Professionaliteit',
        'implementatie': 'Implementatie'
    }

    # Build highlights HTML
    highlights_html = ""
    if top_strength:
        label = score_labels.get(top_strength[0], top_strength[0])
        highlights_html += f'''
        <div style="display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #E5E7EB;">
            <span style="color: #10B981; font-size: 18px; margin-right: 12px;">✓</span>
            <span style="color: #374151;"><strong>Sterk:</strong> {label} ({top_strength[1]}/10)</span>
        </div>'''

    for weakness in weaknesses:
        label = score_labels.get(weakness[0], weakness[0])
        highlights_html += f'''
        <div style="display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #E5E7EB;">
            <span style="color: #EF4444; font-size: 18px; margin-right: 12px;">✗</span>
            <span style="color: #374151;"><strong>Verbeterpunt:</strong> {label} ({weakness[1]}/10)</span>
        </div>'''

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #F3F4F6;">

    <!-- Compact Header -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, #FF6B35 0%, #FF8F5C 100%); padding: 25px 20px;">
        <tr>
            <td align="center">
                <h1 style="color: white; margin: 0; font-size: 22px; font-weight: 700;">
                    🎯 Je Vacature Analyse is klaar!
                </h1>
                <p style="color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 14px;">
                    {company_name} • {vacancy_title or 'Vacature'}
                </p>
            </td>
        </tr>
    </table>

    <!-- Main Content -->
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
        <tr>
            <td style="padding: 20px;">

                <!-- Score Hero - Compact -->
                <div style="background: white; border-radius: 16px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); text-align: center;">
                    <div style="display: inline-block; width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, {score_color}22 0%, {score_color}11 100%); border: 4px solid {score_color}; line-height: 100px;">
                        <span style="font-size: 36px; font-weight: 800; color: {score_color};">{score}</span>
                    </div>
                    <p style="color: {score_color}; font-size: 16px; font-weight: 700; margin: 12px 0 4px 0;">
                        {score_emoji} {score_label}
                    </p>
                    <p style="color: #6B7280; font-size: 13px; margin: 0;">
                        {score_msg}
                    </p>
                </div>

                <!-- Quick Highlights -->
                <div style="background: white; border-radius: 16px; padding: 20px 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="color: #1F2937; margin: 0 0 10px 0; font-size: 16px;">
                        In één oogopslag
                    </h2>
                    {highlights_html}
                </div>

                <!-- Attachments Notice -->
                <div style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-radius: 16px; padding: 25px; margin-bottom: 20px; border: 1px solid #93C5FD; text-align: center;">
                    <span style="font-size: 32px;">📎</span>
                    <h3 style="color: #1E40AF; margin: 10px 0 8px 0; font-size: 16px;">
                        Open de bijlagen voor details
                    </h3>
                    <p style="color: #3B82F6; font-size: 13px; margin: 0 0 5px 0;">
                        <strong>Bijlage 1:</strong> Volledig Analyse Rapport (12 criteria + verbeteringen)
                    </p>
                    <p style="color: #3B82F6; font-size: 13px; margin: 0;">
                        <strong>Bijlage 2:</strong> Je geoptimaliseerde vacaturetekst (copy-paste ready)
                    </p>
                </div>

                <!-- CTA Button -->
                <div style="text-align: center; margin: 25px 0;">
                    <a href="https://recruitin.nl/contact"
                       style="display: inline-block; background: linear-gradient(135deg, #FF6B35 0%, #FF8F5C 100%); color: white; text-decoration: none;
                              padding: 14px 28px; border-radius: 10px; font-weight: 600; font-size: 14px;
                              box-shadow: 0 4px 14px rgba(255,107,53,0.35);">
                        📞 Hulp nodig? Plan een gratis gesprek
                    </a>
                </div>

            </td>
        </tr>
    </table>

    <!-- Compact Footer -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background: #1F2937; padding: 20px;">
        <tr>
            <td align="center">
                <p style="color: #9CA3AF; font-size: 12px; margin: 0;">
                    Recruitin B.V. | Kandidatentekort.nl<br>
                    <a href="mailto:info@recruitin.nl" style="color: #FF6B35;">info@recruitin.nl</a>
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


def send_analysis_email(to_email, contact_name, company_name, vacancy_title, analysis_result, score=None, original_vacancy_text=""):
    """Send the analysis report email with TWO PDF attachments:
    - Bijlage 1: Analyse Rapport (12 criteria + voor/na vergelijking)
    - Bijlage 2: Geoptimaliseerde Vacaturetekst (copy-paste ready)
    """
    if not GMAIL_APP_PASSWORD:
        logger.error("GMAIL_APP_PASSWORD not set")
        return False

    try:
        # Use 'mixed' for attachments instead of 'alternative'
        msg = MIMEMultipart('mixed')
        msg['Subject'] = f"🎯 Vacature Analyse Rapport - {company_name}"
        msg['From'] = f"Recruitin <{GMAIL_USER}>"
        msg['To'] = to_email

        # Create alternative part for HTML email
        msg_alternative = MIMEMultipart('alternative')

        # Generate HTML email (short & punchy - details in PDFs)
        html = generate_email_html(contact_name, company_name, vacancy_title, analysis_result, score)
        msg_alternative.attach(MIMEText(html, 'html'))
        msg.attach(msg_alternative)

        # Create safe filename base
        safe_company = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_company = safe_company.replace(' ', '_')[:30]
        date_str = datetime.now().strftime('%Y%m%d')

        # ═══════════════════════════════════════════════════════════════
        # BIJLAGE 1: Analyse Rapport (2 pagina's, 12 criteria + voor/na)
        # ═══════════════════════════════════════════════════════════════
        try:
            pdf_analysis = generate_pdf_analysis_report(
                contact_name, company_name, vacancy_title,
                analysis_result, score, original_vacancy_text
            )

            pdf_filename_1 = f"Bijlage1_Analyse_Rapport_{safe_company}_{date_str}.pdf"

            pdf_attachment_1 = MIMEBase('application', 'pdf')
            pdf_attachment_1.set_payload(pdf_analysis)
            encoders.encode_base64(pdf_attachment_1)
            pdf_attachment_1.add_header(
                'Content-Disposition',
                f'attachment; filename="{pdf_filename_1}"'
            )
            msg.attach(pdf_attachment_1)
            logger.info(f"PDF Bijlage 1 (Analyse Rapport) added: {pdf_filename_1}")

        except Exception as pdf_error:
            logger.error(f"PDF Bijlage 1 generation failed: {pdf_error}")

        # ═══════════════════════════════════════════════════════════════
        # BIJLAGE 2: Geoptimaliseerde Vacaturetekst (copy-paste ready)
        # ═══════════════════════════════════════════════════════════════
        try:
            pdf_vacancy = generate_pdf_vacancy_text(company_name, vacancy_title, analysis_result)

            pdf_filename_2 = f"Bijlage2_Vacaturetekst_{safe_company}_{date_str}.pdf"

            pdf_attachment_2 = MIMEBase('application', 'pdf')
            pdf_attachment_2.set_payload(pdf_vacancy)
            encoders.encode_base64(pdf_attachment_2)
            pdf_attachment_2.add_header(
                'Content-Disposition',
                f'attachment; filename="{pdf_filename_2}"'
            )
            msg.attach(pdf_attachment_2)
            logger.info(f"PDF Bijlage 2 (Vacaturetekst) added: {pdf_filename_2}")

        except Exception as pdf_error:
            logger.error(f"PDF Bijlage 2 generation failed: {pdf_error}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Analysis email with 2 PDFs sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Analysis email failed: {e}")
        return False


def analyze_vacancy_with_claude(vacancy_text, company_name, vacancy_title=""):
    """Analyze vacancy using Claude API with V7.0 Master Prompt - 12 criteria analysis."""
    if not CLAUDE_API_KEY:
        logger.warning("CLAUDE_API_KEY not set, using placeholder")
        return None, None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        # V7.0 MASTER PROMPT - Comprehensive 12-criteria vacancy analysis
        prompt = f"""Je bent een expert recruitment consultant gespecialiseerd in vacaturetekst optimalisatie.
Analyseer de volgende vacaturetekst grondig op basis van 12 criteria en geef concrete, actionable feedback.

═══════════════════════════════════════════════════════════════
📋 VACATURE INFORMATIE
═══════════════════════════════════════════════════════════════
🏢 Bedrijf: {company_name}
💼 Functie: {vacancy_title or 'Niet opgegeven'}

📝 VACATURETEKST:
{vacancy_text}

═══════════════════════════════════════════════════════════════
🎯 V7.0 ANALYSE FRAMEWORK - 12 CRITERIA
═══════════════════════════════════════════════════════════════

Analyseer de vacature op de volgende 12 criteria. Geef per criterium een score (1-10) en concrete feedback.

【SESSIE 1: OPENINGSZIN AUDIT】
- Vangt de eerste zin direct de aandacht?
- Is er een 'hook' die nieuwsgierigheid wekt?
- Vermijdt het clichés zoals "Wij zijn op zoek naar..."?
Score: /10 | Feedback + verbeterde openingszin

【SESSIE 2: BEDRIJF AANTREKKINGSKRACHT】
- Wat maakt dit bedrijf uniek als werkgever?
- Zijn de cultuur en waarden duidelijk?
- Is er een compelling employer brand verhaal?
Score: /10 | Feedback + concrete suggesties

【SESSIE 3: ROLKLARHEID】
- Zijn de dagelijkse taken concreet beschreven?
- Weet de kandidaat precies wat de rol inhoudt?
- Is de impact van de rol duidelijk?
Score: /10 | Feedback + verbeterpunten

【SESSIE 4: VEREISTEN REALISME】
- Zijn de eisen realistisch voor het salarisniveau?
- Is er onderscheid tussen must-haves en nice-to-haves?
- Worden er geen 'purple squirrel' kandidaten gevraagd?
Score: /10 | Feedback + realistische aanpassingen

【SESSIE 5: GROEI-NARRATIEF】
- Zijn doorgroeimogelijkheden beschreven?
- Welke ontwikkelkansen biedt de rol?
- Is er een carrièreperspectief geschetst?
Score: /10 | Feedback + groei-elementen toevoegen

【SESSIE 6: INCLUSIE & BIAS CHECK】
- Is de tekst genderneutraal?
- Zijn er onbewuste barrières voor bepaalde groepen?
- Nodigt de tekst een diverse groep kandidaten uit?
Score: /10 | Feedback + inclusieve alternatieven

【SESSIE 7: CIALDINI TRIGGERS】
- Social Proof: Worden team/bedrijf successen genoemd?
- Scarcity: Is er urgentie zonder te pushy te zijn?
- Authority: Wordt expertise/marktpositie benadrukt?
- Reciprocity: Wat biedt het bedrijf eerst?
- Liking: Is de toon sympathiek en benaderbaar?
- Commitment: Zijn er kleine eerste stappen?
Score: /10 | Feedback + 3 toe te voegen triggers

【SESSIE 8: REGIONALE SALARISBENCHMARK】
- Is salarisindicatie genoemd (of gemist)?
- Komt het overeen met marktstandaarden?
- Zijn secundaire arbeidsvoorwaarden aantrekkelijk?
Score: /10 | Feedback + benchmark advies

【SESSIE 9: CTA (CALL-TO-ACTION) TRIGGERS】
- Is er een duidelijke sollicitatie-oproep?
- Is het proces laagdrempelig beschreven?
- Worden contactgegevens vermeld?
Score: /10 | Feedback + krachtige CTA suggestie

【SESSIE 10: COMPETITIEVE DELTA】
- Wat onderscheidt deze vacature van concurrenten?
- Zijn unique selling points duidelijk?
- Waarom zou je HIER solliciteren vs. concurrent?
Score: /10 | Feedback + differentiatie punten

【SESSIE 11: CONFIDENCE SCORING】
- Algehele professionaliteit van de tekst
- Grammatica en spelling
- Structuur en leesbaarheid
Score: /10 | Totaal vertrouwen in tekst

【SESSIE 12: IMPLEMENTATIE ROADMAP】
- Top 3 quick wins (direct implementeerbaar)
- Top 3 strategische verbeteringen (langere termijn)
- Prioritering op basis van impact

═══════════════════════════════════════════════════════════════
📊 OUTPUT FORMAT (STRIKT AANHOUDEN)
═══════════════════════════════════════════════════════════════

Begin je analyse ALTIJD met:

SCORE: [TOTAAL]/100

Bereken totaal: som van alle 12 criteria scores × 0.833 (afgerond)

Geef daarna:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2-3 zinnen kernboodschap met belangrijkste bevinding]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 SCORES PER CRITERIUM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Openingszin: /10
2. Bedrijf Aantrekkingskracht: /10
3. Rolklarheid: /10
4. Vereisten Realisme: /10
5. Groei-narratief: /10
6. Inclusie & Bias: /10
7. Cialdini Triggers: /10
8. Salarisbenchmark: /10
9. CTA Triggers: /10
10. Competitieve Delta: /10
11. Confidence Score: /10
12. Implementatie Klaar: /10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 TOP 3 QUICK WINS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Direct implementeerbaar verbeterpunt]
2. [Direct implementeerbaar verbeterpunt]
3. [Direct implementeerbaar verbeterpunt]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ VERBETERDE VACATURETEKST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BELANGRIJK: Schrijf een VOLLEDIG NIEUWE, PROFESSIONELE vacaturetekst die:
- Minimaal 400-600 woorden bevat
- Een pakkende, emotionele openingszin heeft die nieuwsgierigheid wekt
- Concrete taken en verantwoordelijkheden beschrijft (geen vage bullet points)
- Duidelijke groei- en ontwikkelmogelijkheden noemt
- Een aantrekkelijk werkgeversprofiel schetst met bedrijfscultuur
- Salarisindicatie of "marktconform + uitstekende secundaire voorwaarden" bevat
- Cialdini overtuigingsprincipes toepast (social proof, scarcity, authority)
- Een krachtige call-to-action heeft
- Professioneel en wervend is geschreven - GEEN droge opsomming
- Direct copy-paste klaar is voor publicatie

Structuur de vacaturetekst als volgt:
1. Pakkende kop/titel
2. Wervende intro (2-3 zinnen die de rol en impact beschrijven)
3. "Dit ga je doen" - concrete taken
4. "Dit breng je mee" - realistische eisen (must-haves vs nice-to-haves)
5. "Dit krijg je van ons" - arbeidsvoorwaarden en benefits
6. "Over [bedrijfsnaam]" - employer branding
7. Call-to-action met sollicitatieinstructie

[Schrijf hier de complete, wervende vacaturetekst - minimaal 400 woorden]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 BONUS: CIALDINI POWER-UPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[3 specifieke zinnen die overtuigingsprincipes toepassen]

Wees concreet, actionable, en vermijd vage feedback. Elke suggestie moet direct implementeerbaar zijn."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,  # Increased for comprehensive analysis
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

        logger.info(f"V7.0 Analysis completed for {company_name}, score: {score}")
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
            # Send analysis email with BOTH PDFs (pass original vacancy_text for voor/na comparison)
            send_analysis_email(
                email, contact_name, company_name, vacancy_title,
                analysis_result, score, original_vacancy_text=vacancy_text
            )

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
        "version": "7.2",
        "features": {
            "email": bool(GMAIL_APP_PASSWORD),
            "pipedrive": bool(PIPEDRIVE_API_TOKEN),
            "claude": bool(CLAUDE_API_KEY),
            "v7_analysis": True
        },
        "analysis_criteria": 12,
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
        "service": "Kandidatentekort Webhook V7",
        "version": "7.2",
        "features": [
            "email",
            "pipedrive",
            "claude-ai-v7",
            "async-processing",
            "12-criteria-analysis",
            "cialdini-triggers",
            "inclusie-bias-check",
            "salary-benchmark"
        ],
        "endpoints": ["/health", "/webhook/typeform", "/api/analyze"]
    })


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
