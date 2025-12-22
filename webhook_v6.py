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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Recruitin Brand Colors
RECRUITIN_ORANGE = colors.HexColor("#FF6B35")
RECRUITIN_DARK = colors.HexColor("#1F2937")
RECRUITIN_LIGHT_ORANGE = colors.HexColor("#FFF7ED")
SCORE_GREEN = colors.HexColor("#10B981")
SCORE_BLUE = colors.HexColor("#3B82F6")
SCORE_YELLOW = colors.HexColor("#F59E0B")
SCORE_RED = colors.HexColor("#EF4444")

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


def create_score_bar_drawing(score, width=180, height=12):
    """Create a visual score bar as a ReportLab Drawing."""
    d = Drawing(width, height)

    # Background bar (gray)
    d.add(Rect(0, 0, width, height, fillColor=colors.HexColor("#E5E7EB"), strokeColor=None))

    # Filled bar based on score
    fill_width = (score / 10) * width
    if score >= 8:
        fill_color = colors.HexColor("#10B981")  # Green
    elif score >= 6:
        fill_color = colors.HexColor("#3B82F6")  # Blue
    elif score >= 4:
        fill_color = colors.HexColor("#F59E0B")  # Yellow/Orange
    else:
        fill_color = colors.HexColor("#EF4444")  # Red

    d.add(Rect(0, 0, fill_width, height, fillColor=fill_color, strokeColor=None))

    return d


def create_score_circle_drawing(score):
    """Create a large circular score display like MTEE APK template."""
    d = Drawing(140, 140)

    # Determine color based on score
    if score >= 70:
        main_color = colors.HexColor("#10B981")
        bg_color = colors.HexColor("#ECFDF5")
    elif score >= 50:
        main_color = colors.HexColor("#3B82F6")
        bg_color = colors.HexColor("#EFF6FF")
    elif score >= 30:
        main_color = colors.HexColor("#F59E0B")
        bg_color = colors.HexColor("#FFFBEB")
    else:
        main_color = colors.HexColor("#EF4444")
        bg_color = colors.HexColor("#FEF2F2")

    from reportlab.graphics.shapes import Circle

    # Outer ring
    d.add(Circle(70, 70, 68, fillColor=main_color, strokeColor=None))
    # Inner circle (white)
    d.add(Circle(70, 70, 58, fillColor=colors.white, strokeColor=None))
    # Score number
    d.add(String(70, 60, str(score), fontSize=48, fontName='Helvetica-Bold',
                 fillColor=main_color, textAnchor='middle'))
    # /100 text
    d.add(String(70, 40, '/100', fontSize=12, fontName='Helvetica',
                 fillColor=colors.HexColor("#9CA3AF"), textAnchor='middle'))

    return d


