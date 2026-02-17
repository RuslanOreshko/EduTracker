from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional
import json


class ScheduleRecordOut(BaseModel):
    teacher: str 
    date_from: date
    date_to: date

    total_lessons: int

    by_date: Dict[date, int]
    by_group: Dict[str, int]
    by_subject: Dict[str, int]

    schedule_type_breakdown: Optional[dict[str, int]] = None
