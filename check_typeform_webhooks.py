#!/usr/bin/env python3
"""
Script om Typeform webhook configuratie te controleren.
Controleert of er webhooks (inclusief Rednee) actief zijn.
"""

import os
import requests
import json

# Typeform configuratie
TYPEFORM_PERSONAL_TOKEN = os.getenv('TYPEFORM_PERSONAL_TOKEN', '')
TYPEFORM_FORM_ID = "kalFRTCA"  # Actuele form ID

def check_typeform_webhooks():
    """Haal alle webhooks op voor het Typeform formulier."""

    if not TYPEFORM_PERSONAL_TOKEN:
        print("❌ TYPEFORM_PERSONAL_TOKEN niet geconfigureerd!")
        print("   Stel deze in als environment variable en probeer opnieuw.")
        return None

    # Typeform API endpoint voor webhooks
    url = f"https://api.typeform.com/forms/{TYPEFORM_FORM_ID}/webhooks"

    headers = {
        "Authorization": f"Bearer {TYPEFORM_PERSONAL_TOKEN}",
        "Content-Type": "application/json"
    }

    print(f"🔍 Controleren webhooks voor Typeform: {TYPEFORM_FORM_ID}")
    print(f"   API URL: {url}")
    print()

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            webhooks = data.get('items', [])

            print(f"✅ API Response ontvangen")
            print(f"   Totaal aantal webhooks: {len(webhooks)}")
            print()

            if not webhooks:
                print("⚠️  Geen webhooks geconfigureerd voor dit formulier!")
                return []

            print("=" * 60)
            print("GEVONDEN WEBHOOKS:")
            print("=" * 60)

            rednee_found = False

            for i, webhook in enumerate(webhooks, 1):
                tag = webhook.get('tag', 'Onbekend')
                url = webhook.get('url', 'Geen URL')
                enabled = webhook.get('enabled', False)
                created = webhook.get('created_at', 'Onbekend')
                updated = webhook.get('updated_at', 'Onbekend')

                status = "🟢 ACTIEF" if enabled else "🔴 INACTIEF"

                print(f"\n📌 Webhook #{i}: {tag}")
                print(f"   Status:     {status}")
                print(f"   URL:        {url}")
                print(f"   Aangemaakt: {created}")
                print(f"   Bijgewerkt: {updated}")

                # Check voor Rednee
                if 'rednee' in tag.lower() or 'rednee' in url.lower():
                    rednee_found = True
                    print(f"   ⚡ REDNEE WEBHOOK GEVONDEN!")

            print()
            print("=" * 60)

            if rednee_found:
                print("✅ REDNEE webhook is geconfigureerd in Typeform")
            else:
                print("❌ GEEN Rednee webhook gevonden in Typeform configuratie")

            return webhooks

        elif response.status_code == 401:
            print("❌ Authenticatie mislukt - controleer TYPEFORM_PERSONAL_TOKEN")
            return None
        elif response.status_code == 404:
            print(f"❌ Formulier niet gevonden: {TYPEFORM_FORM_ID}")
            return None
        else:
            print(f"❌ API fout: {response.status_code}")
            print(f"   Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Verbindingsfout: {e}")
        return None


def get_form_details():
    """Haal algemene formulier details op."""

    if not TYPEFORM_PERSONAL_TOKEN:
        return None

    url = f"https://api.typeform.com/forms/{TYPEFORM_FORM_ID}"

    headers = {
        "Authorization": f"Bearer {TYPEFORM_PERSONAL_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print("📋 FORMULIER DETAILS:")
            print(f"   Titel:      {data.get('title', 'Onbekend')}")
            print(f"   ID:         {data.get('id', 'Onbekend')}")
            print(f"   Workspace:  {data.get('workspace', {}).get('href', 'Onbekend')}")
            print()
            return data
        else:
            print(f"⚠️  Kon formulier details niet ophalen: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️  Fout bij ophalen formulier details: {e}")
        return None


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("TYPEFORM WEBHOOK CHECKER")
    print("=" * 60)
    print()

    # Formulier details
    get_form_details()

    # Webhooks controleren
    webhooks = check_typeform_webhooks()

    print()
    print("Script voltooid.")
