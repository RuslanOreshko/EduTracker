from datetime import date
from pydantic import BaseModel
from typing import Optional


class AvgLessonsOut(BaseModel):
    date_from: date
    date_to: date
    teacher: Optional[str] = None
    
    awg_lessons_per_workday: float
    workdays_count: int
    total_lessons: float