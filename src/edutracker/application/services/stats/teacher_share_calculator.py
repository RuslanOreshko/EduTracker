from edutracker.application.services.stats.teacher_matcher import TeacherMatcher

class TeacherShareCalculator:
    def __init__(self, matcher: TeacherMatcher):
        self._matcher = matcher

    def calc(self, teacher_field: str, teacher_norm: str, split_by_slash) -> float:
        if not teacher_field:
            return 0.0
        
        if not split_by_slash:
            return 1.0 if self._matcher.match(teacher_field, teacher_norm, split_by_slash=False) else 0.0
        
        parts = self._matcher.split_parts(teacher_field)
        if not parts:
            return 0.0
        
        matched = any(teacher_norm == p or teacher_norm in p for p in parts)
        if not matched:
            return 0.0
        
        return 1.0 / len(parts)