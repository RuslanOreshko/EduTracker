from dataclasses import dataclass
from collections import Counter

from datetime import date


# Підрахунок 
@dataclass
class StatsAggregator:
    by_date: Counter
    by_group: Counter
    by_subject: Counter
    total: float = 0.0

    def add(self, schedule_date: date, lesson: dict, share: float) -> None:
        self.total += share
        self.by_date[schedule_date] += share

        group_name = (lesson.get("group_name") or "-")
        self.by_group[group_name] += share

        subject = (lesson.get("lesson_name") or "-")
        self.by_subject[subject] += share