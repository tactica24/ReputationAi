#!/usr/bin/env bash
# smart-vercel-deploy.sh
# Smart script to build, verify, and deploy a Vite frontend to Vercel, with environment and config checks

set -e

FRONTEND_DIR="frontend"
DIST_DIR="$FRONTEND_DIR/dist"
VERCEL_JSON="$FRONTEND_DIR/vercel.json"
ENV_FILE="$FRONTEND_DIR/.env"
ENV_LOCAL_FILE="$FRONTEND_DIR/.env.local"

# 1. Check required directories and files
if [ ! -d "$FRONTEND_DIR" ]; then
  echo "Error: $FRONTEND_DIR directory not found."
  exit 1
fi
if [ ! -f "$FRONTEND_DIR/package.json" ]; then
  echo "Error: package.json not found in $FRONTEND_DIR."
  exit 1
fi

# 2. Check Vercel config for correct output directory
if grep -q '"outputDirectory":' "$VERCEL_JSON"; then
  OUTDIR=$(grep '"outputDirectory":' "$VERCEL_JSON" | sed -E 's/.*"outputDirectory":\s*"([^"]+)".*/\1/')
  if [ "$OUTDIR" != "frontend/dist" ]; then
    echo "Warning: outputDirectory in vercel.json is '$OUTDIR', expected 'frontend/dist'."
  fi
else
  echo "Warning: outputDirectory not set in vercel.json."
fi

# 3. Check for .env and .env.local
if [ ! -f "$ENV_FILE" ] && [ ! -f "$ENV_LOCAL_FILE" ]; then
  echo "Warning: No .env or .env.local found in $FRONTEND_DIR."
fi

# 4. Build the frontend
cd "$FRONTEND_DIR"
echo "Installing dependencies..."
npm install

echo "Building frontend..."
npm run build

# 5. Verify build output
if [ ! -f "$DIST_DIR/index.html" ]; then
  echo "Error: Build failed, dist/index.html not found."
  exit 1
fi
if [ ! -d "$DIST_DIR/assets" ]; then
  echo "Error: Build failed, dist/assets directory not found."
  exit 1
fi

# 6. Deploy to Vercel
if ! command -v vercel &> /dev/null; then
  echo "Vercel CLI not found. Installing..."
  npm install -g vercel
fi

echo "Deploying to Vercel (production)..."
npx vercel --prod --yes

# 7. Output deployment info
echo "Deployment complete. Visit your Vercel dashboard to verify environment variables and routing config."
