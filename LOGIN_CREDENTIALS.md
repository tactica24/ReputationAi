# Admin Login Setup - PRODUCTION READY

## Real Database-Backed Authentication

The system now uses a **real SQLite database** with proper user management, password hashing, and JWT authentication.

## Default Admin Accounts

### Super Admin (Full System Access)
- **Email:** `admin@reputation.ai`
- **Password:** `Admin@2024!`
- **Role:** super_admin
- **Permissions:** Complete system control, user management, all features

### Manager
- **Email:** `manager@reputation.ai`
- **Password:** `Manager@2024!`
- **Role:** manager
- **Permissions:** Manage entities, alerts, analytics

### Analyst
- **Email:** `analyst@reputation.ai`
- **Password:** `Analyst@2024!`
- **Role:** analyst
- **Permissions:** View analytics, manage alerts

### Viewer
- **Email:** `user@reputation.ai`
- **Password:** `User@2024!`
- **Role:** viewer
- **Permissions:** Read-only access

## Accessing the Dashboard

1. **Navigate to:** https://reputation-ai-one.vercel.app/app
2. **Enter credentials** from above
3. **Click "Sign In"**

## Creating New Users

Users can register through the API or you can create them via the database directly.

### Via Registration Endpoint:
```bash
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "full_name": "New User Name",
    "password": "SecurePassword123!"
  }'
```

## Database Information

- **Type:** SQLite (local development)
- **Location:** `/workspaces/ReputationAi/reputationai.db`
- **Tables:** Users, Entities, Mentions, Alerts, etc.
- **Password Hashing:** bcrypt (industry standard)

## Reinitializing Database

To reset and recreate the database with default users:

```bash
cd /workspaces/ReputationAi
rm reputationai.db  # Delete existing database
python -m backend.scripts.init_db  # Create fresh database
```

## Running the Backend

To start the backend API server:

```bash
cd /workspaces/ReputationAi
python -m uvicorn backend.main:app --reload --port 8080
```

The frontend will connect to `http://localhost:8080/api/v1`

## Production Deployment

For production, replace SQLite with PostgreSQL:

1. **Set DATABASE_URL environment variable:**
   ```bash
   export DATABASE_URL="postgresql://user:password@host:5432/database"
   ```

2. **Update connection.py** to use PostgreSQL

3. **Run migrations:**
   ```bash
   python -m backend.scripts.init_db
   ```

## Security Features

✅ **Real Database:** SQLite/PostgreSQL with proper schema
✅ **Password Hashing:** bcrypt with salt (industry standard)
✅ **JWT Tokens:** Secure token-based authentication
✅ **Role-Based Access:** Super Admin, Manager, Analyst, Viewer
✅ **Password Validation:** Strong password requirements
✅ **Session Management:** 24-hour token expiration
✅ **CORS Protection:** Restricted origins
✅ **SQL Injection Prevention:** SQLAlchemy ORM

## Changing Admin Password

To change the admin password:

```bash
cd /workspaces/ReputationAi
python -c "
from backend.api.auth import hash_password
from backend.database.connection import SessionLocal
from backend.database.models import User

db = SessionLocal()
admin = db.query(User).filter(User.email == 'admin@reputation.ai').first()
admin.hashed_password = hash_password('YourNewPassword!')
db.commit()
print('Password updated successfully')
"
```

## API Endpoints

- `POST /api/v1/auth/login` - Login with email/password
- `POST /api/v1/auth/register` - Register new user
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout

## Support

For issues or questions, check the backend logs or database directly.

Database location: `/workspaces/ReputationAi/reputationai.db`

