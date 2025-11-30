/**
 * Pipedrive Setup Script voor Pipeline 14: Corporate Recruiter Vacatures
 *
 * Dit script configureert:
 * 1. Pipeline met 14 stages
 * 2. Custom fields (Deal + Organization)
 * 3. Email templates via Mail Templates API
 *
 * Gebruik:
 * 1. npm install node-fetch
 * 2. PIPEDRIVE_API_TOKEN=xxx node setup-pipedrive.js
 */

const PIPEDRIVE_API_TOKEN = process.env.PIPEDRIVE_API_TOKEN;
const PIPEDRIVE_DOMAIN = process.env.PIPEDRIVE_DOMAIN || 'api.pipedrive.com';
const BASE_URL = `https://${PIPEDRIVE_DOMAIN}/v1`;

if (!PIPEDRIVE_API_TOKEN) {
  console.error('❌ PIPEDRIVE_API_TOKEN environment variable is required');
  console.log('\nGebruik: PIPEDRIVE_API_TOKEN=xxx node setup-pipedrive.js');
  process.exit(1);
}

// =============================================================================
// EMAIL TEMPLATES
// =============================================================================

const EMAIL_TEMPLATES = [
  {
    name: 'E1 - The Opener',
    subject_a: '{{first_name}}, snelle vraag over jullie recruiter vacature',
    subject_b: 'Die 45 dagen...',
    content: `Hoi {{first_name}},

Jullie recruiter vacature staat nu {{days_open}} dagen open.

Dat is niet gek. In Nederland staan op dit moment 1.000+ recruiter vacatures open op Indeed alleen al. In jullie regio ({{region}}) zijn dat er 100+.

De gemiddelde time-to-fill voor recruiters: 45 dagen.
(Bron: Intelligence Group 2024)

Maar hier zit de ironie:

Jullie hebben een recruiter nodig om mensen te werven.
Om die recruiter te vinden, heb je recruitment expertise nodig.
Die expertise willen jullie juist inhuren.

Ik help bedrijven zoals {{company}} die cirkel doorbreken.

Eén vraag: Hoeveel serieuze sollicitaties hebben jullie tot nu toe ontvangen?

Groet,
Wouter`
  },
  {
    name: 'E2 - The Follow-up',
    subject: 'Re: {{previous_subject}}',
    content: `Hoi {{first_name}},

Korte follow-up.

Ik besefte dat ik in mijn vorige mail alleen het probleem schetste.
Hier is wat context over hoe ik dit aanpak:

Vorige maand heb ik voor een bedrijf in {{industry}} hun recruiter vacature ingevuld in 18 dagen. Niet 45.

Verschil:
→ Niet wachten op Indeed sollicitaties
→ Direct benaderen van recruiters die niet actief zoeken
→ Mijn netwerk van 2.500+ recruitment professionals in Nederland

Jullie vacature staat nu {{days_open_updated}} dagen open.

Als je nieuwsgierig bent hoe ik dat aanpak voor {{company}}, dan hoor ik het graag.

Wouter

PS: Geen druk. Als de timing niet goed is, snap ik dat. Maar als jullie over 2 weken nog zoeken, dan hebben we een gesprek nodig.`
  },
  {
    name: 'E3 - The Value Drop',
    subject: 'Re: {{previous_subject}}',
    content: `{{first_name}},

Geen verkooppraatje dit keer. Gewoon iets nuttigs.

Ik heb een checklist gemaakt die ik gebruik om recruiter vacatureteksten te optimaliseren. Dezelfde die ik voor klanten gebruik.

3 dingen die bijna elke recruiter vacature mist:

1. Concrete omzetverantwoordelijkheid (niet "bijdragen aan groei")
2. Tech stack specificatie (ATS, sourcing tools, LinkedIn Recruiter)
3. Salary range (ja, ook voor recruiters - 63% haakt af zonder)

De bedrijven die deze 3 toevoegen zien gemiddeld 2.4x meer sollicitaties.
(Eigen data, 47 vacatures geanalyseerd in 2024)

Als je wilt, stuur ik je mijn volledige checklist. Gratis, geen catch.

Reply "JA" en ik stuur hem door.

Wouter`
  },
  {
    name: 'E4 - The Social Proof',
    subject: 'Re: {{previous_subject}}',
    content: `{{first_name}},

Ik deel niet vaak klantresultaten via email, maar dit is relevant voor jullie situatie.

Vorige maand - vergelijkbaar scenario:

Bedrijf: Scale-up in {{industry}}, 80 medewerkers
Probleem: Senior Recruiter vacature, 6 weken open, 4 sollicitaties (geen match)
Aanpak: Mijn netwerk + directe benadering passieve kandidaten
Resultaat: 3 sterke kandidaten binnen 12 dagen, aangenomen na 18 dagen

Quote van de HR Director:
"We hadden zelf nog maanden kunnen zoeken. Wouter had binnen 2 weken kandidaten die wij nooit hadden gevonden."

Jullie vacature staat nu {{days_open_updated}} dagen open.

Ik garandeer niet dezelfde snelheid - elke situatie is anders. Maar ik kan wel vertellen wat realistisch is voor {{company}}.

15 minuten. Geen pitch, gewoon eerlijk advies.

Interesse?

Wouter`
  },
  {
    name: 'E5 - The Reality Check',
    subject: '{{first_name}}, wat kost jullie lege recruiter stoel?',
    content: `{{first_name}},

Even een rekensommetje.

Jullie recruiter vacature staat nu {{days_open_updated}} dagen open.

Wat kost dat?

Stel: die recruiter had 2 vacatures per maand kunnen invullen.
Gemiddelde time-to-fill besparing: 20 dagen per vacature.
Gemiddeld salaris openstaande posities: €60.000/jaar.

Kosten per dag dat een vacature onvervuld is: €164/dag
(Bron: SHRM, aangepast naar NL markt)

2 vacatures × 20 dagen × €164 = €6.560/maand

Jullie missen nu al {{days_open_updated}} dagen × (indirect: €6.560/30) = €{{calculated_cost}} aan recruitment capaciteit.

En dat is conservatief gerekend.

Ik snap dat dit geen prettige email is. Maar iemand moet het zeggen.

Als je wilt sparren over hoe dit sneller kan, reply gewoon met "BELLEN".

Wouter

PS: Geen recruitment fee nodig om te praten. Eerste gesprek is altijd vrijblijvend.`
  },
  {
    name: 'E6 - The Breakup',
    subject: 'Re: {{previous_subject}}',
    content: `{{first_name}},

Dit is mijn laatste mail over jullie recruiter vacature.

Ik heb je 5x gemaild de afgelopen 6 weken. Geen reactie.

Dat kan drie dingen betekenen:

1. Jullie hebben de vacature al ingevuld → Gefeliciteerd! 🎉
2. De timing is niet goed → Snap ik. Hou mijn gegevens voor later.
3. Ik ben niet de juiste partij → Ook prima. Hopelijk vinden jullie snel de juiste.

Hoe dan ook: ik stop met mailen.

Als er ooit een moment komt dat jullie wél hulp nodig hebben bij recruitment posities, dan weet je me te vinden.

Succes met de search.

Wouter

PS: Reply "LATER" als je wilt dat ik over 3 maanden nog eens check. Geen probleem.`
  },
  {
    name: 'E7 - The Resurrection',
    subject: '{{first_name}}, nog steeds aan het zoeken?',
    content: `{{first_name}},

3 maanden geleden mailde ik je over jullie recruiter vacature.

Ik check even in:

□ Ingevuld? → Top, negeer deze mail
□ Nog open? → Dan hebben we iets te bespreken
□ Nieuwe vacature? → Laat me weten, ik help graag

Sinds mijn laatste mail heb ik 7 recruiter posities ingevuld voor bedrijven in {{region}}.

Gemiddelde time-to-fill: 21 dagen.
Gemiddelde fee: €7.990 (no cure, no pay).

Als jullie nog zoeken, stuur ik je graag 2-3 profielen. Vrijblijvend, zodat je ziet wat ik kan leveren.

Interesse?

Wouter`
  }
];

