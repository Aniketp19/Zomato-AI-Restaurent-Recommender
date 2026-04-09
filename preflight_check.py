"""
Pre-flight check - Verify system is ready to run
"""
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    print("🔍 Checking dependencies...")
    required = ["fastapi", "uvicorn", "pydantic", "sqlite3", "requests"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT FOUND")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    return True

def check_database():
    """Check if database exists."""
    print("\n🔍 Checking database...")
    db_path = Path("data/restaurants.db")
    
    if not db_path.exists():
        print(f"  ❌ Database not found at: {db_path}")
        print("   Run: python -m src.phase1.load_data")
        return False
    
    # Check database size
    size_mb = db_path.stat().st_size / (1024 * 1024)
    print(f"  ✅ Database found ({size_mb:.2f} MB)")
    
    # Check if database has data
    try:
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM restaurants")
            count = cursor.fetchone()[0]
            print(f"  ✅ {count:,} restaurants loaded")
            
            if count == 0:
                print("  ⚠️  Database is empty!")
                return False
    except Exception as e:
        print(f"  ❌ Error reading database: {e}")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required keys."""
    print("\n🔍 Checking environment configuration...")
    env_path = Path(".env")
    
    if not env_path.exists():
        print(f"  ⚠️  .env file not found")
        print("   Copy .env.example to .env if available")
        print("   Or create .env with GROQ_API_KEY=your_key")
        return False
    
    print(f"  ✅ .env file exists")
    
    # Check for GROQ_API_KEY
    with open(env_path) as f:
        content = f.read()
        if "GROQ_API_KEY" in content:
            # Check if it's not empty
            for line in content.split('\n'):
                if line.startswith("GROQ_API_KEY"):
                    if "=" in line and line.split("=", 1)[1].strip():
                        print(f"  ✅ GROQ_API_KEY is set")
                    else:
                        print(f"  ⚠️  GROQ_API_KEY is empty")
                    break
        else:
            print(f"  ⚠️  GROQ_API_KEY not found in .env")
    
    return True

def check_port_available():
    """Check if port 8000 is available."""
    print("\n🔍 Checking if port 8000 is available...")
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8000))
    sock.close()
    
    if result == 0:
        print(f"  ⚠️  Port 8000 is already in use!")
        print("   Stop the existing server or use a different port")
        return False
    else:
        print(f"  ✅ Port 8000 is available")
        return True

def main():
    """Run all checks."""
    print("=" * 60)
    print("🚀 Zomato AI Recommender - Pre-flight Check")
    print("=" * 60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("Environment", check_env_file),
        ("Port", check_port_available),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append((name, check_func()))
        except Exception as e:
            print(f"\n  ❌ Error in {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ All checks passed! You're ready to start.")
        print("\nNext steps:")
        print("  1. Run: start_server.bat")
        print("  2. Open: index.html in your browser")
        print("  3. Test: Select a city and get recommendations!")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nSee START_HERE.md for troubleshooting guide.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
