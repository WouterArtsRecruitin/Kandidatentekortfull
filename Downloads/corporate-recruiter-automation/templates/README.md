# Pipedrive Native Export Templates

Direct importeerbare Excel bestanden voor Pipedrive.

## Quick Start

```python
from templates.pipedrive_native_export import export_to_pipedrive_native

export_to_pipedrive_native(
    df=your_leads_dataframe,
    output_path='leads_for_pipedrive.xlsx',
    pipeline_id=14,
    stage_name='lead'
)
```

## Kolommen

| Kolom | Beschrijving |
|-------|--------------|
| Deal - Title | Auto-gegenereerd: "{Company} - Corporate Recruiter" |
| Deal - Owner | Wouter Arts (default) |
| Deal - Pipeline | Pipeline 14 |
| Deal - Stage | lead |
| Deal - Value | 15000 EUR |
| Organization - Name | Bedrijfsnaam |
| Person - Name | Volledige naam contact |
| Person - Email | Email adres |
| Person - Phone | Telefoonnummer |
| Note | HTML-geformatteerde notities |

## Import in Pipedrive

1. Open Pipedrive → Instellingen → Import data
2. Kies "Import from spreadsheet"
3. Upload het gegenereerde Excel bestand
4. Map de kolommen (auto-detect zou moeten werken)
5. Review en importeer

## Functies

- `export_to_pipedrive_native()` - Export DataFrame naar Pipedrive format
- `create_blank_template()` - Maak lege template
- `split_name()` - Split volledige naam in voor/achternaam
- `generate_note_html()` - Genereer HTML notities
