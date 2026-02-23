# UC Cookbook - Backend & Frontend Integration Testing Guide

## ⚠️ Python Installation Required

Python 3.11+ needs to be installed to run the backend. If you don't have it:

### Quick Install Options:

**Option 1: Official Python Installer (Recommended)**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"

**Option 2: Windows Store**
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Get" to install

**Option 3: Chocolatey (Run as Administrator)**
```powershell
choco install python311 -y
```

### Verify Installation:
```powershell
python --version
# Should show: Python 3.11.x or 3.12.x
```

---

## 🚀 Complete Integration Test Guide

### Step 1: Setup Backend

```powershell
# Navigate to backend directory
cd C:\Users\Khoa.Dang\source\Code\Capstone\Senior-Design\Code\uc-cookbook-backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies (this may take 2-3 minutes)
pip install -r requirements.txt

# Initialize database
alembic upgrade head

# Seed with demo data
python scripts\seed.py

# Start backend server (keep this terminal open)
uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 2: Test Backend (New Terminal)

Open a new PowerShell terminal:

```powershell
# Test health endpoint
curl http://localhost:8000/health

# Expected: {"status":"ok"}

# Test API docs (open in browser)
start http://localhost:8000/docs
```

You should see the Swagger UI with all endpoints!

### Step 3: Start Frontend (New Terminal)

```powershell
# Navigate to frontend directory
cd C:\Users\Khoa.Dang\source\Code\Capstone\Senior-Design\Code\uc-cookbook-frontend

# Install dependencies (if not done)
npm install

# Start frontend dev server
npm run dev
```

**Expected Output:**
```
> uc-cookbook-frontend@0.1.0 dev
> next dev

  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Network:      http://x.x.x.x:3000

✓ Ready in Xs
```

### Step 4: Integration Testing

Open your browser to http://localhost:3000

#### Test 1: User Registration
1. Click "Register" or navigate to `/auth/register`
2. Fill in:
   - Email: `testuser@mail.uc.edu`
   - Username: `testuser`
   - Password: `test123`
3. Click "Register"
4. ✅ Should redirect and show you're logged in

#### Test 2: Browse Recipes
1. Navigate to home page or `/recipes`
2. ✅ Should see 10 seeded recipes:
   - Classic Mac and Cheese
   - UC Bearcat Burrito Bowl
   - Dorm Room Ramen Upgrade
   - And more...
3. ✅ Try search: type "ramen" in search box
4. ✅ Try filters: select "Easy" difficulty

#### Test 3: View Recipe Details
1. Click on any recipe card
2. ✅ Should navigate to `/recipes/[id]`
3. ✅ Should show:
   - Title
   - Description
   - Ingredients list
   - Step-by-step instructions
   - Tags, difficulty, time
   - Author info

#### Test 4: Create Recipe (Authenticated)
1. Make sure you're logged in
2. Navigate to `/recipes/contribute`
3. Fill in the form:
   - Title: "My Test Recipe"
   - Description: "Testing recipe creation"
   - Add 2-3 ingredients
   - Add 2-3 steps
   - Select difficulty
   - Set cooking time
   - Add tags (optional)
4. Click "Submit"
5. ✅ Should create recipe and show success

#### Test 5: Save to Cookbook
1. Browse recipes
2. Click "Save to Cookbook" on any recipe
3. ✅ Should show success message
4. Navigate to `/cookbook`
5. ✅ Should see saved recipe in your cookbook

#### Test 6: Remove from Cookbook
1. On cookbook page
2. Click "Remove" on a saved recipe
3. ✅ Should remove from your cookbook

#### Test 7: Login with Demo User
1. Logout (if logged in)
2. Navigate to `/auth/login`
3. Login with:
   - Email: `demo@mail.uc.edu`
   - Password: `demo123`
4. ✅ Should login successfully
5. ✅ Navigate to `/cookbook` - should see 3 pre-saved recipes

#### Test 8: Search & Filters
1. Go to recipes page
2. Test search:
   - Search "pasta" → should show Mac and Cheese, Lasagna
   - Search "cincinnati" → should show Cincinnati Chili
3. Test difficulty filter:
   - Select "Easy" → should filter recipes
   - Select "Medium" → should show different recipes
4. Test tags:
   - Click on a tag → should filter by that tag

---

## 🔍 Backend API Testing (Using Swagger UI)

Visit: http://localhost:8000/docs

### Test Authentication Flow:

1. **Register User**
   - POST `/auth/register`
   - Click "Try it out"
   - Body:
     ```json
     {
       "email": "api-test@mail.uc.edu",
       "username": "api_tester",
       "password": "password123"
     }
     ```
   - Execute
   - ✅ Should return 201 with user data

2. **Login**
   - POST `/auth/login`
   - Body:
     ```json
     {
       "email": "api-test@mail.uc.edu",
       "password": "password123"
     }
     ```
   - Execute
   - ✅ Should return 200 with user data and set cookie

3. **Create Recipe** (Requires login)
   - POST `/recipes`
   - Body:
     ```json
     {
       "title": "API Test Recipe",
       "description": "Testing via Swagger",
       "ingredients": ["ingredient 1", "ingredient 2"],
       "steps": ["step 1", "step 2"],
       "tags": ["test"],
       "time_minutes": 30,
       "difficulty": "easy"
     }
     ```
   - Execute
   - ✅ Should return 201 with recipe data

4. **Get Recipes**
   - GET `/recipes`
   - Try with parameters:
     - `search=pasta`
     - `difficulty=easy`
     - `limit=5&offset=0`
   - ✅ Should return paginated results

5. **Save to Cookbook**
   - POST `/cookbook/{recipe_id}`
   - Use a recipe ID from step 4
   - ✅ Should return 201

6. **Get Cookbook**
   - GET `/cookbook`
   - ✅ Should return your saved recipes

---

## 🧪 Running Backend Tests

```powershell
# Make sure virtual environment is activated
.venv\Scripts\activate

