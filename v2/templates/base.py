"""
Base email template with shared styles and structure.
Outlook-compatible: table-based layout, no flexbox/gradients.
"""

from ..config import BRAND_COLORS, CALENDLY_URL, WHATSAPP_URL


def wrap_email(content: str, preview_text: str = "") -> str:
    """
    Wrap content in base email template with header and footer.
    Outlook-compatible with MSO conditionals.
    """
    return f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<!--[if mso]>
<xml>
<o:OfficeDocumentSettings>
<o:AllowPNG/>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml>
<![endif]-->
<title>Kandidatentekort.nl</title>
<style type="text/css">
body, table, td {{margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;}}
img {{border:0;height:auto;line-height:100%;outline:none;text-decoration:none;}}
table {{border-collapse:collapse !important;}}
a {{color:{BRAND_COLORS['orange']};text-decoration:none;}}
</style>
</head>
<body style="margin:0;padding:0;background-color:#f3f4f6;width:100%;">

<!-- Preview text (hidden) -->
<div style="display:none;max-height:0;overflow:hidden;">{preview_text}</div>

<!-- OUTLOOK WRAPPER -->
<!--[if mso]>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f3f4f6;">
<tr><td align="center" style="padding:30px 0;">
<![endif]-->

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f3f4f6;">
<tr><td align="center" style="padding:30px 15px;">

<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;max-width:600px;">

<!-- HEADER -->
<tr>
<td style="background-color:#1E3A8A;padding:25px 30px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td width="50" valign="middle">
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
<tr><td style="width:44px;height:44px;background-color:{BRAND_COLORS['orange']};text-align:center;font-size:22px;font-weight:bold;color:#ffffff;font-family:Arial,sans-serif;line-height:44px;">R</td></tr>
</table>
</td>
<td style="padding-left:14px;" valign="middle">
<p style="margin:0;color:#ffffff;font-size:18px;font-weight:bold;font-family:Arial,sans-serif;">KANDIDATENTEKORT.NL</p>
</td>
</tr>
</table>
</td>
</tr>

<!-- CONTENT -->
{content}

<!-- FOOTER -->
<tr>
<td style="background-color:#111827;padding:25px 30px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td valign="top">
<p style="margin:0 0 4px 0;font-size:15px;font-weight:bold;color:#ffffff;font-family:Arial,sans-serif;">Wouter Arts</p>
<p style="margin:0 0 2px 0;font-size:12px;color:#9CA3AF;font-family:Arial,sans-serif;">Founder & Recruitment Specialist</p>
<p style="margin:0;font-size:13px;font-weight:bold;color:{BRAND_COLORS['orange']};font-family:Arial,sans-serif;">Kandidatentekort.nl</p>
</td>
<td valign="top" align="right">
<p style="margin:0;font-size:11px;color:#9CA3AF;line-height:20px;font-family:Arial,sans-serif;">
06-14314593<br>
warts@recruitin.nl
</p>
</td>
</tr>
</table>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:15px;border-top:1px solid #374151;">
<tr><td style="padding-top:15px;text-align:center;">
<p style="margin:0;color:#6B7280;font-size:10px;font-family:Arial,sans-serif;">© 2025 Kandidatentekort.nl | Recruitin B.V.</p>
</td></tr>
</table>
</td>
</tr>

</table>
</td></tr>
</table>

<!--[if mso]>
</td></tr>
</table>
<![endif]-->

</body>
</html>'''


def get_cta_button(text: str, url: str, color: str = None) -> str:
    """Generate CTA button HTML."""
    bg_color = color or BRAND_COLORS['orange']
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center">
<tr><td style="background-color:{bg_color};padding:14px 28px;border-radius:6px;">
<a href="{url}" style="color:#ffffff;font-size:14px;font-weight:bold;text-decoration:none;font-family:Arial,sans-serif;">{text}</a>
</td></tr>
</table>'''


def get_cta_section() -> str:
    """Get standard CTA section with Calendly and WhatsApp."""
    return f'''<tr>
<td style="padding:0 30px 25px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#1E3A8A;border-radius:8px;">
<tr><td style="padding:25px;text-align:center;">
<p style="margin:0 0 8px 0;font-size:18px;font-weight:bold;color:#ffffff;font-family:Arial,sans-serif;">Wil je nog meer resultaat?</p>
<p style="margin:0 0 18px 0;font-size:13px;color:#E0E7FF;font-family:Arial,sans-serif;">Plan een gratis adviesgesprek van 15 minuten.</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center">
<tr>
<td style="padding:0 5px;">
{get_cta_button("📅 Plan Gesprek", CALENDLY_URL, "#10B981")}
</td>
<td style="padding:0 5px;">
{get_cta_button("💬 WhatsApp", WHATSAPP_URL + "?text=Hoi%20Wouter!", "#25D366")}
</td>
</tr>
</table>
</td></tr>
</table>
</td>
</tr>'''
