#!/bin/bash

# 🔍 Render Deployment Health Check Script
# Comprehensive testing of deployed backend service

echo "🔍 ReputationAI - Render Deployment Health Check"
echo "================================================="
echo ""

# Configuration
RENDER_URL="https://reputationai-backend.onrender.com"
TIMEOUT=30

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper function for checking endpoints
check_endpoint() {
    local endpoint=$1
    local description=$2
    local expected_code=${3:-200}
    
    echo -n "Testing: $description... "
    
    response=$(curl -s -w "\n%{http_code}" --connect-timeout $TIMEOUT --max-time $TIMEOUT "$RENDER_URL$endpoint" 2>&1)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" == "$expected_code" ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
        echo "   Response: $(echo "$body" | jq -c '.' 2>/dev/null || echo "$body" | head -c 100)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (Expected $expected_code, got $http_code)"
        if [ ! -z "$body" ]; then
            echo "   Error: $(echo "$body" | head -c 200)"
        fi
        return 1
    fi
}

# Check if service is reachable
echo "1️⃣  Checking if Render service is reachable..."
echo "   URL: $RENDER_URL"
echo ""

if ! curl -s --connect-timeout 5 --max-time 10 "$RENDER_URL" > /dev/null 2>&1; then
    echo -e "${RED}❌ Cannot reach Render service${NC}"
    echo ""
    echo "Possible issues:"
    echo "  • Service may not be deployed yet"
    echo "  • Service may be sleeping (free tier spins down after 15 min)"
    echo "  • Network connectivity issue"
    echo ""
    echo "🔧 Solutions:"
    echo "  1. Check Render dashboard: https://dashboard.render.com"
    echo "  2. Verify service is 'Live' (not 'Suspended' or 'Failed')"
    echo "  3. Wait ~30 seconds for free tier to wake up"
    echo "  4. Check deployment logs for errors"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Service is reachable${NC}"
echo ""

# Test health endpoints
echo "2️⃣  Testing Health Endpoints..."
echo ""

check_endpoint "/health" "Root health check"
check_endpoint "/api/v1/health" "API health check"

echo ""

# Test API documentation
echo "3️⃣  Testing API Documentation..."
echo ""

check_endpoint "/api/docs" "Swagger UI documentation"
check_endpoint "/api/redoc" "ReDoc documentation"

echo ""

# Test authentication endpoints
echo "4️⃣  Testing Authentication Endpoints..."
echo ""

# Test login endpoint structure (should return 422 without proper data)
echo -n "Testing: Login endpoint structure... "
response=$(curl -s -w "\n%{http_code}" --connect-timeout $TIMEOUT \
    -X POST "$RENDER_URL/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    2>&1)
http_code=$(echo "$response" | tail -n1)

if [ "$http_code" == "422" ] || [ "$http_code" == "400" ]; then
    echo -e "${GREEN}✅ PASS${NC} (Endpoint exists, validation working)"
else
    echo -e "${YELLOW}⚠️  UNEXPECTED${NC} (HTTP $http_code)"
fi

echo ""

# Test protected endpoints
echo "5️⃣  Testing Protected Endpoints (should require auth)..."
echo ""

endpoints=(
    "/api/v1/entities"
    "/api/v1/monitoring/alerts"
    "/api/v1/analytics/overview"
)

for endpoint in "${endpoints[@]}"; do
    echo -n "Testing: $endpoint... "
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout $TIMEOUT "$RENDER_URL$endpoint" 2>&1)
    
    if [ "$http_code" == "401" ] || [ "$http_code" == "403" ]; then
        echo -e "${GREEN}✅ PASS${NC} (Protected - requires auth)"
    elif [ "$http_code" == "404" ]; then
        echo -e "${YELLOW}⚠️  NOT FOUND${NC} (Endpoint may not be implemented)"
    else
        echo -e "${RED}❌ UNEXPECTED${NC} (HTTP $http_code - should require auth)"
    fi
done

echo ""

# Test database connectivity
echo "6️⃣  Testing Database Connectivity..."
echo ""

health_response=$(curl -s --connect-timeout $TIMEOUT "$RENDER_URL/api/v1/health" 2>&1)
db_status=$(echo "$health_response" | jq -r '.database.connected // .database // "unknown"' 2>/dev/null)

if [ "$db_status" == "true" ] || echo "$health_response" | grep -q "database.*true"; then
    echo -e "${GREEN}✅ Database connected${NC}"
elif [ "$db_status" == "false" ] || echo "$health_response" | grep -q "database.*false"; then
    echo -e "${RED}❌ Database connection failed${NC}"
    echo "   Check DATABASE_URL environment variable in Render"
else
    echo -e "${YELLOW}⚠️  Cannot determine database status${NC}"
    echo "   Response: $health_response"
fi

echo ""

# Check environment variables
echo "7️⃣  Environment Configuration Check..."
echo ""

echo "Required environment variables in Render:"
echo "  • DATABASE_URL (from reputationai-db)"
echo "  • SECRET_KEY (auto-generated)"
echo "  • JWT_SECRET_KEY (auto-generated)"
echo "  • ENVIRONMENT=production"
echo "  • CORS_ORIGINS (frontend URLs)"
echo ""
echo "To verify, check: https://dashboard.render.com → reputationai-backend → Environment"
echo ""

# Summary
echo "================================================="
echo "📊 Health Check Summary"
echo "================================================="
echo ""
echo "Service Status: ${GREEN}ONLINE${NC}"
echo "Service URL: $RENDER_URL"
echo "Dashboard: https://dashboard.render.com"
echo ""
echo "Next Steps:"
echo "  1. ✅ Service is deployed and responding"
echo "  2. 🔐 Test login with: admin@reputation.ai / Admin@2024!"
echo "  3. 📊 Check logs in Render dashboard for any errors"
echo "  4. 🗄️  Initialize database if needed (run init_production_db.py)"
echo "  5. 🌐 Update frontend to use: $RENDER_URL"
echo ""
echo "📖 Full deployment guide: RENDER_DEPLOYMENT.md"
echo ""