def generate_pdf_analysis_report(contact_name, company_name, vacancy_title, analysis_result, score=None, original_vacancy_text=""):
    """
    BIJLAGE 1: Analyse Rapport (2 pagina's)
    - Pagina 1: Score overzicht + ALLE 12 criteria met individuele scores
    - Pagina 2: TOP QUICK WINS + WAT WE VERBETERD HEBBEN (voor/na)
    """
    from reportlab.platypus import PageBreak

    # Parse analysis sections
    sections = parse_analysis_sections(analysis_result)

    # Create PDF buffer
    buffer = io.BytesIO()

    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.8*cm,
        leftMargin=1.8*cm,
        topMargin=1.2*cm,
        bottomMargin=1.2*cm
    )

    page_width = A4[0] - 3.6*cm  # Usable width

    # Score level determination
    score_value = score if score else 0
    if score_value >= 70:
        score_color = SCORE_GREEN
        score_label = "EXCELLENT"
        score_emoji = "🏆"
    elif score_value >= 50:
        score_color = SCORE_BLUE
        score_label = "GOED"
        score_emoji = "✓"
    elif score_value >= 30:
        score_color = SCORE_YELLOW
        score_label = "MATIG"
        score_emoji = "⚠"
    else:
        score_color = SCORE_RED
        score_label = "KRITIEK"
        score_emoji = "✗"

    story = []

    # ═══════════════════════════════════════════════════════════════
    # PAGINA 1: SCORE OVERZICHT + 12 CRITERIA
    # ═══════════════════════════════════════════════════════════════

    # === COMPACT HEADER ===
    header = Table(
        [[
            Paragraph(
                f"<font color='#FFFFFF' size='16'><b>VACATURE ANALYSE</b></font>",
                ParagraphStyle('Header', leading=18)
            ),
            Paragraph(
                f"<font color='#FFFFFF' size='9'><b>{company_name}</b><br/>{vacancy_title or 'Vacature'}</font>",
                ParagraphStyle('HeaderRight', alignment=TA_RIGHT, leading=12)
            )
        ]],
        colWidths=[page_width*0.6, page_width*0.4]
    )
    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header)
    story.append(Spacer(1, 15))

    # === SCORE HERO (Compact) ===
    score_circle = create_score_circle_drawing(score_value)

    score_hero = Table(
        [[
            score_circle,
            Paragraph(
                f"<font size='24' color='{score_color.hexval()}'><b>{score_label}</b></font><br/>"
                f"<font size='10' color='#6B7280'>Gebaseerd op 12 professionele criteria</font>",
                ParagraphStyle('ScoreLabel', leading=28)
            )
        ]],
        colWidths=[4*cm, page_width - 4*cm]
    )
    score_hero.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (1, 0), (1, 0), 20),
    ]))
    story.append(score_hero)
    story.append(Spacer(1, 18))

    # === ALLE 12 CRITERIA MET SCORES ===
    story.append(Paragraph(
        "<font size='12' color='#1F2937'><b>SCORE PER CRITERIUM</b></font>",
        ParagraphStyle('SectionTitle', spaceAfter=10)
    ))

    # Define all 12 criteria with Dutch labels
    criteria_list = [
        ('openingszin', 'Openingszin', 'Vangt de eerste zin direct de aandacht?'),
        ('bedrijf', 'Bedrijfsprofiel', 'Wat maakt dit bedrijf uniek als werkgever?'),
        ('rolklarheid', 'Rolklarheid', 'Zijn de dagelijkse taken concreet beschreven?'),
        ('vereisten', 'Vereisten Realisme', 'Zijn de eisen realistisch voor het niveau?'),
        ('groei', 'Groei-narratief', 'Zijn doorgroeimogelijkheden beschreven?'),
        ('inclusie', 'Inclusie & Bias', 'Is de tekst genderneutraal en inclusief?'),
        ('cialdini', 'Cialdini Triggers', 'Worden overtuigingsprincipes toegepast?'),
        ('salaris', 'Salarisbenchmark', 'Is salarisindicatie marktconform?'),
        ('cta', 'Call-to-Action', 'Is er een duidelijke sollicitatie-oproep?'),
        ('competitief', 'Competitieve Delta', 'Wat onderscheidt deze vacature?'),
        ('confidence', 'Confidence Score', 'Algehele professionaliteit van de tekst'),
        ('implementatie', 'Implementatie', 'Hoe snel zijn verbeteringen toe te passen?'),
    ]

    # Build criteria table rows
    criteria_rows = []
    for i, (key, label, description) in enumerate(criteria_list, 1):
        score_val = sections['scores'].get(key, 5)

        # Score color
        if score_val >= 8:
            s_color = "#10B981"
        elif score_val >= 6:
            s_color = "#3B82F6"
        elif score_val >= 4:
            s_color = "#F59E0B"
        else:
            s_color = "#EF4444"

        # Visual bar (using unicode blocks)
        filled = int(score_val)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty

        row = [
            Paragraph(f"<font size='8' color='#6B7280'>{i}.</font>", ParagraphStyle('Num')),
            Paragraph(f"<font size='9' color='#1F2937'><b>{label}</b></font>", ParagraphStyle('Label')),
            Paragraph(f"<font size='8' color='{s_color}'>{bar}</font>", ParagraphStyle('Bar', fontName='Helvetica')),
            Paragraph(f"<font size='10' color='{s_color}'><b>{score_val}/10</b></font>", ParagraphStyle('Score', alignment=TA_RIGHT)),
        ]
        criteria_rows.append(row)

    criteria_table = Table(
        criteria_rows,
        colWidths=[0.6*cm, 3.8*cm, 7*cm, 1.5*cm]
    )
    criteria_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor("#E5E7EB")),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F9FAFB")),
    ]))
    story.append(criteria_table)

    # === QUICK SUMMARY BOX ===
    story.append(Spacer(1, 15))

    # Find top 2 strengths and weaknesses
    all_scores = [(k, v) for k, v in sections['scores'].items()]
    sorted_scores = sorted(all_scores, key=lambda x: x[1], reverse=True)

    strengths = [s for s in sorted_scores if s[1] >= 7][:2]
    weaknesses = [s for s in sorted_scores if s[1] <= 5][:2]

    # Label lookup
    label_map = {k: v for k, v, _ in criteria_list}

    summary_text = "<font size='10' color='#1F2937'><b>In één oogopslag:</b></font><br/>"
    if strengths:
        summary_text += "<font size='9' color='#10B981'>✓ Sterk: "
        summary_text += ", ".join([label_map.get(s[0], s[0]) for s in strengths])
        summary_text += "</font><br/>"
    if weaknesses:
        summary_text += "<font size='9' color='#EF4444'>✗ Aandacht nodig: "
        summary_text += ", ".join([label_map.get(s[0], s[0]) for s in weaknesses])
        summary_text += "</font>"

    summary_box = Table(
        [[Paragraph(summary_text, ParagraphStyle('Summary', leading=14))]],
        colWidths=[page_width]
    )
    summary_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F9FF")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#3B82F6")),
    ]))
    story.append(summary_box)

    # ═══════════════════════════════════════════════════════════════
    # PAGINA 2: QUICK WINS + VOOR/NA VERGELIJKING
    # ═══════════════════════════════════════════════════════════════
    story.append(PageBreak())

    # === PAGE 2 HEADER ===
    header2 = Table(
        [[
            Paragraph(
                f"<font color='#FFFFFF' size='14'><b>WAT WE VERBETERD HEBBEN</b></font>",
                ParagraphStyle('Header2', leading=16)
            ),
            Paragraph(
                f"<font color='#9CA3AF' size='9'>Pagina 2/2</font>",
                ParagraphStyle('PageNum', alignment=TA_RIGHT)
            )
        ]],
        colWidths=[page_width*0.8, page_width*0.2]
    )
    header2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header2)
    story.append(Spacer(1, 15))

    # === TOP 3 QUICK WINS ===
    story.append(Paragraph(
        "<font size='12' color='#FF6B35'><b>🚀 TOP 3 QUICK WINS</b></font>",
        ParagraphStyle('QuickWinTitle', spaceAfter=10)
    ))

    if sections['quick_wins']:
        for i, win in enumerate(sections['quick_wins'][:3], 1):
            win_text = win[:180] + "..." if len(win) > 180 else win
            win_row = Table(
                [[
                    Paragraph(f"<font size='12' color='#FF6B35'><b>{i}</b></font>", ParagraphStyle('WinNum', alignment=TA_CENTER)),
                    Paragraph(f"<font size='9' color='#374151'>{win_text}</font>", ParagraphStyle('WinText', leading=13))
                ]],
                colWidths=[0.8*cm, page_width - 0.8*cm]
            )
            win_row.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#FFF7ED")),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#FDBA74")),
            ]))
            story.append(win_row)
            story.append(Spacer(1, 5))

    story.append(Spacer(1, 15))

    # === VOOR / NA VERGELIJKING ===
    story.append(Paragraph(
        "<font size='12' color='#1F2937'><b>📝 VOOR / NA VERGELIJKING</b></font>",
        ParagraphStyle('CompareTitle', spaceAfter=10)
    ))

    # Extract first 150 chars of original for comparison
    original_snippet = original_vacancy_text[:200] + "..." if len(original_vacancy_text) > 200 else original_vacancy_text
    original_snippet = original_snippet.replace('\n', ' ').strip()

    # Extract first part of improved text
    improved_snippet = sections['improved_text'][:200] + "..." if len(sections['improved_text']) > 200 else sections['improved_text']
    improved_snippet = improved_snippet.replace('\n', ' ').replace('**', '').replace('##', '').strip()

    # VOOR box
    voor_box = Table(
        [[
            Paragraph("<font size='9' color='#EF4444'><b>VOOR</b></font>", ParagraphStyle('VoorLabel')),
        ],
        [
            Paragraph(f"<font size='8' color='#6B7280'><i>{original_snippet or 'Originele tekst niet beschikbaar'}</i></font>",
                     ParagraphStyle('VoorText', leading=11))
        ]],
        colWidths=[page_width]
    )
    voor_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FEE2E2")),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#FEF2F2")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#FECACA")),
    ]))
    story.append(voor_box)
    story.append(Spacer(1, 8))

    # NA box
    na_box = Table(
        [[
            Paragraph("<font size='9' color='#10B981'><b>NA</b></font>", ParagraphStyle('NaLabel')),
        ],
        [
            Paragraph(f"<font size='8' color='#374151'>{improved_snippet or 'Verbeterde tekst wordt gegenereerd...'}</font>",
                     ParagraphStyle('NaText', leading=11))
        ]],
        colWidths=[page_width]
    )
    na_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#D1FAE5")),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#ECFDF5")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#A7F3D0")),
    ]))
    story.append(na_box)

    story.append(Spacer(1, 15))

    # === CIALDINI TIPS (if available) ===
    if sections['cialdini_tips']:
        story.append(Paragraph(
            "<font size='10' color='#6B7280'><b>💡 CIALDINI POWER-UPS</b></font>",
            ParagraphStyle('CialdiniTitle', spaceAfter=6)
        ))
        for tip in sections['cialdini_tips'][:3]:
            tip_text = tip[:140] + "..." if len(tip) > 140 else tip
            story.append(Paragraph(
                f"<font size='8' color='#6B7280'>• {tip_text}</font>",
                ParagraphStyle('CialdiniTip', leading=11, leftIndent=8, spaceBefore=2, spaceAfter=2)
            ))

    # === FOOTER ===
    story.append(Spacer(1, 20))
    footer = Table(
        [[
            Paragraph(
                "<font color='#9CA3AF' size='7'><b>Recruitin B.V.</b> | info@recruitin.nl | www.kandidatentekort.nl</font>",
                ParagraphStyle('FooterLeft', alignment=TA_LEFT)
            ),
            Paragraph(
                f"<font color='#9CA3AF' size='7'>{datetime.now().strftime('%d-%m-%Y')} | Vertrouwelijk</font>",
                ParagraphStyle('FooterRight', alignment=TA_RIGHT)
            )
        ]],
        colWidths=[page_width*0.6, page_width*0.4]
    )
    footer.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(footer)

    # Build PDF
    doc.build(story)

    pdf_content = buffer.getvalue()
    buffer.close()

    logger.info(f"PDF Bijlage 1 (Analyse Rapport) generated for {company_name}, size: {len(pdf_content)} bytes")
    return pdf_content


