"""
Setup script to initialize the UC Cookbook backend

This script:
1. Creates necessary directories
2. Sets up the database
3. Runs migrations
4. Optionally seeds the database
"""

import os
import sys
import subprocess


def main():
    print("🚀 UC Cookbook Backend Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Error: Python 3.11 or higher is required")
        sys.exit(1)
    
    print("✓ Python version check passed")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("⚠️  No .env file found. Copying from .env.example...")
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✓ Created .env file")
            print("⚠️  Remember to update SECRET_KEY in .env for production!")
        else:
            print("❌ .env.example not found")
            sys.exit(1)
    else:
        print("✓ .env file exists")
    
    # Show DB status vs models before migrating
    print("\n📋 Checking database (revision + schema vs models)...")
    try:
        subprocess.run(
            [sys.executable, "scripts/check_db.py"],
            check=False,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )
    except OSError as e:
        print(f"⚠️  Could not run check_db.py: {e}")

    # Run Alembic migrations
    print("\n📊 Running database migrations...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("✓ Database migrations completed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Alembic not found. Make sure dependencies are installed.")
        print("   Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Ask about seeding
    print("\n🌱 Database Seeding")
    seed = input("Do you want to seed the database with sample data? (y/n): ").lower()
    
    if seed == 'y':
        print("Seeding database...")
        try:
            result = subprocess.run([sys.executable, "scripts/seed.py"], check=True)
            print("✓ Database seeded successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Seeding failed: {e}")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📝 Next steps:")
    print("   1. Review .env file and update SECRET_KEY for production")
    print("   2. Run the development server:")
    print("      uvicorn app.main:app --reload")
    print("   3. Visit http://localhost:8000/docs for API documentation")
    print("\n   Demo credentials (if seeded):")
    print("      Email: demo@mail.uc.edu")
    print("      Password: demo123")


if __name__ == "__main__":
    main()
