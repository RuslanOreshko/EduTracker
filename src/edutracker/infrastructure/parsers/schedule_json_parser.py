import json
import logging
from typing import Any

from edutracker.application.interfaces.schedule_repository import ScheduleDayRawRow
from edutracker.application.dto.schedule_day import ScheduleDayRow


logger = logging.getLogger(__name__)


class ScheduleJsonParser:
    def parse_days(self, days: list[ScheduleDayRawRow]) -> list[ScheduleDayRow]:
        out: list[ScheduleDayRow] = []

        for day in days:
            raw = day.schedule_for_teachers_raw

            if not raw:
                continue

            sfg: Any = raw

            if isinstance(sfg, str):
                try:
                    sfg = json.loads(sfg)
                except json.JSONDecodeError:
                    logger.warning(
                        "Invalid schedule_for_teachers JSON, skipped",
                        extra={"schedule_date": str(day.schedule_date), "schedule_type": day.schedule_type},
                    )
                    continue

            if not isinstance(sfg, dict):
                logger.warning(
                    "schedule_for_teachers is not a dict, skipped",
                    extra={"schedule_date": str(day.schedule_date), "schedule_type": day.schedule_type, "type": type(sfg).__name__},
                )
                continue

            out.append(
                ScheduleDayRow(
                    schedule_date=day.schedule_date,
                    schedule_type=day.schedule_type,
                    schedule_for_teachers=sfg,
                )
            )

        return out
