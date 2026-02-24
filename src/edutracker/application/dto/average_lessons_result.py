from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class AverageLessonsResult:
    date_from: date
    date_to: date
    teacher: str | None

    avg_lessons_per_workday: float
    workdays_count: int
    total_lessons: float