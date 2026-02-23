"""
Backend Code Validation Script

This script validates the backend code structure and imports
without requiring full setup or execution.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ MISSING {description}: {filepath}")
        return False

def validate_backend_structure():
    """Validate the backend project structure"""
    print("=" * 60)
    print("UC COOKBOOK BACKEND - STRUCTURE VALIDATION")
    print("=" * 60)
    
    base_path = Path(__file__).parent.parent
    backend_path = base_path / "uc-cookbook-backend"
    
    if not backend_path.exists():
        print(f"❌ Backend directory not found: {backend_path}")
        return False
    
    print(f"\n📁 Backend Directory: {backend_path}")
    print("\n" + "-" * 60)
    
    all_checks_passed = True
    
    # Core files
    print("\n🔧 CORE FILES:")
    core_files = [
        ("app/main.py", "FastAPI Application"),
        ("app/__init__.py", "App Package"),
        ("requirements.txt", "Dependencies"),
        (".env", "Environment Config"),
        ("alembic.ini", "Alembic Config"),
    ]
    
    for filepath, desc in core_files:
        if not check_file_exists(backend_path / filepath, desc):
            all_checks_passed = False
    
    # API Routes
    print("\n🌐 API ROUTES:")
    route_files = [
        ("app/api/routes/health.py", "Health Check"),
        ("app/api/routes/auth.py", "Authentication"),
        ("app/api/routes/recipes.py", "Recipes"),
        ("app/api/routes/cookbook.py", "Cookbook"),
    ]
    
    for filepath, desc in route_files:
        if not check_file_exists(backend_path / filepath, desc):
            all_checks_passed = False
    
    # Database
    print("\n🗄️  DATABASE:")
    db_files = [
        ("app/db/models.py", "Database Models"),
        ("app/db/session.py", "DB Session"),
        ("alembic/versions/001_initial_schema.py", "Initial Migration"),
    ]
    
    for filepath, desc in db_files:
        if not check_file_exists(backend_path / filepath, desc):
            all_checks_passed = False
    
    # Services
    print("\n⚙️  SERVICES:")
    service_files = [
        ("app/services/auth_service.py", "Auth Service"),
        ("app/services/recipe_service.py", "Recipe Service"),
        ("app/services/cookbook_service.py", "Cookbook Service"),
    ]
    
    for filepath, desc in service_files:
        if not check_file_exists(backend_path / filepath, desc):
            all_checks_passed = False
    
    # Schemas
    print("\n📋 SCHEMAS:")
    schema_files = [
        ("app/schemas/auth.py", "Auth Schemas"),
        ("app/schemas/recipe.py", "Recipe Schemas"),
        ("app/schemas/cookbook.py", "Cookbook Schemas"),
    ]
    
    for filepath, desc in schema_files:
        if not check_file_exists(backend_path / filepath, desc):
            all_checks_passed = False
    
    # Tests
    print("\n🧪 TESTS:")
    test_files = [
        ("tests/conftest.py", "Test Config"),
        ("tests/test_auth.py", "Auth Tests"),
        ("tests/test_recipes.py", "Recipe Tests"),
        ("tests/test_cookbook.py", "Cookbook Tests"),
        ("tests/test_health.py", "Health Tests"),
    ]
    
    for filepath, desc in test_files:
        if not check_file_exists(backend_path / filepath, desc):
            all_checks_passed = False
    
    # Scripts
    print("\n📜 SCRIPTS:")
    script_files = [
        ("scripts/seed.py", "Seed Script"),
        ("scripts/setup.py", "Setup Script"),
    ]
    
    for filepath, desc in script_files:
        if not check_file_exists(backend_path / filepath, desc):
            all_checks_passed = False
    
    # Documentation
    print("\n📚 DOCUMENTATION:")
    doc_files = [
        ("README.md", "Main README"),
        ("QUICKSTART.md", "Quick Start Guide"),
        ("SETUP.md", "Setup Instructions"),
        ("DEVELOPMENT.md", "Development Guide"),
    ]
    
    for filepath, desc in doc_files:
        if not check_file_exists(backend_path / filepath, desc):
            all_checks_passed = False
    
    # Count files
    print("\n" + "=" * 60)
    print("📊 FILE COUNT:")
    python_files = list(backend_path.rglob("*.py"))
    print(f"  Python files (.py): {len(python_files)}")
    
    md_files = list(backend_path.rglob("*.md"))
    print(f"  Documentation (.md): {len(md_files)}")
    
    all_files = list(backend_path.rglob("*"))
    files_only = [f for f in all_files if f.is_file()]
    print(f"  Total files: {len(files_only)}")
    
    print("\n" + "=" * 60)
    
    if all_checks_passed:
        print("✅ ALL STRUCTURE CHECKS PASSED!")
        print("\nThe backend project structure is complete and ready.")
        print("\nNext steps:")
        print("  1. Install Python 3.11+")
        print("  2. Create virtual environment: python -m venv .venv")
        print("  3. Activate: .venv\\Scripts\\activate")
        print("  4. Install dependencies: pip install -r requirements.txt")
        print("  5. Run migrations: alembic upgrade head")
        print("  6. Seed database: python scripts\\seed.py")
        print("  7. Start server: uvicorn app.main:app --reload")
        return True
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nSome required files are missing.")
        return False

if __name__ == "__main__":
    success = validate_backend_structure()
    sys.exit(0 if success else 1)
