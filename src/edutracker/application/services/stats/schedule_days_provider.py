from datetime import date

from edutracker.application.interfaces.schedule_repository import IScheduleRepository
from edutracker.application.dto.schedule_day import ScheduleDayRow
from edutracker.infrastructure.parsers.schedule_json_parser import ScheduleJsonParser

class ScheduleDayProvider:
    def __init__(self, repo: IScheduleRepository, parser: ScheduleJsonParser):
        self._repo = repo
        self._parser = parser

    def get_days(self, date_from: date, date_to: date) -> list[ScheduleDayRow]:
        raw = self._repo.get_days_in_range(date_from, date_to)
        return self._parser.parse_days(raw)