"""
Analysis report email template - sent with full analysis results.
"""

from .base import wrap_email, get_cta_section, BRAND_COLORS


def get_score_badge(score: float) -> tuple:
    """Get score color and label based on score value."""
    if score >= 8.0:
        return "#10B981", "#ECFDF5", "Uitstekend", "🏆"
    elif score >= 6.5:
        return "#3B82F6", "#EFF6FF", "Goed", "👍"
    elif score >= 5.0:
        return "#F59E0B", "#FFFBEB", "Kan beter", "📈"
    else:
        return "#EF4444", "#FEF2F2", "Verbetering nodig", "⚠️"


def get_analysis_report_email(
    voornaam: str,
    bedrijf: str,
    score: float,
    score_section: str,
    improvements: list,
    improved_text: str,
    bonus_tips: list = None,
    original_text: str = ""
) -> str:
    """
    Generate analysis report email HTML.

    Args:
        voornaam: Recipient first name
        bedrijf: Company name
        score: Overall score (0-10)
        score_section: Score breakdown string
        improvements: List of top 3 improvements
        improved_text: Full improved vacancy text
        bonus_tips: Optional list of bonus tips
        original_text: Optional original text for before/after
    """
    score_color, score_bg, score_label, score_emoji = get_score_badge(score)

    # Build improvements HTML
    improvements_html = ""
    for i, imp in enumerate(improvements[:3], 1):
        improvements_html += f'''<tr>
<td style="padding:10px 0;border-bottom:1px solid #FDE68A;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td width="35" valign="top">
<table cellpadding="0" cellspacing="0"><tr>
<td style="width:28px;height:28px;background-color:#F59E0B;text-align:center;font-weight:bold;color:white;font-size:13px;font-family:Arial,sans-serif;line-height:28px;">{i}</td>
</tr></table>
</td>
<td style="padding-left:10px;color:#78350F;font-size:13px;line-height:20px;font-family:Arial,sans-serif;">{imp}</td>
</tr>
</table>
</td>
</tr>'''

    # Build tips HTML
    tips_html = ""
    if bonus_tips:
        for tip in bonus_tips[:3]:
            tips_html += f'''<tr><td style="padding:6px 0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
<tr>
<td width="35" valign="top" style="padding:10px;font-size:16px;">💡</td>
<td style="padding:10px;color:#5B21B6;font-size:12px;line-height:18px;font-family:Arial,sans-serif;">{tip}</td>
</tr>
</table>
</td></tr>'''

    # Truncate texts for display
    improved_preview = improved_text[:400] + '...' if len(improved_text) > 400 else improved_text
    improved_text_html = improved_text.replace('\n', '<br>')

    content = f'''
<!-- SCORE SECTION -->
<tr>
<td style="padding:35px 30px;background-color:#f8fafc;" align="center">
<!-- Score Box -->
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:15px;">
<tr><td align="center" style="width:120px;height:120px;border:6px solid {score_color};background-color:#ffffff;">
<p style="margin:0;font-size:42px;font-weight:bold;color:{score_color};font-family:Arial,sans-serif;line-height:1;">{score}</p>
<p style="margin:4px 0 0 0;font-size:14px;color:#9CA3AF;font-family:Arial,sans-serif;">/10</p>
</td></tr>
</table>
<!-- Score Label -->
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
<tr><td style="background-color:{score_bg};border:2px solid {score_color};padding:8px 18px;">
<p style="margin:0;font-size:13px;font-weight:bold;color:{score_color};font-family:Arial,sans-serif;">{score_emoji} {score_label}</p>
</td></tr>
</table>
<!-- Score Breakdown -->
<p style="margin:15px 0 0 0;color:#6B7280;font-size:12px;font-family:Arial,sans-serif;line-height:1.5;">{score_section.replace('|', ' | ')}</p>
</td>
</tr>

<!-- INTRO -->
<tr>
<td style="padding:25px 30px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td width="4" style="background-color:{BRAND_COLORS['orange']};"></td>
<td style="padding-left:18px;">
<p style="margin:0 0 10px 0;font-size:18px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam}! 👋</p>
<p style="margin:0;color:#4B5563;font-size:13px;line-height:21px;font-family:Arial,sans-serif;">Bedankt voor het insturen van je vacature via <strong style="color:{BRAND_COLORS['orange']};">kandidatentekort.nl</strong>. Onze AI heeft je tekst grondig geanalyseerd. Hieronder vind je de resultaten met concrete verbeteringen.</p>
</td>
</tr>
</table>
</td>
</tr>

<!-- TOP 3 VERBETERPUNTEN -->
<tr>
<td style="padding:0 30px 25px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFBEB;border:2px solid #F59E0B;">
<tr><td style="padding:20px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:15px;">
<tr>
<td width="40" valign="middle"><table cellpadding="0" cellspacing="0"><tr><td style="width:36px;height:36px;background-color:#F59E0B;text-align:center;font-size:18px;line-height:36px;">🎯</td></tr></table></td>
<td style="padding-left:12px;" valign="middle">
<p style="margin:0;font-size:16px;font-weight:bold;color:#92400E;font-family:Arial,sans-serif;">Top 3 Verbeterpunten</p>
</td>
</tr>
</table>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{improvements_html}</table>
</td></tr>
</table>
</td>
</tr>

<!-- VERBETERDE TEKST -->
<tr>
<td style="padding:0 30px 25px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ECFDF5;border:2px solid #10B981;">
<tr><td style="padding:20px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:15px;">
<tr>
<td width="40" valign="middle"><table cellpadding="0" cellspacing="0"><tr><td style="width:36px;height:36px;background-color:#10B981;text-align:center;font-size:18px;line-height:36px;">✍️</td></tr></table></td>
<td style="padding-left:12px;" valign="middle">
<p style="margin:0 0 2px 0;font-size:10px;font-weight:bold;color:#047857;text-transform:uppercase;font-family:Arial,sans-serif;">Direct te gebruiken</p>
<p style="margin:0;font-size:16px;font-weight:bold;color:#065F46;font-family:Arial,sans-serif;">Verbeterde Vacaturetekst</p>
</td>
</tr>
</table>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;border:1px solid #A7F3D0;">
<tr><td style="padding:15px;font-size:12px;color:#374151;line-height:20px;font-family:Arial,sans-serif;">{improved_text_html}</td></tr>
</table>
<p style="margin:12px 0 0 0;text-align:center;font-size:11px;color:#059669;font-family:Arial,sans-serif;">💾 Kopieer deze tekst en plaats direct in je vacature</p>
</td></tr>
</table>
</td>
</tr>

<!-- BONUS TIPS -->
{f"""<tr>
<td style="padding:0 30px 25px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F5F3FF;border:2px solid #8B5CF6;">
<tr><td style="padding:20px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px;">
<tr>
<td width="40" valign="middle"><table cellpadding="0" cellspacing="0"><tr><td style="width:36px;height:36px;background-color:#8B5CF6;text-align:center;font-size:18px;line-height:36px;">🚀</td></tr></table></td>
<td style="padding-left:12px;" valign="middle">
<p style="margin:0;font-size:16px;font-weight:bold;color:#5B21B6;font-family:Arial,sans-serif;">Bonus Tips</p>
</td>
</tr>
</table>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{tips_html}</table>
</td></tr>
</table>
</td>
</tr>""" if bonus_tips else ""}

<!-- CTA SECTION -->
{get_cta_section()}
'''

    return wrap_email(content, f"Je vacature-analyse voor {bedrijf} is klaar! Score: {score}/10")
