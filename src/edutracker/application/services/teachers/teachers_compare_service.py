from collections import Counter
from datetime import date
import logging

from edutracker.application.services.teachers.teacher_stats_service import TeacherStatsService

logger = logging.getLogger(__name__)


class TeacherCompareService:
    def __init__(self, stats_service: TeacherStatsService):
        self._stats = stats_service

    def compare(
        self,
        teacher_a: str,
        teacher_b: str,
        date_from: date,
        date_to: date,
        top_n: int = 5,
    ):
        # Логування про початок роботи сервісу
        logger.info(
            "Compare teachers requested",
            extra={
                "teacher_1": teacher_a,
                "teacher_2": teacher_b,
                "date_from": str(date_from),
                "date_to": str(date_to),
            },
        )

        # Статистики викладачів повернуто від класу TeacherStatsService
        # Викладач а
        a = self._stats.teacher_stats(
            teacher=teacher_a,
            date_from=date_from,
            date_to=date_to,
            split_teachers_by_slash=True,
        )

        # Викладач б
        b = self._stats.teacher_stats(
            teacher=teacher_b,
            date_from=date_from,
            date_to=date_to,
            split_teachers_by_slash=True,
        )

        a_total = float(a.total_lessons)
        b_total = float(b.total_lessons)

        if a_total > b_total:
            winner = "teacher_a"
        elif b_total > a_total:
            winner = "teacher_b"
        else:
            winner = "tie"

        diff = round(abs(a_total - b_total), 2)

        base = max(a_total, b_total, 1e-9)
        diff_percent = round((diff / base) * 100, 2)

        def top_items(counter_dict: dict, n: int):
            c = Counter(counter_dict)
            return [{"name": k, "count": round(float(v), 2)} for k, v in c.most_common(n)]
        
        summary = self._build_summary(teacher_a, teacher_b, winner, diff, diff_percent)

        # Лог про закінчення роботи
        logger.info(
            "Compare teachers computed",
            extra={
                "teacher_1": teacher_a,
                "teacher_2": teacher_b,
                "total_1": a_total,
                "total_2": b_total,
            },
        )

        return {
            "date_from": date_from,
            "date_to": date_to,
            "teacher_a": {
                "name": teacher_a,
                "total_lessons": round(a_total, 2),
                "by_subject_top": top_items(a.by_subject, top_n),
                "by_group_top": top_items(a.by_group, top_n)
            },
            "teacher_b": {
                "name": teacher_b,
                "total_lessons": round(b_total, 2),
                "by_subject_top": top_items(b.by_subject, top_n),
                "by_group_top": top_items(b.by_group, top_n)
            },
            "comparison": {
                "winner": winner,
                "difference_lesson": diff,
                "defference_percent": diff_percent,
            },
            "summary": summary,
        }

    
    # Висновок
    def _build_summary(self, ta: str, tb: str, winner: str, diff: float, diff_percent: float) -> str:
        if winner == "tie":
            return f"За вибраний період {ta} і {tb} провели одинакову кількість зайнять."
        if winner == "teacher_a":
            return f"{ta} провів(ла) на {diff} зайнять більше (+{diff_percent}%) за вибраний період"
        return f"{tb} провів(ла) на {diff} зайнять більше (+{diff_percent}%) за вибраний період"

