from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from datetime import datetime

def clock_in(db: Session, user_id: int, project_id: int):
    db_timesheet = models.Timesheet(
        user_id=user_id,
        project_id=project_id,
        clock_in_time=datetime.now(),
        status="Clocked In"
    )
    db.add(db_timesheet)
    db.commit()
    db.refresh(db_timesheet)
    return db_timesheet

def clock_out(db: Session, timesheet_id: int):
    db_timesheet = db.query(models.Timesheet).filter(models.Timesheet.id == timesheet_id).first()
    if db_timesheet and db_timesheet.status == "Clocked In":
        db_timesheet.clock_out_time = datetime.now()
        db_timesheet.status = "Submitted"
        db.commit()
        db.refresh(db_timesheet)
    return db_timesheet

def approve_timesheet(db: Session, timesheet_id: int, approver_id: int):
    db_timesheet = db.query(models.Timesheet).filter(models.Timesheet.id == timesheet_id).first()
    if db_timesheet and db_timesheet.status == "Submitted":
        db_timesheet.status = "Approved"
        db.commit()
        db.refresh(db_timesheet)

        # Calculate hours worked and create LaborCost entry
        if db_timesheet.clock_in_time and db_timesheet.clock_out_time:
            duration = db_timesheet.clock_out_time - db_timesheet.clock_in_time
            hours_worked = duration.total_seconds() / 3600
            
            # Placeholder for actual wage rate lookup
            wage_rate = 50.0 
            amount = hours_worked * wage_rate

            labor_cost = models.LaborCost(
                project_id=db_timesheet.project_id,
                amount=amount
            )
            db.add(labor_cost)
            db.commit()
            db.refresh(labor_cost)

    return db_timesheet

