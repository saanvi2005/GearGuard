"""
Seed script to populate database with sample data for testing
Run this script after initializing the database
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, init_db
from backend.models import MaintenanceTeam, Equipment, MaintenanceRequest
from datetime import date, datetime, timedelta

def seed_database():
    """Populate database with sample data"""
    init_db()
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(MaintenanceTeam).count() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        # Create Maintenance Teams
        team1 = MaintenanceTeam(
            name="Electrical Team",
            members="John Smith, Jane Doe, Bob Johnson"
        )
        team2 = MaintenanceTeam(
            name="Mechanical Team",
            members="Alice Williams, Charlie Brown, David Lee"
        )
        team3 = MaintenanceTeam(
            name="HVAC Team",
            members="Emma Davis, Frank Miller, Grace Wilson"
        )
        
        db.add(team1)
        db.add(team2)
        db.add(team3)
        db.commit()
        
        # Create Equipment
        equipment1 = Equipment(
            name="Industrial Generator",
            serial_number="GEN-001",
            department="Production",
            location="Building A - Floor 1",
            purchase_date=date(2020, 1, 15),
            warranty_expiry=date(2025, 1, 15),
            maintenance_team_id=team1.id,
            is_scrapped=False
        )
        
        equipment2 = Equipment(
            name="Conveyor Belt System",
            serial_number="CONV-002",
            department="Manufacturing",
            location="Building B - Floor 2",
            purchase_date=date(2019, 6, 20),
            warranty_expiry=date(2024, 6, 20),
            maintenance_team_id=team2.id,
            is_scrapped=False
        )
        
        equipment3 = Equipment(
            name="Central Air Conditioning Unit",
            serial_number="HVAC-003",
            department="Facilities",
            location="Building C - Roof",
            purchase_date=date(2021, 3, 10),
            warranty_expiry=date(2026, 3, 10),
            maintenance_team_id=team3.id,
            is_scrapped=False
        )
        
        equipment4 = Equipment(
            name="Hydraulic Press",
            serial_number="HYD-004",
            department="Production",
            location="Building A - Floor 2",
            purchase_date=date(2018, 9, 5),
            warranty_expiry=None,
            maintenance_team_id=team2.id,
            is_scrapped=False
        )
        
        db.add(equipment1)
        db.add(equipment2)
        db.add(equipment3)
        db.add(equipment4)
        db.commit()
        
        # Create Maintenance Requests
        today = date.today()
        
        request1 = MaintenanceRequest(
            title="Generator Oil Change",
            description="Routine oil change and filter replacement",
            equipment_id=equipment1.id,
            team_id=team1.id,
            technician="John Smith",
            request_type="Preventive",
            status="New",
            scheduled_date=today + timedelta(days=5),
            duration=2,
            created_at=datetime.utcnow()
        )
        
        request2 = MaintenanceRequest(
            title="Conveyor Belt Repair",
            description="Belt is making unusual noise, needs inspection",
            equipment_id=equipment2.id,
            team_id=team2.id,
            technician="Alice Williams",
            request_type="Corrective",
            status="In Progress",
            scheduled_date=today,
            duration=4,
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        
        request3 = MaintenanceRequest(
            title="AC Unit Filter Replacement",
            description="Monthly filter replacement",
            equipment_id=equipment3.id,
            team_id=team3.id,
            technician="Emma Davis",
            request_type="Preventive",
            status="Repaired",
            scheduled_date=today - timedelta(days=3),
            duration=1,
            created_at=datetime.utcnow() - timedelta(days=5)
        )
        
        request4 = MaintenanceRequest(
            title="Overdue Inspection",
            description="Quarterly inspection that was missed",
            equipment_id=equipment4.id,
            team_id=team2.id,
            technician="Charlie Brown",
            request_type="Preventive",
            status="New",
            scheduled_date=today - timedelta(days=10),  # Overdue
            duration=3,
            created_at=datetime.utcnow() - timedelta(days=15)
        )
        
        request5 = MaintenanceRequest(
            title="Generator Battery Check",
            description="Check battery voltage and connections",
            equipment_id=equipment1.id,
            team_id=team1.id,
            technician="Jane Doe",
            request_type="Preventive",
            status="New",
            scheduled_date=today + timedelta(days=15),
            duration=1,
            created_at=datetime.utcnow()
        )
        
        db.add(request1)
        db.add(request2)
        db.add(request3)
        db.add(request4)
        db.add(request5)
        db.commit()
        
        print("✓ Database seeded successfully!")
        print(f"  - Created {db.query(MaintenanceTeam).count()} teams")
        print(f"  - Created {db.query(Equipment).count()} equipment")
        print(f"  - Created {db.query(MaintenanceRequest).count()} maintenance requests")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

