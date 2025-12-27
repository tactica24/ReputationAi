#!/bin/bash

# Test Render Deployment After Auto-Deploy
# Run this after Render finishes deploying

URL="https://reputationai-backend.onrender.com"

echo "🧪 Testing Render Deployment"
echo "=============================="
echo ""

# Give Render time to wake up if sleeping
echo "⏳ Waiting for service to wake up (if needed)..."
sleep 2

# Test 1: Basic health
echo "1️⃣ Testing basic health endpoint..."
HEALTH=$(curl -s -w "\nHTTP:%{http_code}" "$URL/health" 2>/dev/null)
HTTP_CODE=$(echo "$HEALTH" | tail -n1 | cut -d: -f2)

if [ "$HTTP_CODE" == "200" ]; then
    echo "   ✅ Service is online"
    echo "$HEALTH" | head -n-1 | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
else
    echo "   ❌ Service offline (HTTP $HTTP_CODE)"
    exit 1
fi

echo ""

# Test 2: Database health
echo "2️⃣ Testing database health..."
DB_HEALTH=$(curl -s "$URL/api/v1/health" 2>/dev/null)
PG_STATUS=$(echo "$DB_HEALTH" | python3 -c "import sys, json; print(json.load(sys.stdin)['database']['postgresql'])" 2>/dev/null)

if [ "$PG_STATUS" == "True" ]; then
    echo "   ✅ Database connected"
else
    echo "   ⚠️  Database not connected - calling initialization endpoint..."
    echo ""
    echo "3️⃣ Calling /api/v1/system/initialize..."
    INIT_RESULT=$(curl -s -X POST "$URL/api/v1/system/initialize" 2>/dev/null)
    echo "$INIT_RESULT" | python3 -m json.tool 2>/dev/null || echo "$INIT_RESULT"
    echo ""
    sleep 2
fi

# Test 3: Login
echo ""
echo "4️⃣ Testing login..."
LOGIN_RESULT=$(curl -s -X POST "$URL/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@reputation.ai","password":"Admin@2024!"}' 2>/dev/null)

if echo "$LOGIN_RESULT" | grep -q "access_token"; then
    echo "   ✅ Login successful!"
    echo "   Token: $(echo "$LOGIN_RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'][:50])" 2>/dev/null)..."
else
    echo "   ❌ Login failed"
    echo "   Response: $LOGIN_RESULT"
fi

echo ""
echo "=============================="
echo "✅ Test complete!"
echo ""
echo "📊 Summary:"
echo "   Service: $URL"
echo "   Docs: $URL/api/docs"
echo "   Dashboard: https://dashboard.render.com"
