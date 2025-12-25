"""
PDF delivery email template - sent with analysis PDFs.
"""

from .base import wrap_email, get_cta_section, get_cta_button, BRAND_COLORS


def get_pdf_delivery_email(
    voornaam: str,
    functie_titel: str,
    bedrijf: str,
    vacature_pdf_url: str = "",
    rapport_pdf_url: str = "",
    score: float = None
) -> str:
    """
    Generate PDF delivery email HTML.

    Args:
        voornaam: Recipient first name
        functie_titel: Job title
        bedrijf: Company name
        vacature_pdf_url: URL to improved vacancy PDF
        rapport_pdf_url: URL to analysis report PDF
        score: Analysis score (optional, for display)
    """
    score_text = f" (Score: {score}/10)" if score else ""

    content = f'''
<tr>
<td style="padding:30px;">

<!-- Success Banner -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ECFDF5;border-left:4px solid #10B981;margin-bottom:25px;">
<tr><td style="padding:20px;">
<p style="margin:0;font-size:20px;font-weight:bold;color:#065F46;font-family:Arial,sans-serif;">📄 Je analyse is klaar!</p>
<p style="margin:8px 0 0 0;font-size:14px;color:#047857;font-family:Arial,sans-serif;">Bekijk je persoonlijke rapport{score_text}</p>
</td></tr>
</table>

<!-- Greeting -->
<p style="margin:0 0 15px 0;font-size:18px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam}!</p>

<p style="margin:0 0 20px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Goed nieuws! De analyse van je vacature <strong style="color:{BRAND_COLORS['orange']};">"{functie_titel}"</strong> voor <strong style="color:{BRAND_COLORS['orange']};">{bedrijf}</strong> is afgerond.
</p>

<!-- PDF Downloads -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border-radius:8px;margin-bottom:25px;">
<tr><td style="padding:20px;">
<p style="margin:0 0 15px 0;font-size:16px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">📥 Download je documenten:</p>

<!-- Vacature PDF -->
{f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;border:1px solid #E5E7EB;border-radius:6px;margin-bottom:10px;">
<tr>
<td width="50" style="padding:15px;text-align:center;font-size:24px;">📄</td>
<td style="padding:15px 0;">
<p style="margin:0;font-size:14px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">Verbeterde Vacaturetekst</p>
<p style="margin:4px 0 0 0;font-size:12px;color:#6B7280;font-family:Arial,sans-serif;">Direct te gebruiken in je werving</p>
</td>
<td style="padding:15px;text-align:right;">
<a href="{vacature_pdf_url}" style="display:inline-block;background-color:#10B981;color:#ffffff;padding:8px 16px;border-radius:4px;font-size:12px;font-weight:bold;text-decoration:none;font-family:Arial,sans-serif;">Download</a>
</td>
</tr>
</table>""" if vacature_pdf_url else ""}

<!-- Rapport PDF -->
{f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;border:1px solid #E5E7EB;border-radius:6px;">
<tr>
<td width="50" style="padding:15px;text-align:center;font-size:24px;">📊</td>
<td style="padding:15px 0;">
<p style="margin:0;font-size:14px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">Analyse Rapport</p>
<p style="margin:4px 0 0 0;font-size:12px;color:#6B7280;font-family:Arial,sans-serif;">Volledige analyse met scores en tips</p>
</td>
<td style="padding:15px;text-align:right;">
<a href="{rapport_pdf_url}" style="display:inline-block;background-color:#3B82F6;color:#ffffff;padding:8px 16px;border-radius:4px;font-size:12px;font-weight:bold;text-decoration:none;font-family:Arial,sans-serif;">Download</a>
</td>
</tr>
</table>""" if rapport_pdf_url else ""}

</td></tr>
</table>

<!-- What's next -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFF7ED;border-left:4px solid {BRAND_COLORS['orange']};margin-bottom:25px;">
<tr><td style="padding:20px;">
<p style="margin:0 0 10px 0;font-size:14px;font-weight:bold;color:#C2410C;font-family:Arial,sans-serif;">💡 Tip: Implementeer de verbeteringen deze week</p>
<p style="margin:0;font-size:13px;color:#EA580C;line-height:20px;font-family:Arial,sans-serif;">
Bedrijven die de aanpassingen binnen 7 dagen doorvoeren zien gemiddeld <strong>35% meer reacties</strong> op hun vacatures.
</p>
</td></tr>
</table>

<p style="margin:0 0 25px 0;font-size:14px;color:#374151;font-family:Arial,sans-serif;">
Vragen over het rapport? Reply op deze email of plan een kort gesprek via de button hieronder.
</p>

</td>
</tr>

<!-- CTA SECTION -->
{get_cta_section()}
'''

    return wrap_email(content, f"Je vacature-analyse voor {bedrijf} staat klaar om te downloaden!")
