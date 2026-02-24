from pydantic import BaseModel
from datetime import date
from typing import Literal

class NameCount(BaseModel):
    name: str
    count: float

class TeacherCompareSide(BaseModel):
    name: str
    total_lessons: float
    by_subject_top: list[NameCount]
    by_group_top: list[NameCount]
 
class ComparisonBlock(BaseModel):
    winner: Literal["teacher_a", "teacher_b", "tie"]
    difference_lessons: float
    difference_percent: float


class TeacherCompareOut(BaseModel):
    date_from: date
    date_to: date
    teacher_a: TeacherCompareSide
    teacher_b: TeacherCompareSide
    comparison: ComparisonBlock
    summary: str


