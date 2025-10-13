from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TimesheetBase(BaseModel):
    user_id: int
    project_id: int
    clock_in_time: datetime
    clock_out_time: Optional[datetime] = None

class TimesheetCreate(TimesheetBase):
    pass

class Timesheet(TimesheetBase):
    id: int
    status: str

    class Config:
        orm_mode = True

