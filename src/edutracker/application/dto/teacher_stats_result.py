from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class TeacherStatsResult():
    teacher: str
    date_from: date
    date_to: date

    total_lessons: float

    by_date: dict[date, float]
    by_group: dict[str, float]
    by_subject: dict[str, float]

    schedule_type_breakdown: dict[str, int] | None = None