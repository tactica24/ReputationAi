#!/usr/bin/env python3
"""
Populate Firestore with sample data
Run with: python3 populate_firestore.py
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Initialize Firebase with default credentials
try:
    firebase_admin.initialize_app()
except:
    pass

db = firestore.client()

def populate_firestore():
    print("🚀 Populating Firestore with sample data...\n")
    
    try:
        # 1. Create Users
        print("👤 Creating users...")
        
        admin_user = {
            'email': 'admin@reputationai.com',
            'name': 'Admin User',
            'role': 'admin',
            'company': 'ReputationAI',
            'is_active': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        admin_doc = db.collection('users').add(admin_user)
        admin_id = admin_doc[1].id
        print(f"   ✅ Admin user created: {admin_id}")
        
        test_user = {
            'email': 'user@reputationai.com',
            'name': 'Test User',
            'role': 'user',
            'company': 'Test Company',
            'is_active': True,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        test_doc = db.collection('users').add(test_user)
        test_id = test_doc[1].id
        print(f"   ✅ Test user created: {test_id}")
        
        # 2. Create Entities
        print("\n🏢 Creating entities...")
        
        entity1 = {
            'name': 'TechCorp Inc',
            'entity_type': 'company',
            'description': 'Leading technology company specializing in AI solutions',
            'is_active': True,
            'ownerId': test_id,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        entity1_doc = db.collection('entities').add(entity1)
        entity1_id = entity1_doc[1].id
        print(f"   ✅ Entity 1 created: {entity1_id}")
        
        entity2 = {
            'name': 'John Smith',
            'entity_type': 'person',
            'description': 'CEO and Founder of TechCorp',
            'is_active': True,
            'ownerId': test_id,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        entity2_doc = db.collection('entities').add(entity2)
        entity2_id = entity2_doc[1].id
        print(f"   ✅ Entity 2 created: {entity2_id}")
        
        entity3 = {
            'name': 'AI Assistant Pro',
            'entity_type': 'product',
            'description': 'Advanced AI-powered virtual assistant',
            'is_active': True,
            'ownerId': test_id,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        entity3_doc = db.collection('entities').add(entity3)
        entity3_id = entity3_doc[1].id
        print(f"   ✅ Entity 3 created: {entity3_id}")
        
        # 3. Create Mentions
        print("\n💬 Creating mentions...")
        
        mentions = [
            {
                'text': "TechCorp's new AI Assistant Pro is revolutionary! Best product I've used this year.",
                'source': 'Twitter',
                'url': 'https://twitter.com/user1/status/123',
                'sentiment': 'positive',
                'sentiment_score': 0.92,
                'author': '@techfan2024',
                'entityId': entity1_id,
                'created_at': datetime.now()
            },
            {
                'text': 'Had a great experience with TechCorp support team. They resolved my issue quickly!',
                'source': 'Reddit',
                'url': 'https://reddit.com/r/tech/comments/xyz',
                'sentiment': 'positive',
                'sentiment_score': 0.85,
                'author': 'u/happycustomer',
                'entityId': entity1_id,
                'created_at': datetime.now()
            },
            {
                'text': 'The customer service could be better, but the product quality is decent.',
                'source': 'ProductHunt',
                'url': 'https://producthunt.com/posts/ai-assistant-pro',
                'sentiment': 'neutral',
                'sentiment_score': 0.5,
                'author': 'techreviewer99',
                'entityId': entity3_id,
                'created_at': datetime.now()
            },
            {
                'text': 'Not happy with the latest update. Some features are missing now.',
                'source': 'Twitter',
                'url': 'https://twitter.com/user2/status/456',
                'sentiment': 'negative',
                'sentiment_score': 0.25,
                'author': '@disappointeduser',
                'entityId': entity3_id,
                'created_at': datetime.now()
            },
            {
                'text': 'John Smith gave an excellent keynote at TechSummit 2024. Very inspiring!',
                'source': 'LinkedIn',
                'url': 'https://linkedin.com/posts/user-123',
                'sentiment': 'positive',
                'sentiment_score': 0.88,
                'author': 'Tech Enthusiast',
                'entityId': entity2_id,
                'created_at': datetime.now()
            }
        ]
        
        for i, mention in enumerate(mentions, 1):
            db.collection('mentions').add(mention)
            print(f"   ✅ Mention {i} created ({mention['sentiment']})")
        
        # 4. Create Alerts
        print("\n🔔 Creating alerts...")
        
        alerts = [
            {
                'alert_type': 'negative_mention',
                'severity': 'high',
                'message': 'Negative mention detected on Twitter',
                'is_read': False,
                'userId': test_id,
                'created_at': datetime.now()
            },
            {
                'alert_type': 'trending',
                'severity': 'medium',
                'message': 'Your brand is trending on social media',
                'is_read': False,
                'userId': test_id,
                'created_at': datetime.now()
            },
            {
                'alert_type': 'review_spike',
                'severity': 'low',
                'message': 'Increase in positive reviews detected',
                'is_read': True,
                'userId': test_id,
                'created_at': datetime.now()
            }
        ]
        
        for i, alert in enumerate(alerts, 1):
            db.collection('alerts').add(alert)
            print(f"   ✅ Alert {i} created ({alert['severity']} severity)")
        
        # 5. Create Applications
        print("\n📝 Creating applications...")
        
        applications = [
            {
                'company_name': 'Acme Corporation',
                'email': 'contact@acme.com',
                'industry': 'Technology',
                'company_size': '50-200',
                'use_case': 'Brand reputation monitoring',
                'status': 'pending',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'company_name': 'Global Enterprises',
                'email': 'info@globalent.com',
                'industry': 'Finance',
                'company_size': '200-1000',
                'use_case': 'Executive reputation management',
                'status': 'approved',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'company_name': 'Small Biz LLC',
                'email': 'hello@smallbiz.com',
                'industry': 'Retail',
                'company_size': '1-50',
                'use_case': 'Customer feedback analysis',
                'status': 'rejected',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
        
        for i, app in enumerate(applications, 1):
            db.collection('applications').add(app)
            print(f"   ✅ Application {i} created ({app['status']})")
        
        print("\n" + "="*50)
        print("✅ ALL SAMPLE DATA CREATED SUCCESSFULLY!")
        print("="*50)
        print("\n📊 Summary:")
        print("   • Users: 2")
        print("   • Entities: 3")
        print("   • Mentions: 5")
        print("   • Alerts: 3")
        print("   • Applications: 3")
        
        print("\n🔑 Login Credentials:")
        print("   Admin: admin@reputationai.com / Admin123!@#")
        print("   User:  user@reputationai.com / User123!@#")
        
        print("\n📝 Next Steps:")
        print("   1. Go to: https://console.firebase.google.com/project/reputationai-df869/authentication")
        print("   2. Create these 2 users in Firebase Authentication")
        print("   3. Set passwords: Admin123!@ and User123!@#")
        print("   4. Visit: https://reputationai-df869.web.app")
        print("   5. Login with admin credentials")
        print("   6. Dashboard will show all the sample data!")
        print("\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    if populate_firestore():
        print("✅ Done!")
        exit(0)
    else:
        print("❌ Failed!")
        exit(1)
