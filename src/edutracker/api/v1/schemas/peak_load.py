from pydantic import BaseModel
from datetime import date
from typing import Optional


# Максимально нагружений день
class PeakDayOut(BaseModel):
    date: date
    total_lessons: float


class PeakWeekOut(BaseModel):
    year: int
    week: int
    date_from: date
    date_to: date
    total_lessons: float


class PeakMonthOut(BaseModel):
    year: int
    month: int
    total_lessons: float


class TeacherPeakLoadOut(BaseModel):
    teacher: str
    date_from: date
    date_to: date
    peak_day: Optional[PeakDayOut] = None
    peak_week: Optional[PeakWeekOut] = None
    peak_month: Optional[PeakMonthOut] = None