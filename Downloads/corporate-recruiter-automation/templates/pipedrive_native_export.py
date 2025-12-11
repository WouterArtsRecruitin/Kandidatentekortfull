"""
Pipedrive Native Export Module
==============================
Exports lead data to Pipedrive's native import format (.xlsx)

Features:
- All 23 standard Pipedrive fields supported
- Automatic deal title generation
- HTML note formatting
- Name splitting (first/last)
- Direct import compatibility

Usage:
    from templates.pipedrive_native_export import export_to_pipedrive_native
    
    export_to_pipedrive_native(
        df=your_dataframe,
        output_path='output.xlsx',
        pipeline_id=14,
        stage_name='lead'
    )
"""

import pandas as pd
from datetime import datetime
from typing import Optional
import re


def split_name(full_name: str) -> tuple:
    """Split full name into first and last name."""
    if not full_name or pd.isna(full_name):
        return ('', '')
    
    parts = str(full_name).strip().split()
    if len(parts) == 0:
        return ('', '')
    elif len(parts) == 1:
        return (parts[0], '')
    else:
        return (parts[0], ' '.join(parts[1:]))


def generate_note_html(row: dict) -> str:
    """Generate HTML-formatted note from lead data."""
    sections = []
    
    # Company info
    company_info = []
    if row.get('sector'):
        company_info.append(f"Sector: {row['sector']}")
    if row.get('fte'):
        company_info.append(f"FTE: {row['fte']}")
    if row.get('locatie') or row.get('Organization - Address'):
        loc = row.get('locatie') or row.get('Organization - Address')
        company_info.append(f"Locatie: {loc}")
    
    if company_info:
        sections.append("<b>🏢 Bedrijfsinfo</b><br/>" + "<br/>".join(company_info))
    
    # Score info
    score_info = []
    if row.get('score') or row.get('Deal - Lead Score'):
        score = row.get('score') or row.get('Deal - Lead Score')
        score_info.append(f"Lead Score: {score}")
    if row.get('priority') or row.get('Deal - Priority'):
        prio = row.get('priority') or row.get('Deal - Priority')
        score_info.append(f"Priority: {prio}")
    if row.get('tier') or row.get('Deal - Tier'):
        tier = row.get('tier') or row.get('Deal - Tier')
        score_info.append(f"Tier: {tier}")
    
    if score_info:
        sections.append("<b>📊 Scoring</b><br/>" + "<br/>".join(score_info))
    
    # Import metadata
    sections.append(f"<b>📅 Import</b><br/>Imported: {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>Source: JobDigger Automation v5.4")
    
    return "<br/><br/>".join(sections)


def create_blank_template(output_path: str = 'pipedrive_template_BLANK.xlsx'):
    """Create a blank Pipedrive import template with all standard columns."""
    columns = [
        'Deal - Title', 'Deal - Owner', 'Deal - Pipeline', 'Deal - Stage',
        'Deal - Value', 'Deal - Currency', 'Deal - Expected close date',
        'Deal - Status', 'Deal - Probability', 'Deal - Label',
        'Organization - Name', 'Organization - Owner', 'Organization - Label',
        'Organization - Address', 'Organization - Visible to',
        'Person - Name', 'Person - First name', 'Person - Last name',
        'Person - Owner', 'Person - Email', 'Person - Phone', 'Person - Label',
        'Note'
    ]
    
    df = pd.DataFrame(columns=columns)
    df.to_excel(output_path, index=False)
    return output_path


def export_to_pipedrive_native(
    df: pd.DataFrame,
    output_path: str,
    pipeline_id: int = 14,
    stage_name: str = 'lead',
    deal_value: float = 15000,
    currency: str = 'EUR',
    owner_name: str = 'Wouter Arts'
) -> str:
    """
    Export DataFrame to Pipedrive's native import format.
    
    Args:
        df: Source DataFrame with lead data
        output_path: Output Excel file path
        pipeline_id: Pipedrive pipeline ID (default: 14)
        stage_name: Stage name (default: 'lead')
        deal_value: Default deal value (default: 15000)
        currency: Currency code (default: 'EUR')
        owner_name: Owner name (default: 'Wouter Arts')
    
    Returns:
        Path to created Excel file
    """
    export_rows = []
    
    for _, row in df.iterrows():
        # Get company name
        org_name = (row.get('Organization - Name') or 
                   row.get('bedrijfsnaam') or 
                   row.get('company') or '')
        
        # Get person name and split
        full_name = (row.get('Person - Name') or 
                    row.get('contactpersoon') or 
                    row.get('contact_name') or '')
        first_name, last_name = split_name(full_name)
        
        # Get contact details
        email = (row.get('Person - Email') or 
                row.get('email') or '')
        phone = (row.get('Person - Phone') or 
                row.get('telefoon') or 
                row.get('phone') or '')
        title = (row.get('Person - Title') or 
                row.get('functie') or 
                row.get('title') or '')
        
        # Get address
        address = (row.get('Organization - Address') or 
                  row.get('locatie') or 
                  row.get('location') or '')
        
        # Generate deal title
        deal_title = f"{org_name} - Corporate Recruiter" if org_name else "New Lead"
        
        # Generate note
        note = generate_note_html(row.to_dict())
        
        export_rows.append({
            'Deal - Title': deal_title,
            'Deal - Owner': owner_name,
            'Deal - Pipeline': f'Pipeline {pipeline_id}',
            'Deal - Stage': stage_name,
            'Deal - Value': deal_value,
            'Deal - Currency': currency,
            'Deal - Expected close date': '',
            'Deal - Status': 'open',
            'Deal - Probability': '',
            'Deal - Label': '',
            'Organization - Name': org_name,
            'Organization - Owner': owner_name,
            'Organization - Label': '',
            'Organization - Address': address,
            'Organization - Visible to': 'Entire company',
            'Person - Name': full_name,
            'Person - First name': first_name,
            'Person - Last name': last_name,
            'Person - Owner': owner_name,
            'Person - Email': email,
            'Person - Phone': phone,
            'Person - Label': '',
            'Note': note
        })
    
    export_df = pd.DataFrame(export_rows)
    export_df.to_excel(output_path, index=False)
    
    print(f"✅ Exported {len(export_rows)} leads to {output_path}")
    return output_path
