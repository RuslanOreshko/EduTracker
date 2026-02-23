from dataclasses import dataclass
from datetime import date
from typing import Any


from dataclasses import dataclass
from datetime import date
from typing import Any, Optional


@dataclass(frozen=True, slots=True)
class ScheduleDayRawRow:
    schedule_date: date
    schedule_type: Optional[str]
    schedule_for_teachers_raw: str | dict[str, Any] | None


@dataclass(frozen=True, slots=True)
class ScheduleDayRow:
    schedule_date: date
    schedule_type: Optional[str]
    schedule_for_teachers: dict[str, Any]