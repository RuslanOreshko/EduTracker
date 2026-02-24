from typing import Literal
from datetime import date
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NameCountResult:
    name: str
    count: float

@dataclass(frozen=True, slots=True)
class TeacherCompareSideResult:
    name: str
    total_lessons: float
    by_subject_top: list[NameCountResult]
    by_group_top: list[NameCountResult]
 
@dataclass(frozen=True, slots=True)
class ComparisonBlockResult:
    winner: Literal["teacher_a", "teacher_b", "tie"]
    difference_lessons: float
    difference_percent: float

@dataclass(frozen=True, slots=True)
class TeacherCompareResult:
    date_from: date
    date_to: date
    teacher_a: TeacherCompareSideResult
    teacher_b: TeacherCompareSideResult
    comparison: ComparisonBlockResult
    summary: str