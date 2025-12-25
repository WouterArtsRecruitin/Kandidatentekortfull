"""
Nurture Email Templates - 8 emails over 30 days.
"""

from ..templates.base import wrap_email, get_cta_section, BRAND_COLORS
from ..config import CALENDLY_URL, WHATSAPP_URL


def get_nurture_email_subject(email_num: int) -> str:
    """Get subject line for nurture email."""
    subjects = {
        1: "Even checken - alles goed ontvangen?",
        2: "Is het gelukt om de aanpassingen door te voeren?",
        3: "Hoe gaat het met de resultaten?",
        4: "Tip: De kracht van een goede functietitel",
        5: "Tip: Waarom salaris vermelden 35% meer reacties geeft",
        6: "Tip: Een opening die direct pakt",
        7: "Gratis adviesgesprek - interesse?",
        8: "Laatste check-in van mij",
    }
    return subjects.get(email_num, "Follow-up van Kandidatentekort.nl")


def get_nurture_email_html(email_num: int, voornaam: str, functie_titel: str) -> str:
    """Generate HTML for nurture email."""
    templates = {
        1: _get_email_1(voornaam, functie_titel),
        2: _get_email_2(voornaam, functie_titel),
        3: _get_email_3(voornaam, functie_titel),
        4: _get_email_4(voornaam, functie_titel),
        5: _get_email_5(voornaam, functie_titel),
        6: _get_email_6(voornaam, functie_titel),
        7: _get_email_7(voornaam, functie_titel),
        8: _get_email_8(voornaam, functie_titel),
    }
    return templates.get(email_num, "")


def _email_content(body: str, preview: str = "") -> str:
    """Wrap email body in base template."""
    content = f'''
<tr>
<td style="padding:30px;">
{body}
</td>
</tr>
'''
    return wrap_email(content, preview)


def _get_email_1(voornaam: str, functie_titel: str) -> str:
    """Day 1: Check-in"""
    return _email_content(f'''
<p style="margin:0 0 15px 0;font-size:16px;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam},</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Even een snelle check: heb je mijn analyse van je vacature goed ontvangen?
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Ik wil er zeker van zijn dat alles duidelijk is. Mocht je vragen hebben over de verbeterpunten of hoe je ze het beste kunt implementeren - laat het me weten!
</p>

<p style="margin:0 0 20px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Je kunt gewoon op deze email reageren.
</p>

<p style="margin:0;font-size:14px;color:#1F2937;font-family:Arial,sans-serif;">
Groet,<br>
<strong>Wouter</strong>
</p>
''', "Even checken of je mijn analyse hebt ontvangen...")


def _get_email_2(voornaam: str, functie_titel: str) -> str:
    """Day 3: Is het gelukt?"""
    return _email_content(f'''
<p style="margin:0 0 15px 0;font-size:16px;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam},</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Is het al gelukt om de aanpassingen uit mijn analyse door te voeren?
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Ik begrijp dat het soms lastig is om tijd te vinden. Mijn tip: begin met de <strong>top 3 verbeterpunten</strong>. Die hebben vaak de grootste impact.
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Loop je ergens tegenaan? Ik help je graag verder.
</p>

<p style="margin:0;font-size:14px;color:#1F2937;font-family:Arial,sans-serif;">
Groet,<br>
<strong>Wouter</strong>
</p>
''', "Is het al gelukt om de verbeteringen door te voeren?")


def _get_email_3(voornaam: str, functie_titel: str) -> str:
    """Day 5: Resultaten"""
    return _email_content(f'''
<p style="margin:0 0 15px 0;font-size:16px;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam},</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Benieuwd: heb je al iets gemerkt van de aanpassingen aan je vacature?
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Andere klanten melden vaak dat ze binnen de eerste week al meer relevante reacties krijgen. Sommigen zien zelfs een <strong>verdubbeling</strong> in het aantal sollicitaties.
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Ik hoor graag hoe het bij jou gaat!
</p>

<p style="margin:0;font-size:14px;color:#1F2937;font-family:Arial,sans-serif;">
Groet,<br>
<strong>Wouter</strong>
</p>
''', "Hoe gaat het met de resultaten van je verbeterde vacature?")


def _get_email_4(voornaam: str, functie_titel: str) -> str:
    """Day 8: Tip Functietitel"""
    return _email_content(f'''
<p style="margin:0 0 15px 0;font-size:16px;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam},</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Een extra tip die ik je wilde delen:
</p>

<table role="presentation" width="100%" style="background-color:#FFF7ED;border-left:4px solid {BRAND_COLORS['orange']};margin:20px 0;">
<tr><td style="padding:20px;">
<p style="margin:0 0 10px 0;font-size:15px;font-weight:bold;color:#C2410C;font-family:Arial,sans-serif;">💡 De kracht van je functietitel</p>
<p style="margin:0;font-size:13px;color:#EA580C;line-height:20px;font-family:Arial,sans-serif;">
De functietitel is het eerste wat kandidaten zien. Een herkenbare, zoekbare titel kan je bereik met <strong>40%</strong> vergroten.
</p>
</td></tr>
</table>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
<strong>Voorbeelden:</strong><br>
❌ "Medewerker Operations" → ✅ "Operations Manager"<br>
❌ "Allround Technicus" → ✅ "Onderhoudsmonteur Productie"
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Gebruik de termen die kandidaten daadwerkelijk zoeken!
</p>

<p style="margin:0;font-size:14px;color:#1F2937;font-family:Arial,sans-serif;">
Groet,<br>
<strong>Wouter</strong>
</p>
''', "Tip: Hoe je functietitel je bereik kan vergroten")


