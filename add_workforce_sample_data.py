#!/usr/bin/env python3
"""
Sample data script for the new simplified workforce module
"""

import sys
import os
from datetime import date, datetime
from decimal import Decimal

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.workforce import models

# Create all tables
models.Base.metadata.create_all(bind=engine)

def add_sample_workforce_data():
    """Add sample professions, workers, and project history"""
    db = SessionLocal()
    
    try:
        # Add Professions
        professions = [
            {
                "name": "Electrician",
                "description": "Licensed electrician for commercial and residential projects",
                "category": "Electrical"
            },
            {
                "name": "Plumber", 
                "description": "Licensed plumber for water and sewer systems",
                "category": "Plumbing"
            },
            {
                "name": "Carpenter",
                "description": "Skilled carpenter for framing and finishing work",
                "category": "Structural"
            },
            {
                "name": "Mason",
                "description": "Stone and brick mason for foundation and wall work",
                "category": "Structural"
            },
            {
                "name": "HVAC Technician",
                "description": "Heating, ventilation, and air conditioning specialist",
                "category": "HVAC"
            }
        ]
        
        profession_objects = []
        for prof_data in professions:
            # Check if profession already exists
            existing = db.query(models.Profession).filter(models.Profession.name == prof_data["name"]).first()
            if not existing:
                profession = models.Profession(**prof_data)
                db.add(profession)
                profession_objects.append(profession)
            else:
                profession_objects.append(existing)
        
        db.commit()
        
        # Add Workers
        workers = [
            {
                "worker_id": "ELC001",
                "first_name": "John",
                "last_name": "Smith",
                "phone_number": "+1-555-0101",
                "email": "john.smith@buildbuzz.com",
                "address": "123 Main St, Detroit, MI 48201",
                "profession_id": profession_objects[0].id,  # Electrician
                "skill_rating": Decimal("8.5"),
                "wage_rate": Decimal("35.50"),
                "availability": "Available"
            },
            {
                "worker_id": "ELC002", 
                "first_name": "Sarah",
                "last_name": "Johnson",
                "phone_number": "+1-555-0102",
                "email": "sarah.johnson@buildbuzz.com",
                "address": "456 Oak Ave, Detroit, MI 48202",
                "profession_id": profession_objects[0].id,  # Electrician
                "skill_rating": Decimal("9.2"),
                "wage_rate": Decimal("42.00"),
                "availability": "Assigned",
                "current_project_id": 1,
                "current_project_start_date": date(2024, 10, 1),
                "current_project_end_date": date(2024, 12, 15)
            },
            {
                "worker_id": "PLB001",
                "first_name": "Michael",
                "last_name": "Rodriguez",
                "phone_number": "+1-555-0103",
                "email": "michael.rodriguez@buildbuzz.com",
                "address": "789 Pine St, Detroit, MI 48203",
                "profession_id": profession_objects[1].id,  # Plumber
                "skill_rating": Decimal("7.8"),
                "wage_rate": Decimal("38.25"),
                "availability": "Available"
            },
            {
                "worker_id": "CAR001",
                "first_name": "David",
                "last_name": "Wilson",
                "phone_number": "+1-555-0104",
                "email": "david.wilson@buildbuzz.com",
                "address": "321 Elm St, Detroit, MI 48204",
                "profession_id": profession_objects[2].id,  # Carpenter
                "skill_rating": Decimal("9.0"),
                "wage_rate": Decimal("33.75"),
                "availability": "Assigned",
                "current_project_id": 2,
                "current_project_start_date": date(2024, 9, 15),
                "current_project_end_date": date(2024, 11, 30)
            },
            {
                "worker_id": "MAS001",
                "first_name": "Robert",
                "last_name": "Garcia",
                "phone_number": "+1-555-0105",
                "email": "robert.garcia@buildbuzz.com",
                "address": "654 Maple Dr, Detroit, MI 48205",
                "profession_id": profession_objects[3].id,  # Mason
                "skill_rating": Decimal("8.0"),
                "wage_rate": Decimal("36.00"),
                "availability": "On Leave"
            },
            {
                "worker_id": "HVC001",
                "first_name": "Lisa",
                "last_name": "Chen",
                "phone_number": "+1-555-0106",
                "email": "lisa.chen@buildbuzz.com",
                "address": "987 Cedar Ln, Detroit, MI 48206",
                "profession_id": profession_objects[4].id,  # HVAC Technician
                "skill_rating": Decimal("8.8"),
                "wage_rate": Decimal("40.50"),
                "availability": "Available"
            }
        ]
        
        worker_objects = []
        for worker_data in workers:
            # Check if worker already exists
            existing = db.query(models.Worker).filter(models.Worker.worker_id == worker_data["worker_id"]).first()
            if not existing:
                worker = models.Worker(**worker_data)
                db.add(worker)
                worker_objects.append(worker)
            else:
                worker_objects.append(existing)
        
        db.commit()
        
        # Add Project History
        project_histories = [
            {
                "worker_id": worker_objects[0].id,  # John Smith (Electrician)
                "project_id": 1,
                "start_date": date(2024, 1, 15),
                "end_date": date(2024, 3, 30),
                "role": "Lead Electrician",
                "status": "Completed",
                "performance_rating": Decimal("4.5"),
                "notes": "Excellent work on main electrical installation. Met all deadlines."
            },
            {
                "worker_id": worker_objects[0].id,  # John Smith (Electrician)
                "project_id": 2,
                "start_date": date(2024, 4, 1),
                "end_date": date(2024, 6, 15),
                "role": "Senior Electrician",
                "status": "Completed",
                "performance_rating": Decimal("4.2"),
                "notes": "Good performance, minor delays due to material shortage."
            },
            {
                "worker_id": worker_objects[1].id,  # Sarah Johnson (Electrician)
                "project_id": 1,
                "start_date": date(2024, 10, 1),
                "end_date": None,  # Currently active
                "role": "Lead Electrician",
                "status": "Active",
                "performance_rating": None,
                "notes": "Currently working on new office building electrical systems."
            },
            {
                "worker_id": worker_objects[2].id,  # Michael Rodriguez (Plumber)
                "project_id": 1,
                "start_date": date(2024, 2, 1),
                "end_date": date(2024, 4, 10),
                "role": "Senior Plumber",
                "status": "Completed",
                "performance_rating": Decimal("4.0"),
                "notes": "Solid performance on plumbing installation."
            },
            {
                "worker_id": worker_objects[3].id,  # David Wilson (Carpenter)
                "project_id": 2,
                "start_date": date(2024, 9, 15),
                "end_date": None,  # Currently active
                "role": "Lead Carpenter",
                "status": "Active",
                "performance_rating": None,
                "notes": "Working on custom millwork for luxury residential project."
            },
            {
                "worker_id": worker_objects[4].id,  # Robert Garcia (Mason)
                "project_id": 3,
                "start_date": date(2024, 3, 1),
                "end_date": date(2024, 5, 20),
                "role": "Master Mason",
                "status": "Completed",
                "performance_rating": Decimal("4.8"),
                "notes": "Outstanding stonework on building facade. Ahead of schedule."
            }
        ]
        
        for history_data in project_histories:
            # Check if history entry already exists
            existing = db.query(models.WorkerProjectHistory).filter(
                models.WorkerProjectHistory.worker_id == history_data["worker_id"],
                models.WorkerProjectHistory.project_id == history_data["project_id"],
                models.WorkerProjectHistory.start_date == history_data["start_date"]
            ).first()
            
            if not existing:
                history = models.WorkerProjectHistory(**history_data)
                db.add(history)
        
        db.commit()
        
        print("✅ Sample workforce data added successfully!")
        print(f"   • Added {len(professions)} professions")
        print(f"   • Added {len(workers)} workers")
        print(f"   • Added {len(project_histories)} project history entries")
        
        # Print summary
        print("\n📊 Workforce Summary:")
        total_workers = db.query(models.Worker).count()
        available_workers = db.query(models.Worker).filter(models.Worker.availability == "Available").count()
        assigned_workers = db.query(models.Worker).filter(models.Worker.availability == "Assigned").count()
        
        print(f"   • Total Workers: {total_workers}")
        print(f"   • Available Workers: {available_workers}")
        print(f"   • Assigned Workers: {assigned_workers}")
        
        # Print workers by profession
        print("\n👥 Workers by Profession:")
        for profession in profession_objects:
            count = db.query(models.Worker).filter(models.Worker.profession_id == profession.id).count()
            print(f"   • {profession.name}: {count} workers")
            
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Adding sample workforce data...")
    add_sample_workforce_data()