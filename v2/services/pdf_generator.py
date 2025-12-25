"""
PDF Generator Service - PDFMonkey + ReportLab fallback.
"""

import io
import time
import requests
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass
from ..config import (
    PDFMONKEY_API_KEY, PDFMONKEY_TEMPLATE_ANALYSE, PDFMONKEY_TEMPLATE_VACATURE,
    USE_PDFMONKEY, BRAND_COLORS
)
from ..utils import get_logger, retry_with_backoff

logger = get_logger("pdf_generator")

# ReportLab imports (optional)
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.graphics.shapes import Drawing, Rect, String
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not installed - fallback PDF generation disabled")


@dataclass
class PDFResult:
    """Result of PDF generation."""
    success: bool
    pdf_bytes: Optional[bytes] = None
    error: Optional[str] = None


class PDFGenerator:
    """PDF generation service with PDFMonkey and ReportLab fallback."""

    def __init__(self):
        self.pdfmonkey_api_url = "https://api.pdfmonkey.io/api/v1/documents"

    # =========================================================================
    # PDFMONKEY
    # =========================================================================

    @retry_with_backoff(max_attempts=2, initial_delay=2.0, exceptions=(requests.RequestException,))
    def _pdfmonkey_create(self, template_id: str, payload: Dict) -> Optional[str]:
        """Create PDFMonkey document, return document ID."""
        headers = {
            "Authorization": f"Bearer {PDFMONKEY_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "document": {
                "document_template_id": template_id,
                "status": "pending",
                "payload": payload
            }
        }

        response = requests.post(self.pdfmonkey_api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        doc_data = response.json()
        return doc_data.get('document', {}).get('id')

    def _pdfmonkey_wait_and_download(self, document_id: str, max_attempts: int = 30, delay: int = 2) -> Optional[bytes]:
        """Wait for PDFMonkey document and download."""
        headers = {"Authorization": f"Bearer {PDFMONKEY_API_KEY}"}

        for attempt in range(max_attempts):
            try:
                response = requests.get(
                    f"{self.pdfmonkey_api_url}/{document_id}",
                    headers=headers,
                    timeout=30
                )

                if response.status_code == 200:
                    doc = response.json().get('document', {})
                    status = doc.get('status')

                    if status == 'success':
                        download_url = doc.get('download_url')
                        if download_url:
                            pdf_response = requests.get(download_url, timeout=60)
                            if pdf_response.status_code == 200:
                                return pdf_response.content

                    elif status == 'failure':
                        logger.error(f"PDFMonkey failed: {doc.get('failure_cause')}")
                        return None

                time.sleep(delay)

            except Exception as e:
                logger.error(f"PDFMonkey wait error: {e}")
                time.sleep(delay)

        logger.error("PDFMonkey timeout")
        return None

    def generate_with_pdfmonkey(self, template_id: str, payload: Dict, filename: str) -> PDFResult:
        """Generate PDF using PDFMonkey."""
        if not PDFMONKEY_API_KEY or not template_id:
            return PDFResult(success=False, error="PDFMonkey not configured")

        try:
            logger.info(f"Generating PDF with PDFMonkey: {filename}")

            # Create document
            document_id = self._pdfmonkey_create(template_id, payload)
            if not document_id:
                return PDFResult(success=False, error="Failed to create document")

            # Wait and download
            pdf_bytes = self._pdfmonkey_wait_and_download(document_id)
            if pdf_bytes:
                logger.info(f"PDFMonkey success: {filename} ({len(pdf_bytes)} bytes)")
                return PDFResult(success=True, pdf_bytes=pdf_bytes)

            return PDFResult(success=False, error="Failed to download PDF")

        except Exception as e:
            logger.error(f"PDFMonkey error: {e}")
            return PDFResult(success=False, error=str(e))

    # =========================================================================
    # REPORTLAB FALLBACK
    # =========================================================================

    def generate_analysis_report_reportlab(
        self,
        company_name: str,
        contact_name: str,
        vacancy_title: str,
        score: float,
        score_section: str,
        improvements: list,
        improved_text: str
    ) -> PDFResult:
        """Generate analysis report using ReportLab."""
        if not REPORTLAB_AVAILABLE:
            return PDFResult(success=False, error="ReportLab not available")

        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm)
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor(BRAND_COLORS['navy']),
                spaceAfter=20
            )

            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor(BRAND_COLORS['orange']),
                spaceBefore=15,
                spaceAfter=10
            )

            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=11,
                leading=16
            )

            # Build document
            elements = []

            # Header
            elements.append(Paragraph("VACATURE ANALYSE RAPPORT", title_style))
            elements.append(Paragraph(f"<b>{company_name}</b> - {vacancy_title}", body_style))
            elements.append(Paragraph(f"Rapport voor: {contact_name}", body_style))
            elements.append(Paragraph(f"Datum: {datetime.now().strftime('%d-%m-%Y')}", body_style))
            elements.append(Spacer(1, 20))

            # Score
            score_color = BRAND_COLORS['green'] if score >= 7 else (BRAND_COLORS['yellow'] if score >= 5 else BRAND_COLORS['red'])
            elements.append(Paragraph(f"<font size=36 color='{score_color}'><b>{score}/10</b></font>", ParagraphStyle('Score', alignment=TA_CENTER)))
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(score_section.replace('|', '<br/>'), body_style))
            elements.append(Spacer(1, 20))

            # Improvements
            elements.append(Paragraph("TOP 3 VERBETERPUNTEN", header_style))
            for i, improvement in enumerate(improvements[:3], 1):
                elements.append(Paragraph(f"<b>{i}.</b> {improvement}", body_style))
            elements.append(Spacer(1, 20))

            # Improved text
            if improved_text:
                elements.append(Paragraph("VERBETERDE VACATURETEKST", header_style))
                # Split into paragraphs
                for para in improved_text.split('\n\n'):
                    if para.strip():
                        elements.append(Paragraph(para.strip(), body_style))
                        elements.append(Spacer(1, 8))

            # Footer
            elements.append(Spacer(1, 30))
            elements.append(Paragraph(
                f"<font size=9 color='gray'>Gegenereerd door Kandidatentekort.nl | {datetime.now().strftime('%d-%m-%Y %H:%M')}</font>",
                ParagraphStyle('Footer', alignment=TA_CENTER)
            ))

            doc.build(elements)
            pdf_bytes = buffer.getvalue()
            buffer.close()

            logger.info(f"ReportLab PDF generated: {len(pdf_bytes)} bytes")
            return PDFResult(success=True, pdf_bytes=pdf_bytes)

        except Exception as e:
            logger.error(f"ReportLab error: {e}")
            return PDFResult(success=False, error=str(e))

    # =========================================================================
    # HIGH-LEVEL METHODS
    # =========================================================================

    def generate_analysis_report(
        self,
        company_name: str,
        contact_name: str,
        vacancy_title: str,
        analysis_result
    ) -> PDFResult:
        """
        Generate analysis report PDF.
        Uses PDFMonkey if configured, falls back to ReportLab.
        """
        # Try PDFMonkey first
        if USE_PDFMONKEY:
            payload = self._prepare_analyse_payload(
                company_name, contact_name, vacancy_title, analysis_result
            )
            result = self.generate_with_pdfmonkey(
                PDFMONKEY_TEMPLATE_ANALYSE,
                payload,
                f"Analyse_{company_name}.pdf"
            )
            if result.success:
                return result
            logger.warning("PDFMonkey failed, falling back to ReportLab")

        # Fallback to ReportLab
        return self.generate_analysis_report_reportlab(
            company_name,
            contact_name,
            vacancy_title,
            analysis_result.score,
            analysis_result.score_section,
            analysis_result.top_3_improvements,
            analysis_result.improved_text
        )

    def _prepare_analyse_payload(self, company_name: str, contact_name: str, vacancy_title: str, analysis_result) -> Dict:
        """Prepare payload for PDFMonkey analyse template."""
        score = analysis_result.score
        if score >= 8:
            score_level, score_label = 'excellent', 'Uitstekend'
        elif score >= 6:
            score_level, score_label = 'good', 'Goed'
        elif score >= 4:
            score_level, score_label = 'average', 'Gemiddeld'
        else:
            score_level, score_label = 'poor', 'Verbetering nodig'

        return {
            "report_date": datetime.now().strftime("%d-%m-%Y"),
            "contact_name": contact_name,
            "company_name": company_name,
            "vacancy_title": vacancy_title,
            "overall_score": f"{score}/10",
            "overall_score_percent": score * 10,
            "score_level": score_level,
            "score_label": score_label,
            "score_breakdown": analysis_result.score_section,
            "executive_summary": analysis_result.executive_summary,
            "improvements": analysis_result.top_3_improvements,
            "quick_wins": analysis_result.quick_wins,
            "improved_vacancy_text": analysis_result.improved_text,
            "bonus_tips": analysis_result.bonus_tips
        }


# Singleton
_pdf_generator = None


def get_pdf_generator() -> PDFGenerator:
    """Get singleton PDF generator instance."""
    global _pdf_generator
    if _pdf_generator is None:
        _pdf_generator = PDFGenerator()
    return _pdf_generator
