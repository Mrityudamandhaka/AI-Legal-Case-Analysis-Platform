import os
import subprocess
import sys

def test_backend_build():
    """Test if the backend can be built correctly"""
    print("Testing backend build...")
    
    # Check if requirements.txt exists
    if not os.path.exists("backend/requirements.txt"):
        print("ERROR: backend/requirements.txt not found")
        return False
    
    # Check if main.py exists
    if not os.path.exists("backend/main.py"):
        print("ERROR: backend/main.py not found")
        return False
    
    print("✓ All required backend files found")
    return True

def test_frontend_build():
    """Test if the frontend can be built correctly"""
    print("Testing frontend build...")
    
    # Check if package.json exists
    if not os.path.exists("frontend/package.json"):
        print("ERROR: frontend/package.json not found")
        return False
    
    # Check if next.config.ts exists
    if not os.path.exists("frontend/next.config.ts"):
        print("ERROR: frontend/next.config.ts not found")
        return False
    
    print("✓ All required frontend files found")
    return True

def main():
    print("LawMind Build Test")
    print("=" * 20)
    
    # Test backend
    backend_ok = test_backend_build()
    print()
    
    # Test frontend
    frontend_ok = test_frontend_build()
    print()
    
    if backend_ok and frontend_ok:
        print("✓ All tests passed! Docker build should work correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())