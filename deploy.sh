#!/bin/bash
# Kandidatentekort Deploy Script

set -e

echo "🔨 Building..."
npm run build

echo "🚀 Deploying to Netlify..."
netlify deploy --prod --dir=build

echo "✅ Done! Site live at https://kandidatentekort.nl"
