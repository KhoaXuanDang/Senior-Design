# UC Cookbook Backend - Quick Start Guide

Get the backend running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- pip (Python package manager)

## Quick Setup

### 1. Navigate to backend directory

```bash
cd Senior-Design/Code/uc-cookbook-backend
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run setup script

```bash
python scripts/setup.py
```

This will:
- Create `.env` file if needed
- Run database migrations
- Optionally seed the database with sample data

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

## Verify Installation

1. Open browser to: http://localhost:8000/docs
2. You should see the Swagger UI with all API endpoints
3. Test the health check: http://localhost:8000/health

## Demo Credentials

If you seeded the database:
- **Email:** demo@mail.uc.edu
- **Password:** demo123

## Common Commands

### Run tests
```bash
pytest
```

### Run tests with coverage
```bash
pytest --cov=app
```

### Create new migration
```bash
alembic revision --autogenerate -m "description"
```

### Apply migrations
```bash
alembic upgrade head
```

### Seed database
```bash
python scripts/seed.py
```

## Troubleshooting

### Port already in use
```bash
uvicorn app.main:app --reload --port 8001
```

### Reset database
```bash
# Delete the database file
rm uc_cookbook.db

# Re-run migrations
alembic upgrade head

# Re-seed if desired
python scripts/seed.py
```

### Import errors
Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

## Project Structure

```
uc-cookbook-backend/
├── app/                    # Main application code
│   ├── api/               # API routes and dependencies
│   ├── core/              # Configuration and security
│   ├── db/                # Database models and session
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── main.py            # FastAPI app
├── alembic/               # Database migrations
├── scripts/               # Utility scripts
├── tests/                 # Test suite
└── requirements.txt       # Dependencies
```

## API Endpoints

- `GET /health` - Health check
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `POST /auth/logout` - Logout
- `GET /recipes` - List recipes (with filters)
- `POST /recipes` - Create recipe (auth required)
- `GET /recipes/{id}` - Get recipe details
- `GET /cookbook` - Get saved recipes (auth required)
- `POST /cookbook/{recipe_id}` - Save recipe (auth required)
- `DELETE /cookbook/{recipe_id}` - Remove saved recipe (auth required)

## Environment Variables

See `.env.example` for all available configuration options.

**Important:** Change `SECRET_KEY` for production deployments!

## Next Steps

1. Explore the API documentation at `/docs`
2. Run the test suite to verify everything works
3. Start the frontend and test full integration
4. Review the main README.md for detailed documentation

---

**Need help?** Check the main README.md or contact the development team.
