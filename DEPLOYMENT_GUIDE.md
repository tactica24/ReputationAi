# 🚀 Deploy Cost-Optimized MVP - Complete Guide

## Total Cost: $0-$200/month (vs $12,000+/month enterprise version)

---

## 📋 Prerequisites

### Required Accounts (All FREE):

1. **Oracle Cloud** - FREE Forever Tier
   - Sign up: https://www.oracle.com/cloud/free/
   - Get: 4 ARM cores, 24GB RAM, 200GB storage
   - Cost: **$0/month FOREVER**

2. **GitHub** - Free account
   - For version control
   - Cost: **$0**

3. **Free API Keys** (Optional but recommended):
   - Reddit API: https://www.reddit.com/prefs/apps
   - NewsAPI.org: https://newsapi.org/register
   - Google Custom Search: https://developers.google.com/custom-search
   - SendGrid: https://sendgrid.com/free/
   - Cost: **$0**

---

## 🏗️ Step 1: Setup Oracle Cloud Free Tier (30 min)

### 1.1 Create Oracle Cloud Account
```bash
# Go to: https://signup.cloud.oracle.com/
# Fill in details (credit card required but NEVER charged on Free Tier)
# Verify email
```

### 1.2 Create Free VM Instance

1. Login to Oracle Cloud Console
2. Navigate to: Compute → Instances → Create Instance

3. Configure Instance:
   - **Name**: reputation-monitor
   - **Image**: Ubuntu 22.04
   - **Shape**: VM.Standard.A1.Flex (Ampere ARM)
   - **OCPUs**: 4 (max free tier)
   - **Memory**: 24GB (max free tier)
   - **Boot Volume**: 200GB (max free tier)

4. **Network Configuration**:
   - Create new VCN
   - Assign public IP: Yes
   - Select "Assign a public IPv4 address"

5. **SSH Keys**:
   - Generate new key pair
   - Download private key (save as `oracle-key.pem`)

6. Click "Create" - wait 2-3 minutes

### 1.3 Configure Firewall

1. In Oracle Console:
   - Navigate to: Networking → Virtual Cloud Networks
   - Click your VCN
   - Click "Security Lists" → "Default Security List"
   - Click "Add Ingress Rules"

2. Add rules:
   ```
   Source: 0.0.0.0/0
   Protocol: TCP
   Destination Port: 80, 443, 8000
   Description: HTTP/HTTPS/API
   ```

3. Also configure Ubuntu firewall:
   ```bash
   # SSH into your instance first (see below)
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 8000/tcp
   sudo ufw enable
   ```

---

## 🔧 Step 2: Connect to Your Server

### 2.1 SSH Connection

```bash
# On your local machine
chmod 400 oracle-key.pem

# Connect (replace IP with your instance IP)
ssh -i oracle-key.pem ubuntu@YOUR_INSTANCE_IP
```

### 2.2 Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    git \
    nginx \
    postgresql \
    postgresql-contrib \
    redis-server \
    certbot \
    python3-certbot-nginx

# Verify installations
python3 --version  # Should be 3.10+
psql --version
redis-cli --version
```

---

## 💾 Step 3: Setup Database (FREE)

### 3.1 Configure PostgreSQL

```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

# In PostgreSQL console:
CREATE DATABASE reputation_monitor;
CREATE USER repmonitor WITH PASSWORD 'your_secure_password_here';
ALTER ROLE repmonitor SET client_encoding TO 'utf8';
ALTER ROLE repmonitor SET default_transaction_isolation TO 'read committed';
ALTER ROLE repmonitor SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE reputation_monitor TO repmonitor;
\q
```

### 3.2 Configure Redis

```bash
# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis
redis-cli ping  # Should return "PONG"
```

---

## 📦 Step 4: Deploy Application

### 4.1 Clone Repository

```bash
# Create app directory
mkdir -p /home/ubuntu/apps
cd /home/ubuntu/apps

# Clone your repo
git clone https://github.com/tactica24/ReputationAi.git
cd ReputationAi
```

### 4.2 Create Python Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 4.3 Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# If requirements.txt doesn't exist, install manually:
pip install \
    fastapi \
    uvicorn[standard] \
    sqlalchemy \
    psycopg2-binary \
    redis \
    pydantic \
    python-jose[cryptography] \
    passlib[bcrypt] \
    python-multipart \
    aiohttp \
    beautifulsoup4 \
    scrapy \
    selenium \
    praw \
    instaloader \
    feedparser \
    transformers \
    sentence-transformers \
    torch \
    torchvision \
    pillow \
    piexif
```

### 4.4 Download AI Models (One-Time, ~2GB)

