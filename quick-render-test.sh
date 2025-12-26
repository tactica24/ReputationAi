#!/bin/bash

# Quick Render Deployment Test
echo "🔍 Quick Render Service Test"
echo "=============================="
echo ""

URL="https://reputationai-backend.onrender.com"

# Test 1: Service availability
echo "1. Testing service availability..."
if curl -s -m 5 "$URL/health" > /dev/null 2>&1; then
    echo "   ✅ Service is ONLINE"
    curl -s -m 5 "$URL/health" | jq '.'
else
    echo "   ❌ Service is OFFLINE or unreachable"
    echo "   Note: Free tier services sleep after 15 min of inactivity"
    echo "   First request may take 30-60 seconds to wake up"
    exit 1
fi

echo ""

# Test 2: API Documentation
echo "2. Testing API documentation..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -m 5 "$URL/api/docs")
if [ "$STATUS" == "200" ]; then
    echo "   ✅ API docs available at: $URL/api/docs"
else
    echo "   ❌ API docs not accessible (HTTP $STATUS)"
fi

echo ""

# Test 3: Authentication endpoint
echo "3. Testing authentication endpoint..."
RESPONSE=$(curl -s -m 10 -X POST "$URL/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@reputation.ai","password":"Admin@2024!"}')

if echo "$RESPONSE" | jq -e '.access_token' > /dev/null 2>&1; then
    echo "   ✅ Login successful - Database initialized"
    echo "   Token received: $(echo "$RESPONSE" | jq -r '.access_token' | cut -c1-20)..."
elif echo "$RESPONSE" | grep -q "Invalid email or password"; then
    echo "   ⚠️  Login failed - Database needs initialization"
    echo "   Action required: Run database initialization in Render shell"
elif echo "$RESPONSE" | grep -q "detail"; then
    echo "   ⚠️  Response: $(echo "$RESPONSE" | jq -r '.detail')"
else
    echo "   ❌ Unexpected response: $RESPONSE"
fi

echo ""
echo "=============================="
echo "📊 Summary:"
echo "   Service URL: $URL"
echo "   API Docs: $URL/api/docs"
echo "   Dashboard: https://dashboard.render.com"
echo ""