// =============================================================================
// PIPELINE STAGES
// =============================================================================

const PIPELINE_STAGES = [
  { name: 'New Lead', order_nr: 1 },
  { name: 'Email 1 Sent', order_nr: 2 },
  { name: 'Email 2 Sent', order_nr: 3 },
  { name: 'Email 3 Sent', order_nr: 4 },
  { name: 'Email 4 Sent', order_nr: 5 },
  { name: 'Email 5 Sent', order_nr: 6 },
  { name: 'Email 6 Sent (Breakup)', order_nr: 7 },
  { name: 'Replied - Positive', order_nr: 8 },
  { name: 'Replied - Negative', order_nr: 9 },
  { name: 'Call Scheduled', order_nr: 10 },
  { name: 'Meeting Done', order_nr: 11 },
  { name: 'Proposal Sent', order_nr: 12 },
  { name: 'Won', order_nr: 13 },
  { name: 'Lost', order_nr: 14 }
];

// =============================================================================
// CUSTOM FIELDS
// =============================================================================

const DEAL_FIELDS = [
  {
    name: 'Email Sequence Stage',
    field_type: 'enum',
    options: ['Pending', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'Replied', 'Stopped']
  },
  {
    name: 'Days Open',
    field_type: 'double'
  },
  {
    name: 'Import Date',
    field_type: 'date'
  },
  {
    name: 'Last Email Sent',
    field_type: 'date'
  },
  {
    name: 'Reply Sentiment',
    field_type: 'enum',
    options: ['None', 'Positive', 'Negative', 'Neutral']
  },
  {
    name: 'Vacature URL',
    field_type: 'varchar'
  },
  {
    name: 'Subject Variant',
    field_type: 'enum',
    options: ['A', 'B']
  },
  {
    name: 'Gmail Thread ID',
    field_type: 'varchar'
  }
];