```bash
# Run model download script
python3 -c "
from transformers import pipeline
from sentence_transformers import SentenceTransformer

print('Downloading AI models (this will take 5-10 minutes)...')

# Fake news classifier
pipeline('text-classification', model='hamzab/roberta-fake-news-classification')

# Sentiment analyzer
pipeline('sentiment-analysis', model='cardiffnlp/twitter-roberta-base-sentiment-latest')

# Zero-shot classifier
pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Sentence transformer
SentenceTransformer('all-MiniLM-L6-v2')

print('✅ All models downloaded and cached!')
"
```

### 4.5 Configure Environment Variables

```bash
# Create .env file
nano .env

# Add configuration:
DATABASE_URL=postgresql://repmonitor:your_secure_password_here@localhost/reputation_monitor
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-generate-with-openssl-rand-hex-32
DEBUG=False

# API Keys (Optional - get free from respective websites)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
NEWSAPI_KEY=your_newsapi_key
GOOGLE_CSE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_search_engine_id
SENDGRID_API_KEY=your_sendgrid_key

# Save and exit (Ctrl+X, Y, Enter)
```

### 4.6 Initialize Database

```bash
# Run migrations
python3 -m backend.database.init_db

# Or create tables manually:
python3 -c "
from sqlalchemy import create_engine
from backend.database.models import Base
import os

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
print('✅ Database initialized!')
"
```

---

## 🌐 Step 5: Setup NGINX (Reverse Proxy)

### 5.1 Configure NGINX

```bash
# Create NGINX config
sudo nano /etc/nginx/sites-available/reputation-monitor

# Add configuration:
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/ubuntu/apps/ReputationAi/frontend/build/static;
    }
}

# Save and exit
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/reputation-monitor /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart NGINX
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 5.2 Setup SSL Certificate (FREE with Let's Encrypt)

```bash
# Only if you have a domain name
sudo certbot --nginx -d yourdomain.com

# Follow prompts
# Certificate auto-renews every 90 days (FREE)
```

---

## 🚀 Step 6: Run Application

### 6.1 Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/reputation-monitor.service

# Add configuration:
[Unit]
Description=Reputation Monitor API
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/apps/ReputationAi
Environment="PATH=/home/ubuntu/apps/ReputationAi/venv/bin"
ExecStart=/home/ubuntu/apps/ReputationAi/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Save and exit
```

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start reputation-monitor

# Enable on boot
sudo systemctl enable reputation-monitor

# Check status
sudo systemctl status reputation-monitor

# View logs
sudo journalctl -u reputation-monitor -f
```

### 6.2 Setup Celery Worker (Background Tasks)

```bash
# Create Celery service
sudo nano /etc/systemd/system/celery-worker.service

# Add configuration:
[Unit]
Description=Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=ubuntu
WorkingDirectory=/home/ubuntu/apps/ReputationAi
Environment="PATH=/home/ubuntu/apps/ReputationAi/venv/bin"
ExecStart=/home/ubuntu/apps/ReputationAi/venv/bin/celery -A backend.tasks worker --loglevel=info --detach
Restart=always

[Install]
WantedBy=multi-user.target

# Save and exit
```

```bash
# Start Celery
sudo systemctl start celery-worker
sudo systemctl enable celery-worker
```

### 6.3 Setup Cron Jobs (Scheduled Scraping)

```bash
# Edit crontab
crontab -e

# Add scraping schedule:
# Run every 15 minutes during business hours
*/15 6-22 * * * /home/ubuntu/apps/ReputationAi/venv/bin/python /home/ubuntu/apps/ReputationAi/backend/scripts/run_scrapers.py

# Run comprehensive scan once daily at 2 AM
0 2 * * * /home/ubuntu/apps/ReputationAi/venv/bin/python /home/ubuntu/apps/ReputationAi/backend/scripts/daily_scan.py

# Save and exit
```

---

## 📊 Step 7: Setup Monitoring (FREE)

### 7.1 Install Prometheus + Grafana

```bash
# Install Prometheus
cd /tmp
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-arm64.tar.gz
tar xvfz prometheus-*.tar.gz
sudo mv prometheus-2.45.0.linux-arm64 /opt/prometheus
sudo useradd --no-create-home --shell /bin/false prometheus
sudo chown -R prometheus:prometheus /opt/prometheus

# Create systemd service
sudo nano /etc/systemd/system/prometheus.service

# Add basic config
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
ExecStart=/opt/prometheus/prometheus --config.file=/opt/prometheus/prometheus.yml
Restart=always

[Install]
WantedBy=multi-user.target

# Start Prometheus
sudo systemctl start prometheus
sudo systemctl enable prometheus
```

### 7.2 Install Grafana

```bash
# Add Grafana repository
sudo apt-get install -y software-properties-common
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Install
sudo apt-get update
sudo apt-get install -y grafana

# Start Grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

