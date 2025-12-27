# Quick Start Guide - GearGuard

## Step-by-Step Instructions

### 1. Open Terminal/PowerShell
Navigate to the project directory:
```bash
cd C:\Users\saanvi\OneDrive\Desktop\gearGuard
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. (Optional) Add Sample Data
```bash
python backend/seed_data.py
```

### 6. Run the Application

**Option 1: Using the run script (Recommended - Easiest)**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn backend.main:app --reload
```

**Option 3: Using Python module syntax**
```bash
python -m uvicorn backend.main:app --reload
```

**Note:** Make sure you're in the project root directory (where `run.py` is located) when running these commands.

### 7. Access the Application

Once you see "Database initialized!" and the server starts:

- **Web Interface**: Open your browser and go to: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health`

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, you can change it:
```bash
uvicorn backend.main:app --reload --port 8001
```

### Module Not Found Errors
Make sure you're in the project root directory and the virtual environment is activated.

### Database Issues
If you encounter database errors, delete `gearGuard.db` and restart the application (it will recreate the database).

## What to Expect

1. The server will start and show "Database initialized!"
2. You'll see Uvicorn running on `http://0.0.0.0:8000`
3. Open `http://localhost:8000` in your browser
4. You'll see the Dashboard with statistics
5. Navigate using the top menu to:
   - Dashboard
   - Equipment
   - Kanban Board
   - Calendar

## First Steps After Starting

1. **Create a Team** (via API or by adding equipment - team will be auto-created)
2. **Add Equipment** - Click "Add Equipment" button
3. **Create Maintenance Request** - Go to Kanban Board and click "Create Request"
4. **View Calendar** - See preventive maintenance scheduled

Enjoy using GearGuard! 🛡️

