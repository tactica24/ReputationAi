# 🚀 Quick Start Guide - Get Running in 60 Minutes

## Overview

Get your AI Reputation Monitor running for **$0-$200/month** in under an hour.

---

## Phase 1: Setup (20 minutes)

### 1. Oracle Cloud Account
1. Go to https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Fill in details (credit card needed but NEVER charged)
4. Verify email
5. Login to console

### 2. Create Free VM
1. In Oracle Console: **Compute → Instances → Create Instance**
2. Settings:
   - Name: `reputation-monitor`
   - Image: `Ubuntu 22.04`
   - Shape: `VM.Standard.A1.Flex` (ARM)
   - OCPUs: `4`
   - Memory: `24 GB`
   - Boot volume: `200 GB`
3. Generate SSH key pair → Download private key
4. Click **Create** (takes 2-3 minutes)
5. Note your public IP address

### 3. Connect to Server
```bash
# On your local machine
chmod 400 ~/Downloads/oracle-key.pem
ssh -i ~/Downloads/oracle-key.pem ubuntu@YOUR_IP_ADDRESS
```

---

## Phase 2: Install (15 minutes)

### Run Installation Script
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies (one command)
sudo apt install -y \
    python3.10 python3-pip python3-venv \
    git nginx postgresql postgresql-contrib \
    redis-server certbot python3-certbot-nginx

# Clone your repository
mkdir -p ~/apps && cd ~/apps
git clone https://github.com/tactica24/ReputationAi.git
cd ReputationAi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Download AI models (this takes ~5 minutes)
python3 -c "
from transformers import pipeline
pipeline('text-classification', model='hamzab/roberta-fake-news-classification')
pipeline('sentiment-analysis', model='cardiffnlp/twitter-roberta-base-sentiment-latest')
pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
print('✅ Models downloaded!')
"
```

---

## Phase 3: Configure Database (5 minutes)

```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres psql <<EOF
CREATE DATABASE reputation_monitor;
CREATE USER repmonitor WITH PASSWORD 'change_this_password';
GRANT ALL PRIVILEGES ON DATABASE reputation_monitor TO repmonitor;
\q
EOF

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Initialize database tables
python3 backend/database/models.py
```

---

## Phase 4: Configure Application (5 minutes)

```bash
# Create .env file
cat > .env <<EOF
DATABASE_URL=postgresql://repmonitor:change_this_password@localhost/reputation_monitor
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=$(openssl rand -hex 32)
DEBUG=False

# Optional API keys (get from respective websites)
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
NEWSAPI_KEY=
SENDGRID_API_KEY=
EOF

# Test configuration
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('✅ Configuration loaded')
print(f'Database: {os.getenv(\"DATABASE_URL\")[:30]}...')
"
```

---

## Phase 5: Deploy (10 minutes)

### 1. Create System Service
```bash
sudo tee /etc/systemd/system/reputation-monitor.service > /dev/null <<EOF
[Unit]
Description=Reputation Monitor API
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$HOME/apps/ReputationAi
Environment="PATH=$HOME/apps/ReputationAi/venv/bin"
ExecStart=$HOME/apps/ReputationAi/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl start reputation-monitor
sudo systemctl enable reputation-monitor

# Check status
sudo systemctl status reputation-monitor
```

### 2. Configure NGINX
```bash
sudo tee /etc/nginx/sites-available/reputation-monitor > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/reputation-monitor /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 3. Setup Automated Scanning
```bash
# Add cron jobs
crontab -e

# Add these lines:
*/15 6-22 * * * $HOME/apps/ReputationAi/venv/bin/python $HOME/apps/ReputationAi/backend/scripts/run_scrapers.py
0 2 * * * $HOME/apps/ReputationAi/venv/bin/python $HOME/apps/ReputationAi/backend/scripts/daily_scan.py
```

---

## Phase 6: Test (5 minutes)

### 1. Test API
```bash
# Test health endpoint
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

### 2. Test Web Scraping
```bash
cd ~/apps/ReputationAi
source venv/bin/activate

python3 -c "
import asyncio
from backend.services.scraping.free_web_scraper import PublicContentScraper

async def test():
    scraper = PublicContentScraper()
    results = await scraper.scrape_news_rss('Elon Musk')
    print(f'✅ Scraping works! Found {len(results)} news articles')

