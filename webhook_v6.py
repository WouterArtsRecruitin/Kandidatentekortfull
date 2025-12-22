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
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
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


def generate_pdf_report(contact_name, company_name, vacancy_title, analysis_result, score=None):
    """Generate a professional PDF report with Recruitin branding."""

    # Parse analysis sections
    sections = parse_analysis_sections(analysis_result)

    # Create PDF buffer
    buffer = io.BytesIO()

    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=RECRUITIN_DARK,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=20,
        alignment=TA_CENTER
    )

    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=RECRUITIN_ORANGE,
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=RECRUITIN_DARK,
        leading=14,
        alignment=TA_JUSTIFY
    )

    small_style = ParagraphStyle(
        'SmallText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor("#6B7280"),
        leading=12
    )

    # Story elements
    story = []

    # === HEADER ===
    # Orange header bar
    header_table = Table(
        [[Paragraph("🎯 VACATURE ANALYSE RAPPORT", ParagraphStyle(
            'HeaderTitle',
            fontSize=20,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))]],
        colWidths=[17*cm]
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_ORANGE),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))

    # Company and date info
    story.append(Paragraph(f"<b>{company_name}</b> • {vacancy_title or 'Vacature'}", subtitle_style))
    story.append(Paragraph(f"Analyse datum: {datetime.now().strftime('%d %B %Y')}", small_style))
    story.append(Spacer(1, 20))

    # === SCORE CARD ===
    score_value = score if score else 0
    if score_value >= 70:
        score_color = SCORE_GREEN
        score_label = "Uitstekend"
    elif score_value >= 50:
        score_color = SCORE_BLUE
        score_label = "Goed"
    elif score_value >= 30:
        score_color = SCORE_YELLOW
        score_label = "Verbetering Nodig"
    else:
        score_color = SCORE_RED
        score_label = "Kritiek"

    score_box = Table(
        [[
            Paragraph(f"<font size='36'><b>{score_value}</b></font><font size='14'>/100</font>",
                     ParagraphStyle('ScoreNumber', alignment=TA_CENTER, textColor=score_color, fontName='Helvetica-Bold')),
            Paragraph(f"<b>{score_label}</b>",
                     ParagraphStyle('ScoreLabel', fontSize=14, alignment=TA_CENTER, textColor=score_color))
        ]],
        colWidths=[8.5*cm, 8.5*cm]
    )
    score_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_LIGHT_ORANGE),
        ('BOX', (0, 0), (-1, -1), 2, RECRUITIN_ORANGE),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(score_box)
    story.append(Spacer(1, 20))

    # === EXECUTIVE SUMMARY ===
    if sections['executive_summary']:
        story.append(Paragraph("📋 EXECUTIVE SUMMARY", header_style))
        story.append(Paragraph(sections['executive_summary'][:500], body_style))
        story.append(Spacer(1, 15))

    # === SCORES PER CRITERIUM ===
    story.append(Paragraph("📊 SCORES PER CRITERIUM", header_style))

    score_mapping = [
        ('Openingszin', 'openingszin'),
        ('Bedrijf Aantrekkingskracht', 'bedrijf'),
        ('Rolklarheid', 'rolklarheid'),
        ('Vereisten Realisme', 'vereisten'),
        ('Groei-narratief', 'groei'),
        ('Inclusie & Bias', 'inclusie'),
        ('Cialdini Triggers', 'cialdini'),
        ('Salarisbenchmark', 'salaris'),
        ('CTA Triggers', 'cta'),
        ('Competitieve Delta', 'competitief'),
        ('Confidence Score', 'confidence'),
        ('Implementatie', 'implementatie')
    ]

    score_data = []
    for label, key in score_mapping:
        s = sections['scores'].get(key, 5)
        # Create visual bar representation
        bar = "█" * s + "░" * (10 - s)
        if s >= 8:
            bar_color = "#10B981"
        elif s >= 6:
            bar_color = "#3B82F6"
        elif s >= 4:
            bar_color = "#F59E0B"
        else:
            bar_color = "#EF4444"
        score_data.append([
            label,
            Paragraph(f"<font color='{bar_color}'>{bar}</font>", small_style),
            f"{s}/10"
        ])

    score_table = Table(score_data, colWidths=[6*cm, 8*cm, 2*cm])
    score_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), RECRUITIN_DARK),
        ('TEXTCOLOR', (2, 0), (2, -1), RECRUITIN_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor("#E5E7EB")),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 20))

    # === QUICK WINS ===
    if sections['quick_wins']:
        story.append(Paragraph("🚀 TOP 3 QUICK WINS", header_style))
        for i, win in enumerate(sections['quick_wins'][:3], 1):
            win_text = win[:200] + "..." if len(win) > 200 else win
            quick_win_table = Table(
                [[Paragraph(f"<b>#{i}</b>", ParagraphStyle('QWNum', fontSize=11, textColor=SCORE_GREEN)),
                  Paragraph(win_text, body_style)]],
                colWidths=[1*cm, 16*cm]
            )
            quick_win_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(quick_win_table)
            story.append(Spacer(1, 5))
        story.append(Spacer(1, 15))

    # === VERBETERDE VACATURETEKST ===
    if sections['improved_text']:
        story.append(Paragraph("✍️ VERBETERDE VACATURETEKST", header_style))

        # Split improved text into paragraphs and add
        improved_text = sections['improved_text'][:3000]  # Limit for PDF
        improved_paragraphs = improved_text.split('\n\n')

        improved_box = Table(
            [[Paragraph(improved_text.replace('\n', '<br/>'),
                       ParagraphStyle('ImprovedText', fontSize=10, textColor=RECRUITIN_DARK, leading=14))]],
            colWidths=[17*cm]
        )
        improved_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E5E7EB")),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(improved_box)
        story.append(Spacer(1, 20))

    # === CIALDINI TIPS ===
    if sections['cialdini_tips']:
        story.append(Paragraph("🧠 CIALDINI OVERTUIGINGSTIPS", header_style))
        for tip in sections['cialdini_tips'][:3]:
            tip_text = tip[:150] + "..." if len(tip) > 150 else tip
            tip_table = Table(
                [[Paragraph(f"💡 <i>\"{tip_text}\"</i>",
                           ParagraphStyle('TipText', fontSize=10, textColor=colors.HexColor("#78350F")))]],
                colWidths=[17*cm]
            )
            tip_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF3C7")),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(tip_table)
            story.append(Spacer(1, 5))
        story.append(Spacer(1, 15))

    # === FOOTER ===
    story.append(Spacer(1, 30))
    footer_table = Table(
        [[
            Paragraph("<b>Recruitin B.V.</b> • Kandidatentekort.nl",
                     ParagraphStyle('Footer', fontSize=10, textColor=colors.white, alignment=TA_CENTER)),
        ],
        [
            Paragraph("info@recruitin.nl • www.recruitin.nl",
                     ParagraphStyle('FooterSmall', fontSize=9, textColor=colors.HexColor("#9CA3AF"), alignment=TA_CENTER)),
        ]],
        colWidths=[17*cm]
    )
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), RECRUITIN_DARK),
        ('TOPPADDING', (0, 0), (-1, 0), 15),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(footer_table)

    # Build PDF
    doc.build(story)

    # Get PDF content
    pdf_content = buffer.getvalue()
    buffer.close()

    logger.info(f"PDF generated for {company_name}, size: {len(pdf_content)} bytes")
    return pdf_content


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
    """Generate beautiful HTML email with visual analysis results."""

    # Parse the analysis into sections
    sections = parse_analysis_sections(analysis_result)

    # Score color based on value
    if score:
        if score >= 70:
            score_color = "#10B981"
            score_label = "Uitstekend"
            score_emoji = "🏆"
        elif score >= 50:
            score_color = "#3B82F6"
            score_label = "Goed"
            score_emoji = "👍"
        elif score >= 30:
            score_color = "#F59E0B"
            score_label = "Verbetering nodig"
            score_emoji = "⚠️"
        else:
            score_color = "#EF4444"
            score_label = "Kritiek"
            score_emoji = "🔴"
    else:
        score_color = "#6B7280"
        score_label = "Analyse"
        score_emoji = "📊"
        score = "?"

    # Build score bars HTML
    score_bars = ""
    score_mapping = [
        ('Openingszin', 'openingszin', '✍️'),
        ('Bedrijf', 'bedrijf', '🏢'),
        ('Rolklarheid', 'rolklarheid', '🎯'),
        ('Vereisten', 'vereisten', '📋'),
        ('Groei', 'groei', '📈'),
        ('Inclusie', 'inclusie', '🌍'),
        ('Cialdini', 'cialdini', '🧠'),
        ('Salaris', 'salaris', '💰'),
        ('CTA', 'cta', '🚀'),
        ('Competitief', 'competitief', '⚡'),
        ('Vertrouwen', 'confidence', '✅'),
        ('Implementatie', 'implementatie', '🔧')
    ]

    for label, key, emoji in score_mapping:
        s = sections['scores'].get(key, 5)
        score_bars += generate_score_bar_html(label, s, emoji)

    # Build quick wins HTML
    quick_wins_html = ""
    for i, win in enumerate(sections['quick_wins'][:3], 1):
        quick_wins_html += f'''
        <div style="background: #ECFDF5; border-radius: 8px; padding: 12px 15px; margin-bottom: 10px; border-left: 4px solid #10B981;">
            <span style="color: #059669; font-weight: 600;">Quick Win {i}:</span>
            <span style="color: #065F46;"> {win[:150]}{'...' if len(win) > 150 else ''}</span>
        </div>'''

    if not quick_wins_html:
        quick_wins_html = '<p style="color: #6B7280;">Zie de volledige analyse hieronder voor verbeterpunten.</p>'

    # Build Cialdini tips HTML
    cialdini_html = ""
    for tip in sections['cialdini_tips'][:3]:
        cialdini_html += f'''
        <div style="background: #FEF3C7; border-radius: 8px; padding: 12px 15px; margin-bottom: 10px; border-left: 4px solid #F59E0B;">
            <span style="color: #92400E;">💡 </span>
            <span style="color: #78350F; font-style: italic;">"{tip[:120]}{'...' if len(tip) > 120 else ''}"</span>
        </div>'''

    # Executive summary
    exec_summary = sections['executive_summary'][:300] if sections['executive_summary'] else "Je vacaturetekst is geanalyseerd op 12 criteria. Bekijk hieronder de scores en concrete verbeterpunten."

    # Improved text (truncated for email)
    improved_text = sections['improved_text'][:1500] if sections['improved_text'] else ""
    if improved_text:
        improved_text_html = f'''
        <div style="background: white; border-radius: 16px; padding: 25px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <h2 style="color: #1F2937; margin: 0 0 15px 0; font-size: 18px;">
                ✍️ Verbeterde Vacaturetekst
            </h2>
            <div style="background: #F9FAFB; border-radius: 8px; padding: 20px; border: 1px solid #E5E7EB;">
                <p style="color: #374151; line-height: 1.7; margin: 0; font-size: 14px; white-space: pre-wrap;">{improved_text}{'...' if len(sections['improved_text']) > 1500 else ''}</p>
            </div>
            <p style="color: #9CA3AF; font-size: 12px; margin: 15px 0 0 0; text-align: center;">
                📋 Volledige tekst beschikbaar in je Pipedrive notities
            </p>
        </div>'''
    else:
        improved_text_html = ""

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #F3F4F6;">

    <!-- Header with Logo -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, #FF6B35 0%, #FF8F5C 100%); padding: 30px 20px;">
        <tr>
            <td align="center">
                <div style="background: white; width: 60px; height: 60px; border-radius: 12px; display: inline-block; text-align: center; line-height: 60px; font-size: 28px; margin-bottom: 15px;">
                    🎯
                </div>
                <h1 style="color: white; margin: 0; font-size: 24px; font-weight: 700;">
                    Vacature Analyse Rapport
                </h1>
                <p style="color: rgba(255,255,255,0.9); margin: 8px 0 0 0; font-size: 15px;">
                    {company_name} • {vacancy_title or 'Vacature'}
                </p>
            </td>
        </tr>
    </table>

    <!-- Main Content -->
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
        <tr>
            <td style="padding: 20px;">

                <!-- Score Hero Card -->
                <div style="background: white; border-radius: 20px; padding: 30px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); text-align: center;">
                    <div style="position: relative; display: inline-block;">
                        <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, {score_color}22 0%, {score_color}11 100%); border: 4px solid {score_color}; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 42px; font-weight: 800; color: {score_color};">{score}</span>
                        </div>
                    </div>
                    <div style="margin-top: 15px;">
                        <span style="font-size: 24px;">{score_emoji}</span>
                        <p style="color: {score_color}; font-size: 18px; font-weight: 700; margin: 5px 0 0 0;">
                            {score_label}
                        </p>
                        <p style="color: #9CA3AF; font-size: 13px; margin: 5px 0 0 0;">
                            van de 100 punten
                        </p>
                    </div>
                </div>

                <!-- Executive Summary -->
                <div style="background: white; border-radius: 16px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="color: #1F2937; margin: 0 0 12px 0; font-size: 18px;">
                        👋 Beste {contact_name},
                    </h2>
                    <p style="color: #4B5563; line-height: 1.6; margin: 0; font-size: 15px;">
                        {exec_summary}
                    </p>
                </div>

                <!-- Score Breakdown -->
                <div style="background: white; border-radius: 16px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="color: #1F2937; margin: 0 0 20px 0; font-size: 18px; display: flex; align-items: center;">
                        📊 Score per Criterium
                    </h2>
                    <table width="100%" cellpadding="0" cellspacing="0">
                        {score_bars}
                    </table>
                </div>

                <!-- Quick Wins -->
                <div style="background: white; border-radius: 16px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="color: #1F2937; margin: 0 0 15px 0; font-size: 18px;">
                        🚀 Top 3 Quick Wins
                    </h2>
                    {quick_wins_html}
                </div>

                <!-- Cialdini Tips (if available) -->
                {f'''<div style="background: white; border-radius: 16px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h2 style="color: #1F2937; margin: 0 0 15px 0; font-size: 18px;">
                        🧠 Overtuigingstips
                    </h2>
                    {cialdini_html}
                </div>''' if cialdini_html else ''}

                <!-- Improved Text -->
                {improved_text_html}

                <!-- CTA Button -->
                <div style="text-align: center; margin: 25px 0;">
                    <a href="https://recruitin.nl/contact"
                       style="display: inline-block; background: linear-gradient(135deg, #FF6B35 0%, #FF8F5C 100%); color: white; text-decoration: none;
                              padding: 16px 32px; border-radius: 10px; font-weight: 600; font-size: 15px;
                              box-shadow: 0 4px 14px rgba(255,107,53,0.35);">
                        📞 Gratis adviesgesprek inplannen
                    </a>
                </div>

                <!-- What's Next Card -->
                <div style="background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%); border-radius: 16px; padding: 25px; margin-bottom: 20px; border: 1px solid #FDBA74;">
                    <h3 style="color: #9A3412; margin: 0 0 12px 0; font-size: 16px;">
                        💡 Volgende stappen
                    </h3>
                    <ol style="color: #78350F; margin: 0; padding-left: 20px; line-height: 1.9; font-size: 14px;">
                        <li>Implementeer de Quick Wins in je vacaturetekst</li>
                        <li>Gebruik de verbeterde tekst als inspiratie</li>
                        <li>Meet het resultaat (meer sollicitaties!)</li>
                    </ol>
                </div>

            </td>
        </tr>
    </table>

    <!-- Footer -->
    <table width="100%" cellpadding="0" cellspacing="0" style="background: #1F2937; padding: 30px 20px;">
        <tr>
            <td align="center">
                <p style="color: white; font-size: 15px; font-weight: 600; margin: 0 0 5px 0;">
                    Recruitin B.V.
                </p>
                <p style="color: #9CA3AF; font-size: 13px; margin: 0 0 15px 0;">
                    Kandidatentekort.nl
                </p>
                <p style="color: #6B7280; font-size: 11px; margin: 0;">
                    Dit rapport is automatisch gegenereerd door AI.<br>
                    Vragen? Mail naar <a href="mailto:info@recruitin.nl" style="color: #FF6B35;">info@recruitin.nl</a>
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


