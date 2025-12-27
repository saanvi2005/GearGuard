"""
Quick start script for GearGuard
Run this from the project root directory
"""
import sys
import os

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Add project root to Python path
sys.path.insert(0, PROJECT_ROOT)

# Change to project root directory
os.chdir(PROJECT_ROOT)

import uvicorn

def check_dependencies():
    """Check if required dependencies are installed"""
    required_modules = ['fastapi', 'uvicorn', 'sqlalchemy', 'jinja2']
    missing = []
    
    for module in required_modules:
        try:
            mod = __import__(module)
            # Check SQLAlchemy version for Python 3.13 compatibility
            if module == 'sqlalchemy':
                import sys
                if sys.version_info >= (3, 13):
                    try:
                        version = mod.__version__
                        major, minor = map(int, version.split('.')[:2])
                        if major < 2 or (major == 2 and minor < 36):
                            print("=" * 60)
                            print("WARNING: Python 3.13 detected!")
                            print(f"Your SQLAlchemy version ({version}) may not be compatible with Python 3.13")
                            print("\nPlease upgrade SQLAlchemy:")
                            print("  pip install --upgrade sqlalchemy>=2.0.36")
                            print("\nOr use Python 3.11 or 3.12 instead")
                            print("See FIX_PYTHON313.md for more details")
                            print("=" * 60)
                            response = input("\nContinue anyway? (y/n): ").lower()
                            if response != 'y':
                                sys.exit(1)
                    except (ValueError, AttributeError):
                        pass
        except ImportError:
            missing.append(module)
    
    if missing:
        print("=" * 60)
        print("ERROR: Missing required dependencies!")
        print(f"Please install: {', '.join(missing)}")
        print("\nRun this command to install all dependencies:")
        print("  pip install -r requirements.txt")
        print("=" * 60)
        sys.exit(1)

def check_project_structure():
    """Verify project structure is correct"""
    required_dirs = [
        'backend',
        'frontend',
        'frontend/templates',
        'frontend/static',
        'frontend/static/css',
        'frontend/static/js'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = os.path.join(PROJECT_ROOT, dir_path)
        if not os.path.exists(full_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print("=" * 60)
        print("WARNING: Some directories are missing:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}")
        print("=" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("GearGuard Maintenance Management System")
    print("=" * 60)
    
    # Check dependencies
    check_dependencies()
    
    # Check project structure
    check_project_structure()
    
    print("\nStarting server...")
    print(f"Project root: {PROJECT_ROOT}")
    print("\nAccess the application at:")
    print("  → Web Interface: http://localhost:8000")
    print("  → API Docs: http://localhost:8000/docs")
    print("  → Health Check: http://localhost:8000/api/health")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    try:
        uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the project root directory")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check if port 8000 is already in use")
        sys.exit(1)