def generate_pdf_vacancy_text(company_name, vacancy_title, analysis_result):
    """
    BIJLAGE 2: Geoptimaliseerde Vacaturetekst (1 pagina)
    - Clean, copy-paste ready versie van de verbeterde vacaturetekst
    """

    # Parse analysis sections
    sections = parse_analysis_sections(analysis_result)

    if not sections['improved_text']:
        return None

    # Create PDF buffer
    buffer = io.BytesIO()

    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    page_width = A4[0] - 4*cm

    story = []

    # === COMPACT HEADER ===
    header = Table(
        [[
            Paragraph(
                f"<font color='#FFFFFF' size='14'><b>GEOPTIMALISEERDE VACATURETEKST</b></font>",
                ParagraphStyle('Header', leading=16)
            ),
            Paragraph(
                f"<font color='#10B981' size='9'><b>✓ READY TO USE</b></font>",
                ParagraphStyle('Badge', alignment=TA_RIGHT)
            )
        ]],
        colWidths=[page_width*0.7, page_width*0.3]
    )
    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header)

    # === SUBTITLE ===
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"<font size='11' color='#1F2937'><b>{company_name}</b> | {vacancy_title or 'Vacature'}</font>",
        ParagraphStyle('Subtitle', alignment=TA_CENTER, spaceAfter=15)
    ))

    # === VACATURETEKST ===
    improved_text = sections['improved_text']

    # Split into paragraphs
    paragraphs = [p.strip() for p in improved_text.split('\n\n') if p.strip()]
    if len(paragraphs) < 2:
        paragraphs = [p.strip() for p in improved_text.split('\n') if p.strip()]

    for para in paragraphs[:20]:  # Max 20 paragraphs
        # Clean up markdown
        para = para.replace('**', '')
        para = para.replace('##', '')
        para = para.strip('# ')

        if not para:
            continue

        # Detect headers (short lines)
        if len(para) < 50 and not para.endswith('.') and not para.endswith(':'):
            story.append(Paragraph(
                f"<font size='11' color='#1F2937'><b>{para}</b></font>",
                ParagraphStyle('SubHead', spaceBefore=12, spaceAfter=4)
            ))
        else:
            story.append(Paragraph(
                f"<font size='10' color='#374151'>{para}</font>",
                ParagraphStyle('BodyText', leading=14, spaceBefore=3, spaceAfter=6, alignment=TA_JUSTIFY)
            ))

    # === TIP FOOTER ===
    story.append(Spacer(1, 20))
    tip = Table(
        [[Paragraph(
            "<font size='8' color='#6B7280'><i>💡 Tip: Kopieer deze tekst direct naar je ATS of vacatureplatform. "
            "Alle verbeteringen zijn al toegepast.</i></font>",
            ParagraphStyle('Tip', alignment=TA_CENTER)
        )]],
        colWidths=[page_width]
    )
    tip.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F9FF")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(tip)

    # === FOOTER ===
    story.append(Spacer(1, 15))
    footer = Table(
        [[Paragraph(
            f"<font color='#9CA3AF' size='7'>Recruitin B.V. | {datetime.now().strftime('%d-%m-%Y')}</font>",
            ParagraphStyle('Footer', alignment=TA_CENTER)
        )]],
        colWidths=[page_width]
    )
    footer.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(footer)

    # Build PDF
    doc.build(story)

    pdf_content = buffer.getvalue()
    buffer.close()

    logger.info(f"PDF Bijlage 2 (Vacaturetekst) generated for {company_name}, size: {len(pdf_content)} bytes")
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
[Volledig herschreven vacaturetekst met alle verbeteringen toegepast]

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
