from datetime import date
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TopTacherItem:
    teacher: str
    total_lessons: float


@dataclass(frozen=True, slots=True)
class TopTeachersResult:
    date_from: date
    date_to: date
    top: List[TopTacherItem]