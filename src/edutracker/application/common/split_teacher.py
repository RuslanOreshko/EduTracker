from typing import Any

from edutracker.application.services.stats.teacher_matcher import TeacherMatcher

class SplitTeacher:
    def __init__(self, teacher_matcher: TeacherMatcher):
        self._matcher = teacher_matcher
    
    def split_teacher(self, teacher_field: Any) -> list[tuple[str, float]]:
            if not teacher_field or not isinstance(teacher_field, str):
                return []
            
            parts_raw = [p.strip() for p in teacher_field.split("/") if p.strip()]
            if not parts_raw:
                return []
            
            parts_norm = [self._matcher.norm(p) for p in parts_raw]
            n = len(parts_norm)
            share = 1.0 / n

            out: list[tuple[str, float]] = []
            for p in parts_norm:
                out.append((p, share))
            
            return out