from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class PeakDayOut:
    date: date
    total_lessons: float


@dataclass(frozen=True, slots=True)
class PeakWeekOut:
    year: int
    week: int
    date_from: date
    date_to: date
    total_lessons: float


@dataclass(frozen=True, slots=True)
class PeakMonthOut:
    year: int
    month: int
    total_lessons: float


@dataclass(frozen=True, slots=True)
class TeacherPeakLoadResult:
    teacher: str
    date_from: date
    date_to: date
    peak_day: PeakDayOut | None = None
    peak_week: PeakWeekOut | None = None
    peak_month: PeakMonthOut | None = None