def send_analysis_email(to_email, contact_name, company_name, vacancy_title, analysis_result, score=None):
    """Send the analysis report email with PDF attachment."""
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

        # Generate HTML email
        html = generate_email_html(contact_name, company_name, vacancy_title, analysis_result, score)
        msg_alternative.attach(MIMEText(html, 'html'))
        msg.attach(msg_alternative)

        # Generate and attach PDF
        try:
            pdf_content = generate_pdf_report(contact_name, company_name, vacancy_title, analysis_result, score)

            # Create safe filename
            safe_company = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_company = safe_company.replace(' ', '_')[:30]
            pdf_filename = f"Vacature_Analyse_{safe_company}_{datetime.now().strftime('%Y%m%d')}.pdf"

            # Attach PDF
            pdf_attachment = MIMEBase('application', 'pdf')
            pdf_attachment.set_payload(pdf_content)
            encoders.encode_base64(pdf_attachment)
            pdf_attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="{pdf_filename}"'
            )
            msg.attach(pdf_attachment)
            logger.info(f"PDF attachment added: {pdf_filename}")

        except Exception as pdf_error:
            logger.error(f"PDF generation failed, sending without attachment: {pdf_error}")
            # Continue sending email without PDF if generation fails

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Analysis email with PDF sent to {to_email}")
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
            # Send analysis email
            send_analysis_email(email, contact_name, company_name, vacancy_title, analysis_result, score)

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
        "version": "7.0",
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
        "version": "7.0",
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
