from typing import Any


class ValueCleaner:
    @staticmethod
    def clean(v: str) -> str:
        if v is None:
            return ""
        
        s = str(v).strip()

        if s.lower() == "none":
            return ""
        
        return s