const ORG_FIELDS = [
  {
    name: 'Sector',
    field_type: 'varchar'
  },
  {
    name: 'Region',
    field_type: 'enum',
    options: ['Gelderland', 'Overijssel', 'Noord-Brabant', 'Zuid-Holland', 'Noord-Holland', 'Utrecht', 'Other']
  }
];

// =============================================================================
// API HELPERS
// =============================================================================

async function apiRequest(endpoint, method = 'GET', body = null) {
  const url = `${BASE_URL}${endpoint}?api_token=${PIPEDRIVE_API_TOKEN}`;

  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  const data = await response.json();

  if (!data.success) {
    throw new Error(`API Error: ${JSON.stringify(data.error || data)}`);
  }

  return data;
}

// =============================================================================
// SETUP FUNCTIONS
// =============================================================================

async function createPipeline() {
  console.log('\n📊 Creating Pipeline...');

  try {
    const result = await apiRequest('/pipelines', 'POST', {
      name: 'Recruiter Vacature Outreach',
      deal_probability: 1,
      order_nr: 1,
      active: true
    });

    const pipelineId = result.data.id;
    console.log(`✅ Pipeline created with ID: ${pipelineId}`);

    return pipelineId;
  } catch (error) {
    // Pipeline might already exist, try to find it
    console.log('⚠️  Pipeline might already exist, searching...');
    const pipelines = await apiRequest('/pipelines');
    const existing = pipelines.data.find(p => p.name === 'Recruiter Vacature Outreach');

    if (existing) {
      console.log(`✅ Found existing pipeline with ID: ${existing.id}`);
      return existing.id;
    }

    throw error;
  }
}

async function createStages(pipelineId) {
  console.log('\n📋 Creating Pipeline Stages...');

  for (const stage of PIPELINE_STAGES) {
    try {
      await apiRequest('/stages', 'POST', {
        name: stage.name,
        pipeline_id: pipelineId,
        order_nr: stage.order_nr
      });
      console.log(`  ✅ Stage: ${stage.name}`);
    } catch (error) {
      console.log(`  ⚠️  Stage "${stage.name}" might already exist`);
    }
  }
}

async function createDealFields() {
  console.log('\n🏷️  Creating Deal Custom Fields...');

  const createdFields = {};

  for (const field of DEAL_FIELDS) {
    try {
      const body = {
        name: field.name,
        field_type: field.field_type
      };

      if (field.options) {
        body.options = field.options.map(opt => ({ label: opt }));
      }

      const result = await apiRequest('/dealFields', 'POST', body);
      createdFields[field.name] = result.data.key;
      console.log(`  ✅ Field: ${field.name} (key: ${result.data.key})`);
    } catch (error) {
      console.log(`  ⚠️  Field "${field.name}" might already exist`);
    }
  }

  return createdFields;
}

async function createOrgFields() {
  console.log('\n🏢 Creating Organization Custom Fields...');

  const createdFields = {};

  for (const field of ORG_FIELDS) {
    try {
      const body = {
        name: field.name,
        field_type: field.field_type
      };

      if (field.options) {
        body.options = field.options.map(opt => ({ label: opt }));
      }

      const result = await apiRequest('/organizationFields', 'POST', body);
      createdFields[field.name] = result.data.key;
      console.log(`  ✅ Field: ${field.name} (key: ${result.data.key})`);
    } catch (error) {
      console.log(`  ⚠️  Field "${field.name}" might already exist`);
    }
  }

  return createdFields;
}

