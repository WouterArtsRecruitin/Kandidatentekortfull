"""
Confirmation email template - sent immediately after form submission.
"""

from .base import wrap_email, BRAND_COLORS


def get_confirmation_email(voornaam: str, bedrijf: str, functie: str) -> str:
    """
    Generate confirmation email HTML.

    Args:
        voornaam: First name of recipient
        bedrijf: Company name
        functie: Job title/function
    """
    content = f'''
<tr>
<td style="padding:30px;">

<!-- Success Banner -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ECFDF5;border-left:4px solid #10B981;margin-bottom:25px;">
<tr><td style="padding:20px;">
<p style="margin:0;font-size:20px;font-weight:bold;color:#065F46;font-family:Arial,sans-serif;">✅ Ontvangen!</p>
<p style="margin:8px 0 0 0;font-size:14px;color:#047857;font-family:Arial,sans-serif;">Je vacature-analyse aanvraag is binnen</p>
</td></tr>
</table>

<!-- Greeting -->
<p style="margin:0 0 15px 0;font-size:18px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam}!</p>

<p style="margin:0 0 20px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Bedankt voor je aanvraag! We hebben je vacature voor <strong style="color:{BRAND_COLORS['orange']};">{functie}</strong> bij <strong style="color:{BRAND_COLORS['orange']};">{bedrijf}</strong> in goede orde ontvangen.
</p>

<!-- What to expect -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border-radius:8px;margin-bottom:25px;">
<tr><td style="padding:20px;">
<p style="margin:0 0 12px 0;font-size:16px;font-weight:bold;color:#1F2937;font-family:Arial,sans-serif;">⏰ Wat kun je verwachten?</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td width="30" valign="top" style="color:#10B981;font-size:16px;padding-top:2px;">✓</td>
<td style="padding-bottom:8px;font-size:13px;color:#374151;font-family:Arial,sans-serif;"><strong>Binnen 24 uur</strong> ontvang je een uitgebreide analyse</td>
</tr>
<tr>
<td width="30" valign="top" style="color:#10B981;font-size:16px;padding-top:2px;">✓</td>
<td style="padding-bottom:8px;font-size:13px;color:#374151;font-family:Arial,sans-serif;">Score-overzicht op <strong>9 conversie-criteria</strong></td>
</tr>
<tr>
<td width="30" valign="top" style="color:#10B981;font-size:16px;padding-top:2px;">✓</td>
<td style="padding-bottom:8px;font-size:13px;color:#374151;font-family:Arial,sans-serif;">Concrete verbeterpunten met <strong>direct toepasbare tips</strong></td>
</tr>
<tr>
<td width="30" valign="top" style="color:#10B981;font-size:16px;padding-top:2px;">✓</td>
<td style="font-size:13px;color:#374151;font-family:Arial,sans-serif;"><strong>Verbeterde vacaturetekst</strong> die je direct kunt gebruiken</td>
</tr>
</table>
</td></tr>
</table>

<p style="margin:0;font-size:14px;color:#374151;font-family:Arial,sans-serif;">
Vragen? Reply gewoon op deze email, dan help ik je verder.
</p>

</td>
</tr>
'''
    return wrap_email(content, f"Bedankt! Je vacature-analyse voor {functie} is in behandeling.")
