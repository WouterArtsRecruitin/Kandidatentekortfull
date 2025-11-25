#!/bin/bash

# Nederlandse Vacature Optimizer - Automated Netlify Deploy
echo "🚀 Deploying Nederlandse Vacature Optimizer MVP..."

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Create a manual deployment
echo "📦 Creating deployment package..."

# Deploy using manual method (no interactive prompts)
echo "🌍 Deploying to Netlify..."
netlify deploy --dir=. --open

echo "✅ Deployment initiated!"
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo "1. Copy the deployment URL from above"
echo "2. Go to Netlify dashboard to:"
echo "   - Set production domain"
echo "   - Add CLAUDE_API_KEY environment variable"
echo "   - Configure custom domain (optional)"
echo ""
echo "🔧 Environment Variables Needed:"
echo "   CLAUDE_API_KEY=your_actual_claude_api_key"
echo "   NODE_ENV=production"
echo ""
echo "🎉 Nederlandse Vacature Optimizer MVP ready for launch!"