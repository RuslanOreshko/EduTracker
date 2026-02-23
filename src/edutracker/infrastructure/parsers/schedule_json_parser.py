import json
import logging
from typing import Any

from edutracker.application.interfaces.schedule_repository import ScheduleDayRawRow
from edutracker.application.dto.schedule_day import ScheduleDayRow


logger = logging.getLogger(__name__)


class ScheduleJsonParser:
    def parse_days(self, days: list[ScheduleDayRawRow]) -> list[ScheduleDayRow]:
        out: list[ScheduleDayRow] = []

        total = len(days)
        parsed_ok = 0
        empty = 0
        invalid_json = 0
        invalid_type = 0

        for day in days:
            raw = day.schedule_for_teachers_raw

            if not raw:
                empty += 1
                continue

            sfg: Any = raw

            if isinstance(sfg, str):
                try:
                    sfg = json.loads(sfg)
                except json.JSONDecodeError:
                    invalid_json += 1
                    logger.warning(
                        "Invalid schedule_for_teachers JSON, skipped",
                        extra={
                            "schedule_date": str(day.schedule_date),
                            "schedule_type": day.schedule_type,
                        },
                    )
                    continue

            if not isinstance(sfg, dict):
                invalid_type += 1
                logger.warning(
                    "schedule_for_teachers is not a dict, skipped",
                    extra={
                        "schedule_date": str(day.schedule_date),
                        "schedule_type": day.schedule_type,
                        "value_type": type(sfg).__name__,
                    },
                )
                continue

            parsed_ok += 1
            out.append(
                ScheduleDayRow(
                    schedule_date=day.schedule_date,
                    schedule_type=day.schedule_type,
                    schedule_for_teachers=sfg,
                )
            )

        logger.info(
            "Parsed schedule days",
            extra={
                "total": total,
                "parsed_ok": parsed_ok,
                "empty": empty,
                "invalid_json": invalid_json,
                "invalid_type": invalid_type,
            },
        )

        return out