asyncio.run(test())
"
```

### 3. Test AI Detection
```bash
python3 -c "
import asyncio
from backend.services.ai_detection.free_ai_engine import FreeAIDetectionEngine

async def test():
    engine = FreeAIDetectionEngine()
    result = await engine.detect_fake_news('Breaking: Company faces major scandal')
    print(f'✅ AI detection works!')
    print(f'Fake news probability: {result.confidence:.2%}')

asyncio.run(test())
"
```

---

## ✅ You're Live!

### Access your platform:
- **API**: http://YOUR_IP_ADDRESS/
- **Website**: Copy frontend files to `/var/www/html/`
- **Admin**: Create admin user via Python script

### Monthly Costs:
- **Oracle Cloud VM**: $0 (Free Forever)
- **PostgreSQL**: $0 (Self-hosted)
- **Redis**: $0 (Self-hosted)
- **AI Models**: $0 (HuggingFace)
- **SSL Certificate**: $0 (Let's Encrypt)
- **Optional Proxies**: $50-100/month

**Total: $0-$100/month** 🎉

---

## Next Steps

### 1. Add Your First Client
```bash
python3 -c "
from backend.database.models import SessionLocal, User, MonitoredPerson
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
db = SessionLocal()

# Create user
user = User(
    email='client@example.com',
    hashed_password=pwd_context.hash('temporary_password'),
    full_name='Test Client',
    company_name='Test Company',
    subscription_tier='executive',
    monthly_rate=2497.0,
    is_verified=True
)
db.add(user)
db.commit()

# Create monitored person
person = MonitoredPerson(
    user_id=user.id,
    name='Client Name',
    aliases=['Client Alias'],
    social_handles={
        'twitter': '@handle',
        'linkedin': 'profile-url'
    },
    keywords=['company name', 'ceo name'],
    platforms=['twitter', 'reddit', 'news']
)
db.add(person)
db.commit()

print(f'✅ Client created: {user.email}')
print(f'✅ Monitoring: {person.name}')
"
```

### 2. Get Free API Keys (Optional but Recommended)

**Reddit** (Free - 60 requests/min):
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script"
4. Add to .env: `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`

**NewsAPI** (Free - 100 requests/day):
1. Go to https://newsapi.org/register
2. Get API key
3. Add to .env: `NEWSAPI_KEY`

**SendGrid** (Free - 100 emails/day):
1. Go to https://signup.sendgrid.com/
2. Create API key
3. Add to .env: `SENDGRID_API_KEY`

### 3. Monitor Logs
```bash
# Watch API logs
sudo journalctl -u reputation-monitor -f

# Watch scraper logs
tail -f ~/apps/ReputationAi/logs/scraper.log

# Watch AI detection logs
tail -f ~/apps/ReputationAi/logs/ai_detection.log
```

---

## 🎯 Start Selling!

You now have a platform that costs **$0-$100/month** to run.

### Pricing Your Service:
- **Individual**: $997/month (1 person monitored)
- **Executive**: $2,497/month (3 people + priority alerts)
- **Enterprise**: $4,997/month (10 people + custom features)

### Break-Even Analysis:
- **1 client**: $997-$4,997 revenue - $100 costs = **$897-$4,897 profit** (90-98% margin!)
- **10 clients**: $9,970-$49,970 revenue - $200 costs = **~$48K profit/month**
- **100 clients**: $99,700-$499,700 revenue - $500 costs = **~$450K profit/month**

**You can start making money from client #1!** 🚀

---

## 📞 Troubleshooting

### Service won't start?
```bash
sudo systemctl status reputation-monitor
sudo journalctl -u reputation-monitor -n 50
```

### Can't connect to database?
```bash
sudo systemctl status postgresql
sudo -u postgres psql -c "SELECT version();"
```

### AI models not working?
```bash
# Re-download models
cd ~/apps/ReputationAi
source venv/bin/activate
python3 -c "
from transformers import pipeline
pipeline('text-classification', model='hamzab/roberta-fake-news-classification')
"
```

---

## 🎉 Congratulations!

You've deployed a reputation monitoring platform that:
- ✅ Costs **$0-$100/month** to run
- ✅ Can charge **$997-$4,997/month** per client
- ✅ Has **90-98% profit margins**
- ✅ Scales to thousands of clients
- ✅ Uses enterprise-grade security
- ✅ Runs completely autonomously

**Now go get your first client!** 💰

For detailed documentation, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
