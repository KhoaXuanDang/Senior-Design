# UC Cookbook Backend API

A FastAPI-based microservice backend for the UC Cookbook application - a recipe sharing platform for University of Cincinnati students.

## Features

- 🔐 JWT-based authentication with httpOnly cookies
- 📝 Full CRUD operations for recipes
- 📚 Personal cookbook management
- 🔍 Advanced recipe search and filtering
- 📊 OpenAPI documentation (Swagger UI)
- 🧪 Comprehensive test suite
- 🗄️ SQLite database with Alembic migrations

## Tech Stack

- **Framework**: FastAPI 0.109+
- **Server**: Uvicorn
- **Database**: SQLite with SQLAlchemy ORM
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose) + bcrypt
- **Testing**: pytest + httpx

## Project Structure

```
uc-cookbook-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   └── security.py         # JWT & password utilities
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py             # Base model imports
│   │   ├── models.py           # SQLAlchemy models
│   │   └── session.py          # Database session management
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py             # Auth request/response schemas
│   │   ├── recipe.py           # Recipe schemas
│   │   ├── cookbook.py         # Cookbook schemas
│   │   └── common.py           # Common/shared schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (auth, db)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py       # Health check endpoint
│   │       ├── auth.py         # Authentication routes
│   │       ├── recipes.py      # Recipe CRUD routes
│   │       └── cookbook.py     # Cookbook management routes
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py     # Authentication logic
│       ├── recipe_service.py   # Recipe business logic
│       └── cookbook_service.py # Cookbook business logic
├── alembic/
│   ├── versions/               # Migration files
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Test fixtures
│   ├── test_health.py
│   ├── test_auth.py
│   ├── test_recipes.py
│   └── test_cookbook.py
├── scripts/
│   └── seed.py                 # Database seeding script
├── alembic.ini                 # Alembic configuration
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (if not already done)

2. **Navigate to the backend directory**
   ```bash
   cd Senior-Design/Code/uc-cookbook-backend
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

4. **Activate the virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and update the `SECRET_KEY` (generate a secure random key):
   ```bash
   # Generate a secure secret key (run in Python):
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

7. **Initialize the database**
   ```bash
   alembic upgrade head
   ```

8. **Seed the database (optional)**
   ```bash
   python scripts/seed.py
   ```

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health
- `GET /health` - Health check

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (sets httpOnly cookie)
- `POST /auth/logout` - Logout (clears cookie)

### Recipes
- `GET /recipes` - List recipes (supports search, filtering, pagination)
- `POST /recipes` - Create recipe (auth required)
- `GET /recipes/{id}` - Get recipe details

### Cookbook
- `GET /cookbook` - Get saved recipes (auth required)
- `POST /cookbook/{recipe_id}` - Save recipe (auth required)
- `DELETE /cookbook/{recipe_id}` - Remove saved recipe (auth required)

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_auth.py -v
```

## Database Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

### View migration history

```bash
alembic history
```

## Seeded Demo Data

When you run `python scripts/seed.py`, the following test data is created:

**Demo User:**
- Email: `demo@mail.uc.edu`
- Password: `demo123`
- Username: `demo_user`

**Sample Recipes:**
- Various recipes with different difficulty levels and tags
- Pre-seeded with UC student favorites

## Development Notes

### Architecture

The backend follows a clean architecture pattern with clear separation of concerns:

- **Routes**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Models**: Database entities (SQLAlchemy)
- **Schemas**: Request/Response validation (Pydantic)
- **Dependencies**: Reusable components (auth, db session)

### Authentication Flow

1. User registers/logs in with email and password
2. Backend validates credentials and generates JWT
3. JWT stored in httpOnly cookie (secure, prevents XSS)
4. Frontend sends cookie automatically with each request
5. Backend validates JWT and extracts user info

### CORS Configuration

The API is configured to accept requests from `http://localhost:3000` (Next.js frontend) with credentials enabled.

## Common Issues

### Port Already in Use

If port 8000 is occupied:
```bash
uvicorn app.main:app --reload --port 8001
```

### Database Locked

SQLite may lock if multiple processes access it. Ensure only one instance is running.

### Import Errors

Make sure you're in the virtual environment and have installed all dependencies.

## License

MIT License - UC Cookbook Project

## Support

For issues or questions, please contact the development team.
