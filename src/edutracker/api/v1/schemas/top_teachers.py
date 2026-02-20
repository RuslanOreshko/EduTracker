from pydantic import BaseModel
from datetime import date
from typing import List


class TopTacherItem(BaseModel):
    teacher: str
    total_lessons: float


class TopTeachersOut(BaseModel):
    date_from: date
    date_to: date
    top: List[TopTacherItem]