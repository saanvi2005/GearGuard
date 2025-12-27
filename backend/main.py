import sys
import os

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.routes import router

app = FastAPI(title="GearGuard Maintenance Management System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files with absolute path
static_dir = os.path.join(BASE_DIR, "frontend", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"WARNING: Static directory not found at {static_dir}")

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
        templates_dir = os.path.join(BASE_DIR, "frontend", "templates")
        print("✓ Database initialized successfully!")
        print(f"✓ Project root: {BASE_DIR}")
        print(f"✓ Static files: {static_dir if os.path.exists(static_dir) else 'NOT FOUND'}")
        print(f"✓ Templates: {templates_dir if os.path.exists(templates_dir) else 'NOT FOUND'}")
    except Exception as e:
        print(f"ERROR during startup: {e}")
        raise

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "GearGuard API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

