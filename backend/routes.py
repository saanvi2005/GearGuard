import sys
import os

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, BASE_DIR)

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel
from backend.database import get_db
from backend.models import Equipment, MaintenanceTeam, MaintenanceRequest

router = APIRouter()

# Set templates directory with absolute path
templates_dir = os.path.join(BASE_DIR, "frontend", "templates")
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    print(f"ERROR: Templates directory not found at {templates_dir}")
    raise FileNotFoundError(f"Templates directory not found at {templates_dir}")

# Pydantic models for request/response
class EquipmentCreate(BaseModel):
    name: str
    serial_number: str
    department: str
    location: str
    purchase_date: str
    warranty_expiry: Optional[str] = None
    maintenance_team_id: int
    is_scrapped: bool = False

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    purchase_date: Optional[str] = None
    warranty_expiry: Optional[str] = None
    maintenance_team_id: Optional[int] = None
    is_scrapped: Optional[bool] = None

class TeamCreate(BaseModel):
    name: str
    members: str

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    members: Optional[str] = None

class MaintenanceRequestCreate(BaseModel):
    title: str
    description: Optional[str] = None
    equipment_id: int
    technician: Optional[str] = None
    request_type: str
    scheduled_date: Optional[str] = None
    duration: Optional[int] = None

class MaintenanceRequestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technician: Optional[str] = None
    request_type: Optional[str] = None
    status: Optional[str] = None
    scheduled_date: Optional[str] = None
    duration: Optional[int] = None

# Helper function to parse date
def parse_date(date_str: Optional[str]) -> Optional[date]:
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return None
    return None

# Equipment Routes
@router.get("/api/equipment", response_model=List[dict])
def get_equipment(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).offset(skip).limit(limit).all()
    result = []
    for eq in equipment:
        maintenance_count = db.query(MaintenanceRequest).filter(MaintenanceRequest.equipment_id == eq.id).count()
        result.append({
            "id": eq.id,
            "name": eq.name,
            "serial_number": eq.serial_number,
            "department": eq.department,
            "location": eq.location,
            "purchase_date": str(eq.purchase_date),
            "warranty_expiry": str(eq.warranty_expiry) if eq.warranty_expiry else None,
            "maintenance_team_id": eq.maintenance_team_id,
            "is_scrapped": eq.is_scrapped,
            "maintenance_count": maintenance_count
        })
    return result

