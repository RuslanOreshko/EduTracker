from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional
import json


class ScheduleRecordOut(BaseModel):
    teacher: str 
    date_from: date
    date_to: date

    total_lessons: float

    by_date: Dict[date, float]
    by_group: Dict[str, float]
    by_subject: Dict[str, float]

    schedule_type_breakdown: Optional[dict[str, int]] = None
