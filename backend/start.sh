#!/bin/bash

# Reputation Guardian Backend Startup Script
# This script helps you quickly start the backend with proper configuration

echo "🛡️ Reputation Guardian Backend Startup"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "⚠️ Please run this script from the backend directory:"
    echo "   cd /workspaces/ReputationAi/backend"
    echo "   ./start.sh"
    exit 1
fi

# Check for .env file
if [ ! -f "../.env" ]; then
    echo "⚠️ .env file not found. Creating from example..."
    if [ -f "../.env.example" ]; then
        cp ../.env.example ../.env
        echo "✅ Created .env file. Please edit it with your configuration:"
        echo "   nano ../.env"
        echo ""
        read -p "Press Enter after you've configured .env, or Ctrl+C to exit..."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check for required Python packages
echo "📦 Checking dependencies..."
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ FastAPI not installed. Installing dependencies..."
    pip install -r ../requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please run manually:"
        echo "   pip install -r ../requirements.txt"
        exit 1
    fi
    echo "✅ Dependencies installed"
fi

# Load environment variables
if [ -f "../.env" ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
fi

# Set defaults if not in .env
export API_HOST=${API_HOST:-0.0.0.0}
export API_PORT=${API_PORT:-8080}

echo ""
echo "🚀 Starting Backend Server..."
echo "   Host: $API_HOST"
echo "   Port: $API_PORT"
echo "   API Docs: http://localhost:$API_PORT/api/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Start the server
python3 -m uvicorn main:app --host $API_HOST --port $API_PORT --reload
