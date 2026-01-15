# GradMood Bot

Telegram bot for monitoring master's student mood and early detection of burnout using the Copenhagen Burnout Inventory (CBI).

## Features

- 📋 **CBI Questionnaire**: Complete 13-question burnout assessment
- 🌍 **Multi-language Support**: English and Russian
- 📊 **Results & Statistics**: View detailed results and track your progress over time
- 📈 **History**: Keep track of all your previous tests
- 🗄️ **PostgreSQL Database**: Professional database storage with SQLAlchemy ORM
- 🏗️ **Clean Architecture**: Layered architecture with models, repositories, services, and handlers
- 🖥️ **Admin Dashboard**: Web interface to view all user results and statistics
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose

## Architecture

The project follows a clean architecture pattern with clear separation of concerns:

- **Models**: SQLAlchemy ORM models (`app/models/`)
- **Repository**: Data access layer (`app/repository/`)
- **Services**: Business logic layer (`app/services/`)
- **Handlers**: Telegram bot handlers (`app/handlers/`)
- **API**: REST API endpoints for dashboard (`app/api/`)
- **Config**: Configuration and database setup (`app/config/`)
- **Utils**: Utilities and constants (`app/utils/`)

## Setup

### Option 1: Docker Compose (Recommended)

1. **Get Telegram Bot Token**
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` command
   - Follow the instructions to create your bot
   - Copy the bot token you receive

2. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Update `TELEGRAM_BOT_TOKEN` with your bot token
   - Adjust database credentials if needed

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

   This will:
   - Start PostgreSQL database
   - Initialize database tables
   - Start the bot and dashboard

4. **Run Database Migrations** (if needed)
   ```bash
   docker-compose exec gradmood alembic upgrade head
   ```

### Option 2: Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup PostgreSQL Database**
   - Install PostgreSQL
   - Create database: `CREATE DATABASE gradmood;`

3. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Update database connection settings
   - Add your Telegram bot token

4. **Initialize Database**
   ```bash
   # Run migrations
   alembic upgrade head
   
   # Or initialize directly
   python -c "from app.config.database import init_db; init_db()"
   ```

5. **Run the Bot**
   ```bash
   python bot.py
   ```

## Usage

### Telegram Bot

1. Start the bot by sending `/start` command
2. Select your preferred language (English or Russian)
3. Choose "Start New Test" to begin the CBI questionnaire
4. Answer all 13 questions using the inline buttons
5. View your results with detailed interpretation
6. Check your history and statistics anytime

### Admin Dashboard

When you run the bot, the admin dashboard automatically starts on `http://localhost:5000`

The dashboard provides:
- **Overview Statistics**: Total users, tests, and average burnout scores
- **Visual Charts**: Distribution of burnout levels and trends over time
- **Recent Tests Table**: Detailed view of all recent test results
- **Auto-refresh**: Updates every 30 seconds automatically

Open your browser and navigate to `http://localhost:5000` to access the dashboard.

## CBI Scoring

The Copenhagen Burnout Inventory measures:

- **Personal Burnout** (Questions 1-6): General exhaustion and fatigue
- **Study-related Burnout** (Questions 7-13): Burnout specific to academic work

**Scoring:**
- 0-33: Low burnout
- 34-66: Moderate burnout
- 67-100: High burnout

## Data Storage

All user data is stored in PostgreSQL database:
- **Users table**: User information and language preferences
- **Test Results table**: All test results with scores and timestamps
- Database migrations managed with Alembic

## Project Structure

```
GradMood/
├── app/                    # Application package
│   ├── models/            # SQLAlchemy ORM models
│   │   ├── user.py
│   │   └── test_result.py
│   ├── repository/        # Data access layer
│   │   ├── user_repository.py
│   │   └── test_result_repository.py
│   ├── services/          # Business logic layer
│   │   ├── user_service.py
│   │   ├── test_service.py
│   │   └── statistics_service.py
│   ├── handlers/          # Telegram bot handlers
│   │   ├── base.py
│   │   ├── start_handler.py
│   │   ├── language_handler.py
│   │   ├── test_handler.py
│   │   └── menu_handler.py
│   ├── api/               # REST API for dashboard
│   │   ├── app.py
│   │   └── routes.py
│   ├── config/            # Configuration
│   │   ├── database.py
│   │   └── settings.py
│   └── utils/             # Utilities
│       ├── constants.py
│       └── db_session.py
├── migrations/            # Database migrations (Alembic)
├── templates/             # HTML templates
│   └── dashboard.html
├── bot.py                 # Main bot entry point
├── dashboard.py           # Dashboard entry point
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── alembic.ini            # Alembic configuration
└── README.md              # This file
```

## Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## License

This project is for educational purposes.

