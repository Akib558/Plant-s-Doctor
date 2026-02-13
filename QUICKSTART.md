# Quick Start Guide - Plant's Doctor

## Installation (5 minutes)

```bash
# 1. Navigate to project
cd /home/akib/Coding/16_Projects/Plant-s-Doctor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials (DATABASE_URL, MAIL_USERNAME, MAIL_PASSWORD)

# 4. Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 5. Create admin (optional)
flask create-admin

# 6. Run application
python app.py
```

## Quick Commands

```bash
# Start application
python app.py

# Database operations
flask db migrate -m "description"    # Create migration
flask db upgrade                      # Apply migrations
flask db downgrade                    # Rollback

# Admin operations
flask create-admin                    # Create admin user
flask init-db                         # Initialize tables

# Shell access
flask shell                           # Interactive Python shell
```

## Project Structure

```
app/
├── models/         → Database models (SQLAlchemy)
├── routes/         → URL endpoints (Blueprints)
├── services/       → Business logic
├── ml/             → Machine learning
└── utils/          → Helpers & decorators
```

## Key Files

| File | Purpose |
|------|---------|
| `config.py` | Configuration settings |
| `app.py` | Application entry point |
| `.env` | Environment variables (create from .env.example) |
| `requirements.txt` | Python dependencies |
| `app_old.py` | Original backup file |

## Environment Variables (.env)

```env
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://user:pass@host/db
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

## Security Features

✅ Bcrypt password hashing
✅ SQL injection prevention (ORM)
✅ Token expiration (1hr for password reset)
✅ Input validation
✅ Secure session management
✅ File upload validation

## Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login_validation` - Login submit
- `POST /reg_user` - Register
- `GET /logout` - Logout
- `POST /forgot` - Request password reset
- `POST /reset_fun` - Reset password

### Main Pages
- `GET /` - Home (redirects to login if not authenticated)
- `GET /ppp.html` - Dashboard
- `GET /user_profile` - User profile
- `GET /apple.html` - Apple prediction page
- `GET /tomato.html` - Tomato prediction page
- `GET /potato.html` - Potato prediction page
- `GET /rice.html` - Rice prediction page

### Predictions (POST, requires login & credits)
- `/tomato-predict` - Predict tomato disease
- `/apple-predict` - Predict apple disease
- `/potato-predict` - Predict potato disease
- `/rice-predict` - Predict rice disease

### Admin (POST, requires admin role)
- `/tomato-predict-admin` - Batch test tomato model
- `/apple-predict-admin` - Batch test apple model
- `/potato-predict-admin` - Batch test potato model
- `/rice-predict-admin` - Batch test rice model

## Troubleshooting

### "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### "Connection refused" database error
- Check DATABASE_URL in .env
- Verify database server is running
- Test connection: `mysql -h host -u user -p`

### "Template not found"
- Ensure templates/ directory exists
- Check file names match exactly

### ML model errors
- Verify all .h5 files exist in all_models/
- Check file paths in config.py

### Email not sending
- Update MAIL_USERNAME and MAIL_PASSWORD in .env
- For Gmail, use App-Specific Password
- Enable "Less secure app access" or use OAuth2

## Database Models

- **User**: Authentication, credits, admin status
- **Prediction**: History of all predictions
- **PasswordResetToken**: Password reset flow
- **CreditToken**: Credit redemption system

## Default Settings

- **Port**: 5001
- **Default Credits**: 10 per user
- **Max Upload Size**: 16MB
- **Allowed Extensions**: png, jpg, jpeg, gif, webp
- **Token Validity**: 1 hour (password reset), 24 hours (credits)

## Documentation

- `README.md` - Full project documentation
- `SETUP_GUIDE.md` - Detailed setup instructions
- `REFACTORING_RESULTS.md` - Before/after comparison

## Support

For issues:
1. Check logs for error messages
2. Verify environment variables
3. Test database connection
4. Ensure ML models exist
5. Review SETUP_GUIDE.md

## Migration from Old Version

If you have existing users:
1. See `SETUP_GUIDE.md` → "Database Migration" section
2. Use provided migration script
3. Or start fresh with new database schema

---

**Ready to go?** Run `python app.py` and visit `http://localhost:5001`
