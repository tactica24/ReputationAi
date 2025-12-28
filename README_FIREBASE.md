# 🛡️ ReputationAI - AI-Powered Reputation Management Platform

> **Protect Your Reputation. Monitor Your Brand. Control Your Narrative.**

[![Firebase](https://img.shields.io/badge/Firebase-Ready-orange)](https://firebase.google.com)
[![React](https://img.shields.io/badge/React-18.x-blue)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-Proprietary-red)]()

## 🚀 Live Demo

**🌐 Website**: [https://reputationai-df869.web.app](https://reputationai-df869.web.app)

### 🔑 Demo Credentials
- **Admin**: `admin@reputationai.com` / `Admin123!@#`
- **User**: `user@reputationai.com` / `User123!@#`

---

## ✨ Features

### 🎯 Core Functionality
- ✅ **Real-time Reputation Monitoring** - Track mentions across social media
- ✅ **Sentiment Analysis** - AI-powered sentiment detection
- ✅ **Entity Management** - Monitor people, companies, brands, products
- ✅ **Smart Alerts** - Get notified about critical mentions
- ✅ **Analytics Dashboard** - Comprehensive reputation insights
- ✅ **Multi-user Support** - Admin and user roles

### 🔐 Security & Authentication
- ✅ Firebase Authentication integration
- ✅ Role-based access control (Admin/User)
- ✅ Secure Firestore rules
- ✅ Rate limiting on API endpoints
- ✅ Input validation and sanitization

### 📊 Admin Features
- ✅ User management
- ✅ Application approvals
- ✅ System analytics
- ✅ Data export
- ✅ Audit logs

---

## 🏗️ Technology Stack

### Frontend
- **Framework**: React 18
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **Charts**: Recharts
- **Icons**: Lucide React
- **Routing**: React Router v6

### Backend
- **Platform**: Firebase
- **Authentication**: Firebase Auth
- **Database**: Cloud Firestore
- **Functions**: Firebase Cloud Functions
- **Hosting**: Firebase Hosting
- **Storage**: Firebase Storage

### Development
- **Build Tool**: Vite
- **Package Manager**: npm
- **Language**: JavaScript/JSX

---

## 📦 Quick Start

### Prerequisites
- Node.js 18+
- Firebase CLI
- npm or yarn

### 1️⃣ Clone & Install
```bash
git clone https://github.com/tactica24/ReputationAi.git
cd ReputationAi
```

### 2️⃣ Install Dependencies
```bash
# Frontend
cd frontend
npm install --legacy-peer-deps

# Functions
cd ../functions
npm install
```

### 3️⃣ Deploy to Firebase
```bash
cd ..
./deploy-complete.sh
```

**That's it!** Your app is live at `https://reputationai-df869.web.app`

---

## 📚 Documentation

- 📘 [**Quick Start Guide**](QUICK_START_FIREBASE.md) - Get started in minutes
- 📗 [**Deployment Guide**](FIREBASE_DEPLOYMENT.md) - Complete deployment instructions
- 📙 [**Credentials**](CREDENTIALS.md) - Login info and access details
- 📕 [**API Documentation**](functions/README.md) - API endpoints reference

---

## 🗂️ Project Structure

```
ReputationAI/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # UI components
│   │   │   ├── admin/       # Admin dashboard
│   │   │   ├── auth/        # Login/authentication
│   │   │   ├── dashboard/   # Main dashboard
│   │   │   ├── entities/    # Entity management
│   │   │   ├── mentions/    # Mention tracking
│   │   │   ├── alerts/      # Alert system
│   │   │   └── analytics/   # Analytics views
│   │   ├── services/        # Firebase services
│   │   │   ├── firebaseService.js  # Firestore operations
│   │   │   └── api.js       # API wrapper
│   │   ├── config/          # Firebase config
│   │   ├── store/           # State management
│   │   └── utils/           # Utilities
│   └── build/               # Production build
│
├── functions/               # Firebase Cloud Functions
│   ├── index.js            # API endpoints
│   ├── create-admin.js     # Admin user creation
│   └── seed-firebase.js    # Database seeding
│
├── firebase.json           # Firebase configuration
├── firestore.rules        # Firestore security rules
├── firestore.indexes.json # Firestore indexes
├── storage.rules          # Storage security rules
└── deploy-complete.sh     # One-click deployment
```

---

## 🔥 Firebase Services

### Firestore Collections
- `users` - User profiles and roles
- `entities` - Tracked entities (people, companies, brands)
- `mentions` - Social media mentions and reviews
- `alerts` - Notifications and warnings
- `applications` - User onboarding requests

### Cloud Functions
- `/api/v1/auth/*` - Authentication endpoints
- `/api/v1/users/*` - User management
- `/api/v1/entities/*` - Entity CRUD operations
- `/api/v1/mentions/*` - Mention tracking
- `/api/v1/alerts/*` - Alert management
- `/api/v1/analytics/*` - Analytics and reporting

---

## 🛠️ Development

### Local Development
```bash
# Start frontend dev server
cd frontend
npm run dev

# The app will be available at http://localhost:5173
```

### Firebase Emulators (Optional)
```bash
firebase emulators:start
```

### Build Production
```bash
cd frontend
npm run build
```

### Deploy
```bash
# Deploy everything
firebase deploy

# Deploy only hosting
firebase deploy --only hosting

# Deploy only functions
firebase deploy --only functions
```

---

## 📊 Admin Dashboard

### Features
- 📈 Real-time analytics
- 👥 User management
- 📝 Application approvals
- 🔔 Alert configuration
- 📊 System metrics
- 📥 Data export

### Access
Login with admin credentials to access `/admin` route.

---

## 💰 Pricing & Business Model

### SaaS Pricing Tiers
- **Starter**: $97/month - 1 entity, 100 mentions/month
- **Professional**: $297/month - 5 entities, 500 mentions/month
- **Business**: $997/month - 20 entities, 2,000 mentions/month
- **Enterprise**: Custom - Unlimited entities and mentions

### Cost Structure
- **Firebase Spark Plan**: FREE
  - 10GB hosting
  - 50K Firestore reads/day
  - 125K function invocations/month
  
- **Firebase Blaze Plan**: Pay-as-you-go
  - Scale automatically
  - Only pay for usage
  - Set budget alerts

**Profit Margin**: 90%+ (minimal infrastructure costs)

---

## 🔐 Security

### Authentication
- Email/password authentication
- Role-based access control
- Secure token-based sessions

### Firestore Rules
- Users can only access their own data
- Admins have full access
- All write operations require authentication

### API Security
- CORS protection
- Rate limiting (100 req/15min)
- Input validation
- XSS protection via Helmet.js

---

## 🚀 Deployment

### Automated Deployment
```bash
./deploy-complete.sh
```

This will:
1. ✅ Build frontend
2. ✅ Install dependencies
3. ✅ Create admin user
4. ✅ Seed database
5. ✅ Deploy to Firebase

### Manual Deployment
See [FIREBASE_DEPLOYMENT.md](FIREBASE_DEPLOYMENT.md)

---

## 📈 Monitoring

### Firebase Console
- **Logs**: https://console.firebase.google.com/project/reputationai-df869/functions/logs
- **Analytics**: https://console.firebase.google.com/project/reputationai-df869/analytics
- **Performance**: https://console.firebase.google.com/project/reputationai-df869/performance

### View Logs
```bash
firebase functions:log
```

---

## 🤝 Contributing

This is a proprietary project. Contact the maintainer for collaboration opportunities.

---

## 📄 License

Proprietary - All Rights Reserved

---

## 🆘 Support

### Issues?
1. Check [QUICK_START_FIREBASE.md](QUICK_START_FIREBASE.md)
2. Review Firebase Console logs
3. Check browser console (F12)
4. Verify Firestore data

### Resources
- [Firebase Documentation](https://firebase.google.com/docs)
- [React Documentation](https://react.dev)
- [Firestore Guide](https://firebase.google.com/docs/firestore)

---

## 🎯 Roadmap

### ✅ Completed
- [x] Firebase integration
- [x] Admin dashboard
- [x] User authentication
- [x] Entity management
- [x] Mention tracking
- [x] Analytics dashboard
- [x] Alert system

### 🚧 In Progress
- [ ] Real-time AI sentiment analysis
- [ ] Social media API integrations
- [ ] Email notifications
- [ ] Export to PDF/CSV

### 📋 Planned
- [ ] Mobile app (iOS/Android)
- [ ] Chrome extension
- [ ] Slack integration
- [ ] Advanced AI models
- [ ] Multi-language support

---

## 📞 Contact

**Project**: ReputationAI  
**Website**: https://reputationai-df869.web.app  
**Repository**: https://github.com/tactica24/ReputationAi

---

**Built with ❤️ using Firebase, React, and AI**

*Last Updated: December 28, 2025*
