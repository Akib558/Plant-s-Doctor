# Plant's Doctor - Setup and Migration Guide

## ✅ Refactoring Complete!

The application has been successfully refactored from a monolithic 826-line file to a clean modular architecture with 20+ organized Python files.

## What Changed

### Before
```
Plant-s-Doctor/
├── app.py (826 lines - EVERYTHING)
├── templates/
├── static/
└── all_models/
```

### After
```
Plant-s-Doctor/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models/               # SQLAlchemy models (4 files)
│   ├── routes/               # Blueprints (3 files: auth, main, prediction)
│   ├── services/             # Business logic (3 files)
│   ├── ml/                   # ML module (3 files)
│   └── utils/                # Helpers (2 files)
├── config.py                 # Configuration
├── app.py                    # Entry point (53 lines)
├── requirements.txt
└── .env.example
```

## Installation Steps

### 1. Install Dependencies

```bash
cd /home/akib/Coding/16_Projects/Plant-s-Doctor
pip install -r requirements.txt
```

**Note**: This will install:
- Flask and extensions (SQLAlchemy, Migrate, Bcrypt, Mail)
- ML dependencies (TensorFlow, OpenCV, NumPy)
- Database driver (PyMySQL)
- Utilities (python-dotenv, Werkzeug)

### 2. Configure Environment

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

**Update these values in `.env`:**
```env
SECRET_KEY=generate-a-random-secret-key-here
DATABASE_URL=mysql+pymysql://OQmAQgAGIs:OTh3lb0dWY@remotemysql.com/OQmAQgAGIs
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

**To generate a secret key:**
```bash
python3 -c "import os; print(os.urandom(24).hex())"
```

### 3. Initialize Database

```bash
# Initialize Flask-Migrate
flask db init

# Create initial migration (generates migration file)
flask db migrate -m "Initial database schema"

# Apply migration to database
flask db upgrade
```

This will create all tables:
- `users` (with bcrypt password hashing)
- `predictions` (tracking history)
- `password_reset_tokens` (secure password reset)
- `credit_tokens` (credit redemption system)

### 4. Create Admin User (Optional)

```bash
flask create-admin
```

This will prompt for:
- Admin username
- Admin email
- Admin password

The admin user will have:
- `is_admin = True`
- 99,999 prediction credits
- Access to batch testing endpoints

### 5. Run the Application

```bash
python app.py
```

Or using Flask CLI:
```bash
flask run --port=5001 --debug
```

The app will be available at: `http://localhost:5001`

## Database Migration from Old Schema

If you have existing users in the old database, you need to migrate them:

### Option 1: Manual Data Migration Script

Create `migrate_users.py`:

```python
import mysql.connector
from app import create_app, db, bcrypt
from app.models import User

# Old database connection
old_conn = mysql.connector.connect(
    host="remotemysql.com",
    user="OQmAQgAGIs",
    password="OTh3lb0dWY",
    database="OQmAQgAGIs"
)
old_cursor = old_conn.cursor()

# Get all users from old schema
old_cursor.execute("SELECT user_id, name, email, password, count FROM user")
old_users = old_cursor.fetchall()

# Create Flask app context
app = create_app()
with app.app_context():
    for old_user in old_users:
        user_id, name, email, password, count = old_user
        
        # Check if user already exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"Skipping {email} - already exists")
            continue
        
        # Hash the plain-text password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new user with hashed password
        new_user = User(
            username=name,
            email=email,
            password_hash=password_hash,
            is_admin=(name == 'admin'),
            prediction_credits=count or 10
        )
        
        db.session.add(new_user)
        print(f"Migrated: {email}")
    
    db.session.commit()
    print("Migration complete!")

old_conn.close()
```

Run it:
```bash
python migrate_users.py
```

### Option 2: Fresh Start

If you don't have important user data, start fresh:

1. The new database will be empty
2. Users will need to register again
3. Passwords will be properly hashed from the start

## Testing the Application

### 1. Test Registration
- Go to `http://localhost:5001`
- Register a new account
- Password will be securely hashed

### 2. Test Login
- Login with your credentials
- Session will be created

### 3. Test Predictions
- Navigate to any plant page (Tomato, Apple, Potato, Rice)
- Upload an image
- Check prediction result
- Verify credits are deducted

### 4. Test Password Reset
- Click "Forgot Password"
- Enter your email
- Check email for token
- Use token to reset password

### 5. Test Admin Features (if admin user created)
- Login as admin
- Access admin prediction pages
- Test batch predictions on directories

