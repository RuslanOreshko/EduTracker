class TeacherMatcher:
    def norm(self, s: str) -> str:
        return " ".join(s.lower().replace("’", "'").split())
    
    def split_parts(self, s: str) -> list[str]:
        return [self.norm(p) for p in s.split("/") if p.strip()]
    
    def match(self, raw_teacher_field: str, teacher_norm: str, split_by_slash: bool) -> bool:
        if not raw_teacher_field:
            return False
        
        raw_norm = self.norm(raw_teacher_field)

        if not split_by_slash:
            return teacher_norm == raw_norm or teacher_norm in raw_norm
        
        parts = self.split_parts(raw_teacher_field)
        return any(teacher_norm == p or teacher_norm in p for p in parts)