# Kandidatentekort Auto - Deployment Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
export CLAUDE_API_KEY="your_claude_api_key_here"
export PIPEDRIVE_API_KEY="your_pipedrive_key_here"  # Optional
export SMTP_HOST="smtp.gmail.com"                    # Optional
export SMTP_PORT="587"                               # Optional
export SMTP_USER="your_email@gmail.com"              # Optional
export SMTP_PASSWORD="your_app_password"             # Optional
```

### 3. Test the Script
```bash
python kandidatentekort_auto.py test
```

Expected output:
```
Detected Sector: manufacturing (confidence: 80%)
Test Score: 7.8/10
Sector: Manufacturing
Success: True
```

### 4. Start the Server
```bash
python kandidatentekort_auto.py server
```

Or with production WSGI server:
```bash
gunicorn kandidatentekort_auto:create_app() -b 0.0.0.0:5000
```

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/health
```

### Analyze Vacancy
```bash
curl -X POST http://localhost:5000/webhook/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "vacature_text": "Quality Manager voor manufacturing bedrijf...",
    "bedrijf_naam": "Test Company BV",
    "functie_titel": "Quality Manager",
    "email": "contact@example.com"
  }'
```

### Quick Sector Detection
```bash
curl -X POST http://localhost:5000/api/sector-detect \
  -H "Content-Type: application/json" \
  -d '{"text": "PLC programmeur voor automation project..."}'
```

## Sector Detection

The script automatically detects these technical sectors:

| Sector | Keywords | Score Range |
|--------|----------|-------------|
| Oil & Gas | oil, gas, petrochemical, refinery, offshore | 28-38/100 |
| Manufacturing | manufacturing, productie, quality, lean | 35-45/100 |
| Automation | automation, plc, scada, control, robotics | 32-42/100 |
| Renewable Energy | renewable, wind, solar, sustainable | 30-40/100 |
| Construction | construction, civil, infrastructure, bouw | 25-35/100 |

## Email Subject Examples

Based on score and sector, emails get dynamic subjects:

- Oil & Gas: "Je Oil & Gas vacature: 45% meer gekwalificeerde sollicitaties mogelijk"
- Manufacturing: "Je Manufacturing vacature: 32% meer sollicitaties mogelijk"
- Automation: "Je Automation vacature: 28% meer technische kandidaten mogelijk"

## Monitoring

Check logs for successful analyses:
```bash
tail -f /var/log/kandidatentekort.log

# Expected output:
# 2024-XX-XX - INFO - Detected sector: manufacturing (confidence: 0.85)
# 2024-XX-XX - INFO - Success! Score: 7.8/10 | Sector: manufacturing | Time: 2.34s
```

## Success Indicators

**GREEN LIGHTS:**
- Scores 7.0+ instead of 4.2
- Sector detection works (manufacturing/oil_gas/etc)
- Email subjects have sector + improvement %
- Zero errors in logs

**RED FLAGS (rollback immediately):**
- API errors
- Scores still <5.0
- Email delivery fails

## Systemd Service (Production)

Create `/etc/systemd/system/kandidatentekort.service`:

```ini
[Unit]
Description=Kandidatentekort Auto Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/project
Environment="CLAUDE_API_KEY=your_key"
Environment="PIPEDRIVE_API_KEY=your_key"
ExecStart=/usr/bin/python3 kandidatentekort_auto.py server
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable kandidatentekort
sudo systemctl start kandidatentekort
```

## Expected Results (within 24 hours)

- **Average score:** 4.2 -> 7.8/10
- **Email subject:** Dynamic with sector + improvement %
- **Analysis quality:** Sector-specific insights instead of generic feedback
- **Pipedrive leads:** Better quality with sector tags