async function createEmailTemplates() {
  console.log('\n✉️  Creating Email Templates (Mail Templates)...');

  // Note: Pipedrive Mail Templates API requires Campaigns add-on
  // We'll create them if the API is available, otherwise output for manual creation

  const templates = [];

  for (const template of EMAIL_TEMPLATES) {
    try {
      const result = await apiRequest('/mailbox/mailTemplates', 'POST', {
        name: template.name,
        subject: template.subject_a || template.subject,
        content: template.content
      });

      templates.push({
        name: template.name,
        id: result.data.id
      });
      console.log(`  ✅ Template: ${template.name}`);
    } catch (error) {
      console.log(`  ⚠️  Could not create "${template.name}" via API`);
      console.log(`     → Create manually in Pipedrive > Mail > Templates`);
    }
  }

  return templates;
}

async function getExistingFields() {
  console.log('\n🔍 Fetching existing field keys...');

  const dealFieldsResult = await apiRequest('/dealFields');
  const orgFieldsResult = await apiRequest('/organizationFields');

  const dealFields = {};
  const orgFields = {};

  for (const field of dealFieldsResult.data) {
    dealFields[field.name] = field.key;
  }

  for (const field of orgFieldsResult.data) {
    orgFields[field.name] = field.key;
  }

  return { dealFields, orgFields };
}

// =============================================================================
// OUTPUT CONFIG
// =============================================================================

function outputZapierConfig(pipelineId, dealFields, orgFields) {
  console.log('\n' + '='.repeat(60));
  console.log('📋 ZAPIER CONFIGURATIE');
  console.log('='.repeat(60));

  console.log(`
Pipeline ID: ${pipelineId}

Deal Field Keys (voor Zapier):
${Object.entries(dealFields).map(([name, key]) => `  - ${name}: ${key}`).join('\n')}

Organization Field Keys:
${Object.entries(orgFields).map(([name, key]) => `  - ${name}: ${key}`).join('\n')}

Pipedrive Variabelen voor Email Templates:
  {{person.first_name}}     → Voornaam
  {{organization.name}}     → Bedrijfsnaam
  {{deal.${dealFields['Days Open'] || 'days_open'}}}  → Days Open
  {{organization.${orgFields['Region'] || 'region'}}} → Region
  {{organization.${orgFields['Sector'] || 'sector'}}} → Sector/Industry
`);
}

function outputEmailTemplatesForManualCreation() {
  console.log('\n' + '='.repeat(60));
  console.log('✉️  EMAIL TEMPLATES VOOR HANDMATIGE CREATIE');
  console.log('='.repeat(60));
  console.log('\nGa naar: Pipedrive → Mail → Templates → New Template\n');

  for (const template of EMAIL_TEMPLATES) {
    console.log('-'.repeat(40));
    console.log(`📧 ${template.name}`);
    console.log('-'.repeat(40));
    if (template.subject_a) {
      console.log(`Subject (A): ${template.subject_a}`);
      console.log(`Subject (B): ${template.subject_b}`);
    } else {
      console.log(`Subject: ${template.subject}`);
    }
    console.log(`\nBody:\n${template.content}\n`);
  }
}

// =============================================================================
// MAIN
// =============================================================================

async function main() {
  console.log('🚀 Pipedrive Setup Script voor Pipeline 14');
  console.log('=' .repeat(50));

  try {
    // 1. Create Pipeline
    const pipelineId = await createPipeline();

    // 2. Create Stages
    await createStages(pipelineId);

    // 3. Create Custom Fields
    await createDealFields();
    await createOrgFields();

    // 4. Try to create Email Templates
    await createEmailTemplates();

    // 5. Get all field keys for Zapier config
    const { dealFields, orgFields } = await getExistingFields();

    // 6. Output configuration
    outputZapierConfig(pipelineId, dealFields, orgFields);
    outputEmailTemplatesForManualCreation();

    console.log('\n' + '='.repeat(60));
    console.log('✅ SETUP VOLTOOID!');
    console.log('='.repeat(60));
    console.log(`
Volgende stappen:
1. Kopieer de Pipeline ID (${pipelineId}) naar je Zapier zaps
2. Kopieer de Field Keys naar je Zapier field mappings
3. Maak de email templates handmatig aan als ze niet via API zijn aangemaakt
4. Test met 1 lead voordat je opschaalt
`);

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    process.exit(1);
  }
}

main();