@router.get("/api/equipment/{equipment_id}", response_model=dict)
def get_equipment_by_id(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    maintenance_count = db.query(MaintenanceRequest).filter(MaintenanceRequest.equipment_id == equipment.id).count()
    return {
        "id": equipment.id,
        "name": equipment.name,
        "serial_number": equipment.serial_number,
        "department": equipment.department,
        "location": equipment.location,
        "purchase_date": str(equipment.purchase_date),
        "warranty_expiry": str(equipment.warranty_expiry) if equipment.warranty_expiry else None,
        "maintenance_team_id": equipment.maintenance_team_id,
        "is_scrapped": equipment.is_scrapped,
        "maintenance_count": maintenance_count
    }

@router.post("/api/equipment", response_model=dict)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    # Check if serial number already exists
    existing = db.query(Equipment).filter(Equipment.serial_number == equipment.serial_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Serial number already exists")
    
    db_equipment = Equipment(
        name=equipment.name,
        serial_number=equipment.serial_number,
        department=equipment.department,
        location=equipment.location,
        purchase_date=parse_date(equipment.purchase_date),
        warranty_expiry=parse_date(equipment.warranty_expiry),
        maintenance_team_id=equipment.maintenance_team_id,
        is_scrapped=equipment.is_scrapped
    )
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return {
        "id": db_equipment.id,
        "name": db_equipment.name,
        "serial_number": db_equipment.serial_number,
        "department": db_equipment.department,
        "location": db_equipment.location,
        "purchase_date": str(db_equipment.purchase_date),
        "warranty_expiry": str(db_equipment.warranty_expiry) if db_equipment.warranty_expiry else None,
        "maintenance_team_id": db_equipment.maintenance_team_id,
        "is_scrapped": db_equipment.is_scrapped
    }

@router.put("/api/equipment/{equipment_id}", response_model=dict)
def update_equipment(equipment_id: int, equipment: EquipmentUpdate, db: Session = Depends(get_db)):
    db_equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    if equipment.serial_number and equipment.serial_number != db_equipment.serial_number:
        existing = db.query(Equipment).filter(Equipment.serial_number == equipment.serial_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="Serial number already exists")
    
    update_data = equipment.dict(exclude_unset=True)
    if "purchase_date" in update_data:
        update_data["purchase_date"] = parse_date(update_data["purchase_date"])
    if "warranty_expiry" in update_data:
        update_data["warranty_expiry"] = parse_date(update_data["warranty_expiry"])
    
    for key, value in update_data.items():
        setattr(db_equipment, key, value)
    
    db.commit()
    db.refresh(db_equipment)
    return {
        "id": db_equipment.id,
        "name": db_equipment.name,
        "serial_number": db_equipment.serial_number,
        "department": db_equipment.department,
        "location": db_equipment.location,
        "purchase_date": str(db_equipment.purchase_date),
        "warranty_expiry": str(db_equipment.warranty_expiry) if db_equipment.warranty_expiry else None,
        "maintenance_team_id": db_equipment.maintenance_team_id,
        "is_scrapped": db_equipment.is_scrapped
    }

@router.delete("/api/equipment/{equipment_id}")
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    db.delete(equipment)
    db.commit()
    return {"message": "Equipment deleted successfully"}

# Team Routes
@router.get("/api/teams", response_model=List[dict])
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(MaintenanceTeam).all()
    return [{"id": t.id, "name": t.name, "members": t.members} for t in teams]

@router.get("/api/teams/{team_id}", response_model=dict)
def get_team_by_id(team_id: int, db: Session = Depends(get_db)):
    team = db.query(MaintenanceTeam).filter(MaintenanceTeam.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"id": team.id, "name": team.name, "members": team.members}

@router.post("/api/teams", response_model=dict)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    existing = db.query(MaintenanceTeam).filter(MaintenanceTeam.name == team.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Team name already exists")
    
    db_team = MaintenanceTeam(name=team.name, members=team.members)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return {"id": db_team.id, "name": db_team.name, "members": db_team.members}

@router.put("/api/teams/{team_id}", response_model=dict)
def update_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db)):
    db_team = db.query(MaintenanceTeam).filter(MaintenanceTeam.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    update_data = team.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_team, key, value)
    
    db.commit()
    db.refresh(db_team)
    return {"id": db_team.id, "name": db_team.name, "members": db_team.members}

@router.delete("/api/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(MaintenanceTeam).filter(MaintenanceTeam.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}

# Maintenance Request Routes
@router.get("/api/maintenance-requests", response_model=List[dict])
def get_maintenance_requests(db: Session = Depends(get_db)):
    requests = db.query(MaintenanceRequest).all()
    result = []
    today = date.today()
    for req in requests:
        is_overdue = False
        if req.scheduled_date and req.status not in ["Repaired", "Scrap"]:
            is_overdue = req.scheduled_date < today
        
        result.append({
            "id": req.id,
            "title": req.title,
            "description": req.description,
            "equipment_id": req.equipment_id,
            "team_id": req.team_id,
            "technician": req.technician,
            "request_type": req.request_type,
            "status": req.status,
            "scheduled_date": str(req.scheduled_date) if req.scheduled_date else None,
            "duration": req.duration,
            "created_at": req.created_at.isoformat() if req.created_at else None,
            "is_overdue": is_overdue
        })
    return result

@router.get("/api/maintenance-requests/{request_id}", response_model=dict)
def get_maintenance_request_by_id(request_id: int, db: Session = Depends(get_db)):
    req = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    
    today = date.today()
    is_overdue = False
    if req.scheduled_date and req.status not in ["Repaired", "Scrap"]:
        is_overdue = req.scheduled_date < today
    
    return {
        "id": req.id,
        "title": req.title,
        "description": req.description,
        "equipment_id": req.equipment_id,
        "team_id": req.team_id,
        "technician": req.technician,
        "request_type": req.request_type,
        "status": req.status,
        "scheduled_date": str(req.scheduled_date) if req.scheduled_date else None,
        "duration": req.duration,
        "created_at": req.created_at.isoformat() if req.created_at else None,
        "is_overdue": is_overdue
    }

@router.post("/api/maintenance-requests", response_model=dict)
def create_maintenance_request(request: MaintenanceRequestCreate, db: Session = Depends(get_db)):
    # Get equipment to auto-fill team_id
    equipment = db.query(Equipment).filter(Equipment.id == request.equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    db_request = MaintenanceRequest(
        title=request.title,
        description=request.description,
        equipment_id=request.equipment_id,
        team_id=equipment.maintenance_team_id,  # Auto-filled from equipment
        technician=request.technician,
        request_type=request.request_type,
        scheduled_date=parse_date(request.scheduled_date),
        duration=request.duration,
        status="New"
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    # If status is Scrap, mark equipment as scrapped
    if request.request_type == "Preventive" and request.scheduled_date:
        scheduled = parse_date(request.scheduled_date)
        is_overdue = scheduled < date.today() if scheduled else False
    else:
        is_overdue = False
    
    return {
        "id": db_request.id,
        "title": db_request.title,
        "description": db_request.description,
        "equipment_id": db_request.equipment_id,
        "team_id": db_request.team_id,
        "technician": db_request.technician,
        "request_type": db_request.request_type,
        "status": db_request.status,
        "scheduled_date": str(db_request.scheduled_date) if db_request.scheduled_date else None,
        "duration": db_request.duration,
        "created_at": db_request.created_at.isoformat() if db_request.created_at else None,
        "is_overdue": is_overdue
    }

@router.put("/api/maintenance-requests/{request_id}", response_model=dict)
def update_maintenance_request(request_id: int, request: MaintenanceRequestUpdate, db: Session = Depends(get_db)):
    db_request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    
    update_data = request.dict(exclude_unset=True)
    if "scheduled_date" in update_data:
        update_data["scheduled_date"] = parse_date(update_data["scheduled_date"])
    
    for key, value in update_data.items():
        setattr(db_request, key, value)
    
    # If status is Scrap, mark equipment as scrapped
    if update_data.get("status") == "Scrap":
        equipment = db.query(Equipment).filter(Equipment.id == db_request.equipment_id).first()
        if equipment:
            equipment.is_scrapped = True
    
    db.commit()
    db.refresh(db_request)
    
    today = date.today()
    is_overdue = False
    if db_request.scheduled_date and db_request.status not in ["Repaired", "Scrap"]:
        is_overdue = db_request.scheduled_date < today
    
    return {
        "id": db_request.id,
        "title": db_request.title,
        "description": db_request.description,
        "equipment_id": db_request.equipment_id,
        "team_id": db_request.team_id,
        "technician": db_request.technician,
        "request_type": db_request.request_type,
        "status": db_request.status,
        "scheduled_date": str(db_request.scheduled_date) if db_request.scheduled_date else None,
        "duration": db_request.duration,
        "created_at": db_request.created_at.isoformat() if db_request.created_at else None,
        "is_overdue": is_overdue
    }

@router.delete("/api/maintenance-requests/{request_id}")
def delete_maintenance_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    db.delete(request)
    db.commit()
    return {"message": "Maintenance request deleted successfully"}

# Frontend Routes
@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    equipment_count = db.query(Equipment).count()
    requests_count = db.query(MaintenanceRequest).count()
    teams_count = db.query(MaintenanceTeam).count()
    
    # Count overdue requests
    today = date.today()
    overdue_count = db.query(MaintenanceRequest).filter(
        MaintenanceRequest.scheduled_date < today
    ).filter(
        ~MaintenanceRequest.status.in_(["Repaired", "Scrap"])
    ).count()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "equipment_count": equipment_count,
        "requests_count": requests_count,
        "teams_count": teams_count,
        "overdue_count": overdue_count
    })

@router.get("/equipment", response_class=HTMLResponse)
async def equipment_page(request: Request):
    return templates.TemplateResponse("equipment.html", {"request": request})

@router.get("/kanban", response_class=HTMLResponse)
async def kanban_page(request: Request):
    return templates.TemplateResponse("kanban.html", {"request": request})

@router.get("/calendar", response_class=HTMLResponse)
async def calendar_page(request: Request):
    return templates.TemplateResponse("calendar.html", {"request": request})

