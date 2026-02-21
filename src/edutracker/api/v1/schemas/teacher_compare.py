from pydantic import BaseModel
from datetime import date
from typing import Literal

# Назва групи/предмету, так кількість зайнять 
class NameCount(BaseModel):
    name: str
    count: float

# Ім'я викладача, загальна кількість зайнять, та список груп/предметів, які він вів
class TeacherCompareSide(BaseModel):
    name: str
    total_lessons: float
    by_subject_top: list[NameCount]
    by_group_top: list[NameCount]
 
# Різниця між викладачами
class ComparisonBlock(BaseModel):
    winner: Literal["teacher_a", "teacher_b", "tie"]
    difference_lesson: float
    defference_percent: float


class TeacherCompareOut(BaseModel):
    date_from: date
    date_to: date
    teacher_a: TeacherCompareSide
    teacher_b: TeacherCompareSide
    comparison: ComparisonBlock
    summary: str