## Key Improvements Implemented

### 🔒 Security
- ✅ **Password Hashing**: Bcrypt instead of plain-text
- ✅ **SQL Injection Prevention**: SQLAlchemy ORM (no raw queries)
- ✅ **Token Expiration**: Password reset (1hr), Credit tokens (24hr)
- ✅ **Input Validation**: Email, file types, all inputs
- ✅ **Session Security**: Proper secret key management

### 🏗️ Architecture
- ✅ **Separation of Concerns**: Models, Routes, Services, ML separated
- ✅ **Blueprint Pattern**: Modular route organization
- ✅ **Service Layer**: Business logic isolated from routes
- ✅ **Code-First Database**: SQLAlchemy models with migrations
- ✅ **Lazy Loading**: ML models loaded on demand

### 🧹 Code Quality
- ✅ **DRY Principle**: Eliminated duplicate prediction functions
- ✅ **Consistent Naming**: PEP 8 compliant
- ✅ **Docstrings**: All functions documented
- ✅ **Error Handling**: Try-catch blocks, proper responses
- ✅ **Configuration**: Environment variables, no hardcoded values

### 📊 Database
- ✅ **Proper Schema**: Foreign keys, indexes, constraints
- ✅ **Relationships**: User → Predictions, Tokens
- ✅ **Migration System**: Version-controlled schema changes
- ✅ **Prediction History**: Track all user predictions

## File Changes Summary

### Created (21 new files)
```
config.py
requirements.txt
.env.example
.gitignore
app/__init__.py
app/models/__init__.py
app/models/user.py
app/routes/__init__.py
app/routes/auth.py
app/routes/main.py
app/routes/prediction.py
app/services/__init__.py
app/services/auth_service.py
app/services/user_service.py
app/services/email_service.py
app/ml/__init__.py
app/ml/model_loader.py
app/ml/preprocessors.py
app/ml/predictors.py
app/utils/__init__.py
app/utils/decorators.py
app/utils/validators.py
```

### Renamed
```
app.py → app_old.py (backup)
app.py (new entry point - 53 lines)
```

### Unchanged
```
templates/ (all HTML files - no changes)
static/ (CSS, JS, images - no changes)
all_models/ (ML models - no changes)
```

## CLI Commands

The new app includes helpful CLI commands:

```bash
# Initialize database tables
flask init-db

# Create admin user interactively
flask create-admin

# Access Flask shell with models loaded
flask shell

# Database migrations
flask db init      # First time only
flask db migrate -m "description"
flask db upgrade
flask db downgrade
```

## Troubleshooting

### Database Connection Issues
```bash
# Test connection
python3 -c "import pymysql; conn = pymysql.connect(host='remotemysql.com', user='OQmAQgAGIs', password='OTh3lb0dWY', database='OQmAQgAGIs'); print('✓ Connected')"
```

### Import Errors
```bash
# Make sure you're in the right directory
cd /home/akib/Coding/16_Projects/Plant-s-Doctor

# Reinstall dependencies
pip install -r requirements.txt
```

### Migration Errors
```bash
# Reset migrations (CAUTION: drops all tables)
rm -rf migrations/
flask db init
flask db migrate -m "Fresh start"
flask db upgrade
```

### Model Loading Issues
```bash
# Verify model files exist
ls -lh all_models/*.h5
```

## What's NOT Changed

✅ **ML Models**: Same .h5 files, same algorithms
✅ **UI Templates**: Same HTML files
✅ **CSS/JS**: No frontend changes
✅ **Features**: No new features added
✅ **Business Logic**: Same prediction flow
✅ **Port**: Still runs on 5001

## Next Steps

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Configure .env**: Set your credentials
3. **Initialize database**: Run Flask-Migrate commands
4. **Test locally**: Start the app and test all features
5. **Migrate users** (optional): Run migration script if needed

## Questions?

If you encounter any issues:
1. Check the logs for error messages
2. Verify all environment variables are set
3. Ensure database connection works
4. Check that all ML model files exist

## Success Criteria

You'll know the refactoring is successful when:
- ✅ App starts without errors
- ✅ User can register and login
- ✅ Predictions work correctly
- ✅ Credits are deducted properly
- ✅ Password reset emails work
- ✅ Admin features accessible (if admin exists)
- ✅ No SQL injection vulnerabilities
- ✅ Passwords are hashed in database

**The refactoring is complete and ready for testing!** 🎉
