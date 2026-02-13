# Plant's Doctor 🌱

A Flask web application for plant disease prediction using deep learning models. Supports disease detection for Tomato, Apple, Potato, and Rice plants.

## Features

- **Multi-Plant Disease Detection**: Predict diseases for 4 different plant types
- **User Authentication**: Secure registration, login, and password reset
- **Credit System**: Prediction credits with email-based token redemption
- **Admin Panel**: Batch prediction testing for model evaluation
- **Database Tracking**: Complete history of user predictions

## Technology Stack

- **Backend**: Flask 2.3.3
- **Database**: MySQL with SQLAlchemy ORM
- **ML Framework**: TensorFlow 2.13.0
- **Image Processing**: OpenCV, NumPy
- **Authentication**: Flask-Bcrypt for password hashing
- **Email**: Flask-Mail for notifications
- **Migrations**: Flask-Migrate (Alembic)

## Project Structure

```
Plant-s-Doctor/
├── app/                        # Main application package
│   ├── models/                 # Database models
│   ├── routes/                 # Blueprint routes (auth, main, prediction)
│   ├── services/               # Business logic layer
│   ├── ml/                     # ML models and prediction logic
│   ├── utils/                  # Utilities and decorators
│   ├── static/                 # CSS, JS, images
│   └── templates/              # HTML templates
├── all_models/                 # Trained ML models (.h5 files)
├── migrations/                 # Database migrations
├── uploads/                    # Temporary file uploads
├── app.py                      # Application entry point
├── config.py                   # Configuration management
└── requirements.txt            # Python dependencies
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Plant-s-Doctor
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@host/database
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

### 5. Initialize Database

```bash
# Initialize migration repository
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration to database
flask db upgrade
```

### 6. Create Admin User (Optional)

```bash
flask create-admin
```

### 7. Run Application

```bash
python app.py
```

The application will be available at `http://localhost:5001`

## Database Models

### Users
- Authentication and user management
- Password hashing with bcrypt
- Prediction credit tracking
- Admin role support

### Predictions
- Complete prediction history
- Tracks plant type, result, and timestamp
- Linked to user accounts

### Password Reset Tokens
- Secure password reset flow
- Token expiration (1 hour)
- One-time use tokens

### Credit Tokens
- Email-based credit redemption
- Token expiration (24 hours)
- Configurable credit amounts

## API Endpoints

### Authentication
- `POST /login_validation` - User login
- `POST /reg_user` - User registration
- `GET /logout` - User logout
- `POST /forgot` - Request password reset
- `POST /reset_fun` - Reset password with token

### Predictions
- `POST /tomato-predict` - Predict tomato disease
- `POST /apple-predict` - Predict apple disease
- `POST /potato-predict` - Predict potato disease
- `POST /rice-predict` - Predict rice disease

### Admin (Batch Testing)
- `POST /tomato-predict-admin` - Batch test tomato model
- `POST /apple-predict-admin` - Batch test apple model
- `POST /potato-predict-admin` - Batch test potato model
- `POST /rice-predict-admin` - Batch test rice model

## Development

### Database Migrations

After modifying models:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Flask Shell

Access models in interactive shell:

```bash
flask shell
>>> User.query.all()
>>> db.session.add(user)
>>> db.session.commit()
```

## Security Features

- ✅ Password hashing with bcrypt
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ Secure session management
- ✅ Input validation and sanitization
- ✅ Token-based password reset
- ✅ File upload validation

## Architecture Highlights

### Separation of Concerns
- **Models**: Database schema and relationships
- **Services**: Business logic (auth, email, user management)
- **Routes**: Request handling and response
- **ML Module**: Prediction logic isolated from web layer
- **Utils**: Reusable decorators and validators

### Code-First Database
- SQLAlchemy models define schema
- Automatic migration generation
- Easy rollback and version control
- Database-agnostic design

### Lazy Model Loading
- ML models loaded on first use
- Singleton pattern for memory efficiency
- Reduced startup time

## License

MIT License

## Contributors

Original ML models and concept by Plant's Doctor team
Refactored architecture - 2026