# Access at: http://YOUR_IP:3000
# Default login: admin/admin
```

---

## 🧪 Step 8: Test Everything

### 8.1 Test API

```bash
# Check if API is running
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

### 8.2 Test Scraping

```bash
# Run manual test
cd /home/ubuntu/apps/ReputationAi
source venv/bin/activate

python3 -c "
import asyncio
from backend.services.scraping.free_web_scraper import PublicContentScraper, MonitoringOrchestrator

async def test():
    scraper = PublicContentScraper()
    orchestrator = MonitoringOrchestrator(scraper)
    
    results = await orchestrator.monitor_person(
        person_name='Test Person',
        aliases=[],
        social_handles={},
        keywords=['test']
    )
    
    print(f'✅ Scraping works! Found {len(results)} results')

asyncio.run(test())
"
```

### 8.3 Test AI Detection

```bash
python3 -c "
import asyncio
from backend.services.ai_detection.free_ai_engine import FreeAIDetectionEngine

async def test():
    engine = FreeAIDetectionEngine()
    
    result = await engine.detect_fake_news('This is a test')
    print(f'✅ AI detection works! Confidence: {result.confidence}')

asyncio.run(test())
"
```

---

## 💰 Optional: Add Proxy Service ($50-100/month)

For reliable scraping at scale:

### Option 1: ScraperAPI (Recommended)
```bash
# Sign up: https://www.scraperapi.com/
# Free tier: 1,000 requests/month
# Paid: $49/month for 100K requests

# Add to .env:
SCRAPER_API_KEY=your_key
```

### Option 2: BrightData (Luminati)
```bash
# Sign up: https://brightdata.com/
# Pricing: From $50/month
# Better for high-volume scraping
```

---

## 📈 Monitoring Costs

### Daily Cost Breakdown:

```
Oracle Cloud VM:        $0/month  (Free Tier Forever)
PostgreSQL:             $0/month  (Self-hosted)
Redis:                  $0/month  (Self-hosted)
Nginx:                  $0/month  (Open source)
SSL Certificate:        $0/month  (Let's Encrypt)
AI Models:              $0/month  (HuggingFace free)
News APIs:              $0/month  (Free tiers)
Email (SendGrid):       $0/month  (100/day free)
Monitoring:             $0/month  (Self-hosted Prometheus)
Domain Name:            $1/month  (Optional)
Proxy Service:          $50-100/month (Optional but recommended)
---
TOTAL:                  $51-101/month
```

**vs Enterprise Version: $12,000-163,000/month**

**Savings: 99.2% cost reduction!**

---

## 🎯 Scaling Up

### When to upgrade:

**At 10 clients ($10K-$50K MRR):**
- Current setup handles fine
- Add backup VM: +$12/month
- Better proxies: $100/month
- **Total: $163/month**

**At 50 clients ($50K-$250K MRR):**
- Add second Oracle VM (still free)
- Upgrade to paid Twitter API: +$100/month
- Better proxies: $200/month
- **Total: $300/month**

**At 100+ clients ($100K+ MRR):**
- Consider Twitter Pro API: +$5,000/month
- Add GPT-4 for premium clients: +$2,000/month
- Managed database: +$300/month
- **Total: $7,500/month**

**Still 93% cheaper than starting with enterprise version!**

---

## 🎉 Launch Checklist

- [ ] Oracle Cloud VM running
- [ ] PostgreSQL configured
- [ ] Redis running
- [ ] Application deployed
- [ ] NGINX configured
- [ ] SSL certificate installed (if using domain)
- [ ] Systemd services running
- [ ] Cron jobs scheduled
- [ ] Monitoring setup
- [ ] API keys configured
- [ ] Test scraping working
- [ ] Test AI detection working
- [ ] First client onboarded

---

## 🚨 Troubleshooting

### Application won't start:
```bash
# Check logs
sudo journalctl -u reputation-monitor -n 50

# Check Python errors
source /home/ubuntu/apps/ReputationAi/venv/bin/activate
python3 /home/ubuntu/apps/ReputationAi/backend/main.py
```

### Database connection issues:
```bash
# Test PostgreSQL
sudo -u postgres psql -c "SELECT version();"

# Check .env file
cat /home/ubuntu/apps/ReputationAi/.env
```

### Scraping not working:
```bash
# Test internet connection
curl https://www.google.com

# Test specific scraper
python3 /home/ubuntu/apps/ReputationAi/backend/services/scraping/test_scraper.py
```

---

## 📞 Support

If you encounter issues:
1. Check logs: `sudo journalctl -u reputation-monitor -f`
2. Verify all services running: `sudo systemctl status`
3. Test individual components
4. Check Oracle Cloud console for VM status

---

**You now have a fully functional reputation monitoring platform for $0-$200/month!**

**Next: Start onboarding your first clients at $997-$4,997/month!** 🚀
