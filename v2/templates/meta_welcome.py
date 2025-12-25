"""
Meta/Facebook Lead Ads welcome email template.
Includes direct link to Typeform for quick conversion.
"""

from .base import wrap_email, get_cta_button, BRAND_COLORS
from ..config import TYPEFORM_ID, WEBSITE_URL


def get_meta_welcome_email(
    voornaam: str,
    bedrijf: str = "",
    email: str = "",
    typeform_prefill: bool = True
) -> str:
    """
    Generate Meta Lead Ads welcome email HTML.

    V2 improvement: Includes direct Typeform link for higher conversion.

    Args:
        voornaam: First name of recipient
        bedrijf: Company name (optional)
        email: Email address for Typeform pre-fill
        typeform_prefill: Whether to pre-fill Typeform with known data
    """
    # Build Typeform URL with pre-filled data
    typeform_url = f"https://form.typeform.com/to/{TYPEFORM_ID}"
    if typeform_prefill and email:
        params = []
        if email:
            params.append(f"email={email}")
        if bedrijf:
            params.append(f"bedrijf={bedrijf}")
        params.append("source=meta_lead")
        typeform_url += "#" + "&".join(params)

    bedrijf_text = f' namens <strong style="color:{BRAND_COLORS["orange"]};">{bedrijf}</strong>' if bedrijf else ''

    content = f'''
<tr>
<td style="padding:30px;">

<!-- Welcome Banner -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFF7ED;border-left:4px solid {BRAND_COLORS['orange']};margin-bottom:25px;">
<tr><td style="padding:20px;">
<p style="margin:0;font-size:22px;font-weight:bold;color:#C2410C;font-family:Arial,sans-serif;">👋 Welkom!</p>
<p style="margin:8px 0 0 0;font-size:14px;color:#EA580C;font-family:Arial,sans-serif;">Goed dat je interesse hebt in betere vacatures</p>
</td></tr>
</table>

<!-- Greeting -->
<p style="margin:0 0 15px 0;font-size:18px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam}!</p>

<p style="margin:0 0 20px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Bedankt voor je aanmelding via Facebook!{bedrijf_text} Fijn dat je geïnteresseerd bent in onze gratis vacature-analyse.
</p>

<!-- How it works -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border-radius:8px;margin-bottom:25px;">
<tr><td style="padding:20px;">
<p style="margin:0 0 15px 0;font-size:16px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">📋 Zo werkt het:</p>

<!-- Step 1 -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px;">
<tr>
<td width="35" valign="top">
<table cellpadding="0" cellspacing="0"><tr>
<td style="width:28px;height:28px;background-color:{BRAND_COLORS['orange']};text-align:center;font-weight:bold;color:white;font-size:14px;font-family:Arial,sans-serif;line-height:28px;">1</td>
</tr></table>
</td>
<td style="padding-left:10px;font-size:13px;color:#374151;line-height:20px;font-family:Arial,sans-serif;">
<strong>Stuur je vacaturetekst</strong> - via het formulier hieronder (1 minuut)
</td>
</tr>
</table>

<!-- Step 2 -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px;">
<tr>
<td width="35" valign="top">
<table cellpadding="0" cellspacing="0"><tr>
<td style="width:28px;height:28px;background-color:{BRAND_COLORS['orange']};text-align:center;font-weight:bold;color:white;font-size:14px;font-family:Arial,sans-serif;line-height:28px;">2</td>
</tr></table>
</td>
<td style="padding-left:10px;font-size:13px;color:#374151;line-height:20px;font-family:Arial,sans-serif;">
Wij analyseren deze <strong>gratis</strong> op 9 conversie-criteria
</td>
</tr>
</table>

<!-- Step 3 -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px;">
<tr>
<td width="35" valign="top">
<table cellpadding="0" cellspacing="0"><tr>
<td style="width:28px;height:28px;background-color:{BRAND_COLORS['orange']};text-align:center;font-weight:bold;color:white;font-size:14px;font-family:Arial,sans-serif;line-height:28px;">3</td>
</tr></table>
</td>
<td style="padding-left:10px;font-size:13px;color:#374151;line-height:20px;font-family:Arial,sans-serif;">
Je ontvangt <strong>binnen 24 uur</strong> een rapport met verbeterpunten
</td>
</tr>
</table>

<!-- Step 4 -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td width="35" valign="top">
<table cellpadding="0" cellspacing="0"><tr>
<td style="width:28px;height:28px;background-color:#10B981;text-align:center;font-weight:bold;color:white;font-size:14px;font-family:Arial,sans-serif;line-height:28px;">✓</td>
</tr></table>
</td>
<td style="padding-left:10px;font-size:13px;color:#374151;line-height:20px;font-family:Arial,sans-serif;">
<strong>Meer sollicitaties</strong> van de juiste kandidaten!
</td>
</tr>
</table>

</td></tr>
</table>

<!-- PRIMARY CTA -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{BRAND_COLORS['orange']};border-radius:8px;margin-bottom:20px;">
<tr><td style="padding:20px;text-align:center;">
<p style="margin:0 0 12px 0;font-size:16px;font-weight:bold;color:#ffffff;font-family:Arial,sans-serif;">🚀 Start direct - duurt maar 1 minuut</p>
{get_cta_button("📝 Upload je vacature", typeform_url, "#ffffff").replace('color:#ffffff', 'color:' + BRAND_COLORS['orange'])}
</td></tr>
</table>

<!-- Alternative -->
<p style="margin:0;font-size:13px;color:#6B7280;text-align:center;font-family:Arial,sans-serif;">
Of reply op deze email met je vacaturetekst
</p>

</td>
</tr>
'''
    return wrap_email(content, "Welkom! Stuur je vacature en ontvang gratis een analyse.")