def _get_email_5(voornaam: str, functie_titel: str) -> str:
    """Day 11: Tip Salaris"""
    return _email_content(f'''
<p style="margin:0 0 15px 0;font-size:16px;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam},</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Nog een waardevolle tip:
</p>

<table role="presentation" width="100%" style="background-color:#ECFDF5;border-left:4px solid #10B981;margin:20px 0;">
<tr><td style="padding:20px;">
<p style="margin:0 0 10px 0;font-size:15px;font-weight:bold;color:#065F46;font-family:Arial,sans-serif;">💰 Salaris vermelden = 35% meer reacties</p>
<p style="margin:0;font-size:13px;color:#047857;line-height:20px;font-family:Arial,sans-serif;">
Onderzoek toont aan dat vacatures met een salarisindicatie gemiddeld <strong>35% meer sollicitaties</strong> ontvangen. Kandidaten willen weten of het de moeite waard is.
</p>
</td></tr>
</table>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Geen exact bedrag nodig - een bandbreedte werkt net zo goed:<br>
"€3.500 - €4.500 bruto per maand, afhankelijk van ervaring"
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Dit filtert ook meteen ongeschikte kandidaten eruit!
</p>

<p style="margin:0;font-size:14px;color:#1F2937;font-family:Arial,sans-serif;">
Groet,<br>
<strong>Wouter</strong>
</p>
''', "Wist je dat salaris vermelden 35% meer reacties geeft?")


def _get_email_6(voornaam: str, functie_titel: str) -> str:
    """Day 14: Tip Opening"""
    return _email_content(f'''
<p style="margin:0 0 15px 0;font-size:16px;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam},</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Laatste tip in deze serie:
</p>

<table role="presentation" width="100%" style="background-color:#EFF6FF;border-left:4px solid #3B82F6;margin:20px 0;">
<tr><td style="padding:20px;">
<p style="margin:0 0 10px 0;font-size:15px;font-weight:bold;color:#1E40AF;font-family:Arial,sans-serif;">🎯 De eerste zin bepaalt alles</p>
<p style="margin:0;font-size:13px;color:#1D4ED8;line-height:20px;font-family:Arial,sans-serif;">
Je hebt <strong>3 seconden</strong> om de aandacht te pakken. Begin niet met "Wij zoeken..." maar met wat de kandidaat krijgt.
</p>
</td></tr>
</table>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
<strong>Voorbeeld:</strong><br>
❌ "Wij zijn een groeiend bedrijf en zoeken een..."<br>
✅ "Wil jij werken aan innovatieve projecten in een team waar je ideeën ertoe doen?"
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Spreek de kandidaat direct aan met "jij" en focus op wat zij krijgen, niet wat jij zoekt.
</p>

<p style="margin:0;font-size:14px;color:#1F2937;font-family:Arial,sans-serif;">
Groet,<br>
<strong>Wouter</strong>
</p>
''', "De eerste zin van je vacature bepaalt alles - hier is waarom")


def _get_email_7(voornaam: str, functie_titel: str) -> str:
    """Day 21: Gesprek Aanbod"""
    return _email_content(f'''
<p style="margin:0 0 15px 0;font-size:16px;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam},</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Het is nu een paar weken geleden dat je mijn analyse hebt ontvangen. Ik vroeg me af hoe het gaat met de werving.
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Mocht je behoefte hebben aan persoonlijk advies, dan bied ik je graag een <strong>gratis adviesgesprek van 15 minuten</strong> aan.
</p>

<table role="presentation" width="100%" style="background-color:{BRAND_COLORS['orange']};border-radius:8px;margin:20px 0;">
<tr><td style="padding:25px;text-align:center;">
<p style="margin:0 0 12px 0;font-size:16px;font-weight:bold;color:#ffffff;font-family:Arial,sans-serif;">📅 Plan een gratis adviesgesprek</p>
<table role="presentation" cellpadding="0" cellspacing="0" align="center">
<tr><td style="background-color:#ffffff;padding:12px 24px;border-radius:6px;">
<a href="{CALENDLY_URL}" style="color:{BRAND_COLORS['orange']};font-size:14px;font-weight:bold;text-decoration:none;font-family:Arial,sans-serif;">Kies een moment →</a>
</td></tr>
</table>
</td></tr>
</table>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
We kunnen dan samen kijken naar je specifieke situatie en ik geef je gerichte tips.
</p>

<p style="margin:0;font-size:14px;color:#1F2937;font-family:Arial,sans-serif;">
Groet,<br>
<strong>Wouter</strong>
</p>
''', "Gratis adviesgesprek - interesse?")


def _get_email_8(voornaam: str, functie_titel: str) -> str:
    """Day 30: Final Check-in"""
    return _email_content(f'''
<p style="margin:0 0 15px 0;font-size:16px;color:#1F2937;font-family:Arial,sans-serif;">Hoi {voornaam},</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Dit is mijn laatste check-in over de vacature-analyse die ik voor je heb gemaakt.
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Ik hoop dat de tips en verbeterpunten je hebben geholpen bij je werving. Mocht je in de toekomst weer een vacature willen laten analyseren, dan ben ik er voor je.
</p>

<p style="margin:0 0 15px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
En natuurlijk: als je ooit persoonlijke begeleiding wilt bij je recruitment, laat het me weten. Ik help ondernemers graag om de juiste mensen te vinden.
</p>

<p style="margin:0 0 20px 0;font-size:14px;color:#374151;line-height:22px;font-family:Arial,sans-serif;">
Succes met de werving! 🍀
</p>

<p style="margin:0;font-size:14px;color:#1F2937;font-family:Arial,sans-serif;">
Met vriendelijke groet,<br>
<strong>Wouter Arts</strong><br>
<span style="color:#6B7280;font-size:13px;">Kandidatentekort.nl</span>
</p>
''', "Laatste check-in - succes met de werving!")
