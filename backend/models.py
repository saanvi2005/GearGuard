import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, date
import enum
from backend.database import Base

class MaintenanceTeam(Base):
    __tablename__ = "maintenance_teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    members = Column(Text)  # Comma-separated list of technicians
    
    # Relationships
    equipment = relationship("Equipment", back_populates="team")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="team")

class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    serial_number = Column(String, unique=True, nullable=False, index=True)
    department = Column(String, nullable=False)
    location = Column(String, nullable=False)
    purchase_date = Column(Date, nullable=False)
    warranty_expiry = Column(Date)
    maintenance_team_id = Column(Integer, ForeignKey("maintenance_teams.id"), nullable=False)
    is_scrapped = Column(Boolean, default=False)
    
    # Relationships
    team = relationship("MaintenanceTeam", back_populates="equipment")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="equipment", cascade="all, delete-orphan")

class RequestType(str, enum.Enum):
    CORRECTIVE = "Corrective"
    PREVENTIVE = "Preventive"

class RequestStatus(str, enum.Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    REPAIRED = "Repaired"
    SCRAP = "Scrap"

class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("maintenance_teams.id"), nullable=False)
    technician = Column(String)
    request_type = Column(String, nullable=False)  # Corrective or Preventive
    status = Column(String, nullable=False, default="New")  # New, In Progress, Repaired, Scrap
    scheduled_date = Column(Date)
    duration = Column(Integer)  # Duration in hours
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_requests")
    team = relationship("MaintenanceTeam", back_populates="maintenance_requests")