# Run all tests
pytest

# Run with detailed output
pytest -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=app --cov-report=html
```

**Expected Output:**
```
======================== test session starts ========================
collected 30+ items

tests/test_auth.py ........                                    [ 26%]
tests/test_cookbook.py .........                               [ 56%]
tests/test_health.py ..                                        [ 63%]
tests/test_recipes.py ..........                               [100%]

======================== 30 passed in X.XXs =========================
```

---

## 📊 What to Look For (Success Indicators)

### Backend Running Successfully:
- ✅ Server starts on port 8000
- ✅ `/health` returns `{"status": "ok"}`
- ✅ `/docs` shows Swagger UI
- ✅ No error messages in terminal
- ✅ Database file created: `uc_cookbook.db`

### Frontend Running Successfully:
- ✅ Server starts on port 3000
- ✅ No compilation errors
- ✅ Pages load without errors
- ✅ API calls succeed (check browser console)

### Integration Working:
- ✅ Can register/login users
- ✅ Can see recipes from backend
- ✅ Can create new recipes
- ✅ Can save/unsave to cookbook
- ✅ Search and filters work
- ✅ No CORS errors in browser console

---

## 🐛 Troubleshooting

### Backend Issues:

**"Port 8000 already in use"**
```powershell
uvicorn app.main:app --reload --port 8001
# Update frontend API_BASE_URL if needed
```

**"ModuleNotFoundError"**
```powershell
# Make sure virtual environment is activated
.venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

**"Database is locked"**
- Only run one backend instance
- Delete `uc_cookbook.db` and re-run migrations

**"Alembic not found"**
```powershell
pip install alembic
```

### Frontend Issues:

**"Failed to fetch"**
- Check backend is running on port 8000
- Check `lib/api.ts` has correct `API_BASE_URL`
- Check browser console for CORS errors

**"Connection refused"**
- Backend not running - start it first
- Check firewall settings

### CORS Errors:
- Make sure backend `.env` has:
  ```
  CORS_ORIGINS=http://localhost:3000
  ```
- Restart backend after changing `.env`

### Cookie Not Set:
- Check browser allows cookies
- Check that you're using `http://localhost:3000` (not 127.0.0.1)
- Check browser DevTools → Application → Cookies

---

## 📈 Performance Testing

### Load Testing (Optional):
```powershell
# Install httpx
pip install httpx

# Simple load test
python -c "import httpx; import time; start = time.time(); [httpx.get('http://localhost:8000/recipes') for _ in range(100)]; print(f'100 requests in {time.time()-start:.2f}s')"
```

---

## ✅ Integration Test Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can access Swagger UI at `/docs`
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Can logout
- [ ] Can view all recipes
- [ ] Can search recipes
- [ ] Can filter by difficulty
- [ ] Can filter by tags
- [ ] Can view recipe details
- [ ] Can create new recipe (when logged in)
- [ ] Can save recipe to cookbook
- [ ] Can view cookbook
- [ ] Can remove recipe from cookbook
- [ ] Demo user login works
- [ ] All 30+ backend tests pass
- [ ] No errors in browser console
- [ ] No CORS errors

---

## 🎉 Success Criteria

Your UC Cookbook application is working correctly when:

1. ✅ Backend serves API on http://localhost:8000
2. ✅ Frontend serves UI on http://localhost:3000
3. ✅ Users can register and login
4. ✅ Recipes display correctly
5. ✅ Search and filters work
6. ✅ Recipe creation works
7. ✅ Cookbook save/remove works
8. ✅ All tests pass
9. ✅ No console errors

---

## 📞 Quick Reference

**Backend URLs:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

**Frontend URLs:**
- Home: http://localhost:3000
- Recipes: http://localhost:3000/recipes
- Login: http://localhost:3000/auth/login
- Register: http://localhost:3000/auth/register
- Cookbook: http://localhost:3000/cookbook

**Demo Credentials:**
- Email: demo@mail.uc.edu
- Password: demo123

**Test Commands:**
```powershell
# Backend
cd Senior-Design/Code/uc-cookbook-backend
.venv\Scripts\activate
uvicorn app.main:app --reload

# Frontend  
cd Senior-Design/Code/uc-cookbook-frontend
npm run dev

# Tests
pytest
npm test  # (if frontend tests exist)
```

---

## 🚀 You're Ready!

Once Python is installed, the entire application can be up and running in **under 5 minutes**!

The backend and frontend are **fully integrated** and ready for development, testing, and demonstration.

Good luck! 🎓🍳
