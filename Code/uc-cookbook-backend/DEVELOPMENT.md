# Development Workflow Guide

## Daily Development

### Starting Development

1. **Activate virtual environment**
   ```bash
   .venv\Scripts\activate  # Windows
   ```

2. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **In another terminal, start the frontend**
   ```bash
   cd ../uc-cookbook-frontend
   npm run dev
   ```

### Testing Your Changes

#### Run all tests
```bash
pytest
```

#### Run specific test file
```bash
pytest tests/test_auth.py -v
```

#### Run with coverage
```bash
pytest --cov=app --cov-report=html
```

#### Test a specific endpoint manually
```bash
# Using curl (or use Postman/Insomnia)
curl http://localhost:8000/health

# Using Python requests
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

## Database Changes

### Creating a new model or modifying existing

1. **Edit the model in** `app/db/models.py`

2. **Create a migration**
   ```bash
   alembic revision --autogenerate -m "Add new field to User model"
   ```

3. **Review the generated migration** in `alembic/versions/`

4. **Apply the migration**
   ```bash
   alembic upgrade head
   ```

5. **If needed, update seed script** `scripts/seed.py`

### Reset database (for development)

```bash
# Delete database
rm uc_cookbook.db

# Re-create with migrations
alembic upgrade head

# Re-seed
python scripts/seed.py
```

## Adding New Features

### Adding a new API endpoint

1. **Create/update schema** in `app/schemas/`
   ```python
   # app/schemas/feature.py
   from pydantic import BaseModel
   
   class FeatureCreate(BaseModel):
       name: str
       value: int
   ```

2. **Add service logic** in `app/services/`
   ```python
   # app/services/feature_service.py
   class FeatureService:
       @staticmethod
       def create_feature(db, data):
           # Business logic here
           pass
   ```

3. **Create route** in `app/api/routes/`
   ```python
   # app/api/routes/feature.py
   from fastapi import APIRouter, Depends
   
   router = APIRouter(prefix="/features", tags=["Features"])
   
   @router.post("")
   async def create_feature(...):
       pass
   ```

4. **Register router** in `app/main.py`
   ```python
   from app.api.routes import feature
   app.include_router(feature.router)
   ```

5. **Write tests** in `tests/test_feature.py`

6. **Test manually** at http://localhost:8000/docs

## Code Quality

### Before committing

```bash
# Run tests
pytest

# Check test coverage
pytest --cov=app

# Format code (if using black)
black app/ tests/

# Lint code (if using ruff)
ruff check app/ tests/
```

## API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Use these to:
- Test endpoints interactively
- View request/response schemas
- Generate API client code

## Debugging

### Using print statements
```python
print(f"Debug: user_id = {user_id}")
```

### Using Python debugger
```python
import pdb; pdb.set_trace()  # Add breakpoint
```

### View SQL queries
Set in `.env`:
```
DATABASE_ECHO=True
```

Or temporarily in code:
```python
from sqlalchemy import create_engine
engine = create_engine(url, echo=True)
```

### Check logs
FastAPI logs appear in the terminal where you ran `uvicorn`

## Common Tasks

### Add new Python dependency
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

### Update environment variable
1. Edit `.env` file
2. Restart the server

### Check database contents
```bash
# Using Python
python
>>> from app.db.session import SessionLocal
>>> from app.db.models import User
>>> db = SessionLocal()
>>> users = db.query(User).all()
>>> for u in users: print(u.email)
```

Or use a SQLite browser tool like DB Browser for SQLite.

## Performance Tips

### Database queries
- Use eager loading for relationships: `.options(joinedload(...))`
- Add indexes for frequently queried fields
- Use pagination for large result sets

### Caching
Consider caching for:
- Recipe lists
- User profile data
- Static content

## Security Checklist

- [ ] Never commit `.env` file
- [ ] Use strong SECRET_KEY in production
- [ ] Validate all user inputs (Pydantic does this)
- [ ] Use HTTPS in production (set `secure=True` for cookies)
- [ ] Keep dependencies updated
- [ ] Review CORS settings for production

## Deployment Preparation

### Before deploying to production:

1. **Update environment variables**
   - Change `SECRET_KEY`
   - Set `DEBUG=False`
   - Update `CORS_ORIGINS`
   - Use PostgreSQL instead of SQLite

2. **Security settings**
   - Enable HTTPS
   - Set `secure=True` for cookies
   - Review CORS policy

3. **Performance**
   - Use multiple workers: `--workers 4`
   - Add caching layer
   - Optimize database queries

4. **Monitoring**
   - Set up logging
   - Add health check monitoring
   - Track error rates

## Useful Resources

- FastAPI docs: https://fastapi.tiangolo.com/
- SQLAlchemy docs: https://docs.sqlalchemy.org/
- Alembic docs: https://alembic.sqlalchemy.org/
- Pydantic docs: https://docs.pydantic.dev/

## Getting Help

1. Check the API docs at `/docs`
2. Review test files for usage examples
3. Check FastAPI documentation
4. Ask the development team

---

Happy coding! 🚀
