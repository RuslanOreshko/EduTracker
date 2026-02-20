from typing import Any, Iterable


class LessonExtractor:
    def extract(self, day: Any, weekday: str) -> Iterable[dict]:
        sfg = day.schedule_for_teachers or {}

        if not isinstance(sfg, dict):
            return []
        
        lesson_out: list[dict] = []

        for _, teacher_payload in sfg.items():
            if not isinstance(teacher_payload, dict):
                continue
        
            day_block = teacher_payload.get(weekday)
            if not isinstance(day_block, dict):
                continue

            lessons = day_block.get("lessons") or []
            if not isinstance(lessons, list):
                continue

            for lesson in lessons:
                if isinstance(lesson, dict):
                    lesson_out.append(lesson)

        return lesson_out   