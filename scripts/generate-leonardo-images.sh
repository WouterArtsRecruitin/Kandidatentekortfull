#!/bin/bash
# Leonardo AI Image Generation Script voor Kandidatentekort.nl
# ============================================================

LEONARDO_API_KEY="66040566-3292-45dc-b297-df243c9ea0be"
OUTPUT_DIR="$HOME/Kandidatentekortfull/assets/generated-images"

# Maak output directory
mkdir -p "$OUTPUT_DIR"

echo "🎨 Leonardo AI Image Generator - Kandidatentekort.nl"
echo "===================================================="

# Test API connectie
echo "Testing API connection..."
ME_RESPONSE=$(curl -s -X GET "https://cloud.leonardo.ai/api/rest/v1/me" \
  -H "Authorization: Bearer $LEONARDO_API_KEY" \
  -H "Content-Type: application/json")

echo "Account info: $ME_RESPONSE"
echo ""

# Functie om afbeelding te genereren
generate_image() {
    local PROMPT="$1"
    local NEGATIVE="$2"
    local NAME="$3"

    echo "🖼️  Generating: $NAME"

    # Start generation
    RESPONSE=$(curl -s -X POST "https://cloud.leonardo.ai/api/rest/v1/generations" \
      -H "Authorization: Bearer $LEONARDO_API_KEY" \
      -H "Content-Type: application/json" \
      -d "{
        \"prompt\": \"$PROMPT\",
        \"negative_prompt\": \"$NEGATIVE\",
        \"modelId\": \"6bef9f1b-29cb-40c7-b9df-32b51c1f67d3\",
        \"width\": 1024,
        \"height\": 1024,
        \"num_images\": 4,
        \"guidance_scale\": 7,
        \"num_inference_steps\": 50,
        \"presetStyle\": \"CINEMATIC\"
      }")

    # Extract generation ID
    GEN_ID=$(echo $RESPONSE | jq -r '.sdGenerationJob.generationId')

    if [ "$GEN_ID" != "null" ] && [ -n "$GEN_ID" ]; then
        echo "   Generation ID: $GEN_ID"
        echo "   Waiting for completion..."

        # Wait for generation
        sleep 30

        # Get results
        RESULT=$(curl -s -X GET "https://cloud.leonardo.ai/api/rest/v1/generations/$GEN_ID" \
          -H "Authorization: Bearer $LEONARDO_API_KEY" \
          -H "Content-Type: application/json")

        echo "   ✅ Complete! Downloading images..."

        # Download images
        echo $RESULT | jq -r '.generations_by_pk.generated_images[].url' | while read URL; do
            if [ -n "$URL" ] && [ "$URL" != "null" ]; then
                FILENAME="${NAME}_$(date +%s)_$RANDOM.png"
                curl -s -o "$OUTPUT_DIR/$FILENAME" "$URL"
                echo "   📥 Saved: $FILENAME"
            fi
        done
    else
        echo "   ❌ Error: $RESPONSE"
    fi

    echo ""
}

# Negative prompt (voor alle generaties)
NEGATIVE="low quality, blurry, pixelated, distorted faces, extra limbs, bad anatomy, watermark, text, logo overlay, stock photo watermark, shutterstock, istock, clipart, cartoon, anime, illustration style, painting, artificial looking, fake smile, uncomfortable pose, empty office, messy unprofessional, dark gloomy lighting, sad depressing mood"

# ============================================================
# CAMPAGNE 1: VOOR/NA SPLIT SCREEN
# ============================================================

echo "📢 CAMPAGNE 1: Voor/Na Split Screen"
generate_image \
"Professional split-screen comparison design, left side showing frustrated HR manager looking at laptop with red X marks and declining graph, right side showing same person smiling with green checkmarks and rising graph, modern Dutch office environment, clean white background with orange accent elements, minimalist corporate design, before and after transformation concept, professional photography style, bright natural lighting, business casual attire, laptop showing job posting interface, high contrast between negative and positive sides, 4K quality, advertising photography" \
"$NEGATIVE" \
"voorna_splitscreen"

# ============================================================
# CAMPAGNE 2: STATISTIEK STOPPER
# ============================================================

echo "📢 CAMPAGNE 2: Statistiek Stopper"
generate_image \
"Minimalist professional design with large bold typography space, shocked Dutch HR professional looking at laptop screen, modern Amsterdam office background softly blurred, person wearing business casual in orange and navy color scheme, dramatic lighting highlighting facial expression of surprise, clean composition with negative space for text overlay, professional advertising photography, authentic emotion captured, high-end corporate campaign style, suitable for statistics overlay" \
"$NEGATIVE" \
"statistiek_stopper"

# ============================================================
# CAMPAGNE 3: SUCCESS CELEBRATION
# ============================================================

echo "📢 CAMPAGNE 3: Success Celebration"
generate_image \
"Happy Dutch HR manager celebrating at desk with arms raised, laptop showing positive recruitment metrics and green success indicators, modern Nederlandse office with large windows and natural light, colleague giving thumbs up in background, authentic joy and achievement emotion, business casual professional attire with orange accent scarf or tie, clean organized workspace, corporate success story photography, warm lighting, genuine celebration moment captured" \
"$NEGATIVE" \
"success_celebration"

# ============================================================
# CAMPAGNE 4: PRODUCT DEMO
# ============================================================

echo "📢 CAMPAGNE 4: Product Demo"
generate_image \
"Over-the-shoulder view of Dutch professional using recruitment optimization tool on laptop, screen showing clear vacancy analysis interface with orange score indicators and improvement suggestions, modern minimalist desk setup, persons hands on keyboard, coffee cup with orange accent nearby, shallow depth of field focusing on screen content, professional product photography style, clean workspace aesthetic, natural daylight from window, authentic user experience moment" \
"$NEGATIVE" \
"product_demo"

# ============================================================
# CAMPAGNE 5: PAIN POINT - EMPTY INBOX
# ============================================================

echo "📢 CAMPAGNE 5: Pain Point - Empty Inbox"
generate_image \
"Frustrated Dutch HR professional staring at empty email inbox on laptop screen, zero nieuwe sollicitaties concept, modern office environment, person with hand on forehead showing stress, cold blue lighting emphasizing frustration, vacancy posting visible as browser tab, authentic disappointment emotion, professional corporate photography, clean composition with space for text overlay, Nederlandse workplace setting" \
"$NEGATIVE" \
"painpoint_emptyinbox"

# ============================================================
echo ""
echo "🎉 ALLE GENERATIES VOLTOOID!"
echo "📁 Output directory: $OUTPUT_DIR"
echo ""
ls -la "$OUTPUT_DIR"
