from .average_lessons_mapper import to_schema as average_lessons
from .compare_teachers import to_schema as compare_teacher
from .peak_load_mapper import to_schema as peak_load
from .stats_teachers_mapper import to_schema as stats_teacher
from .top_teacher_mapper import to_schame as top_teacher

__all__ = (
    "average_lessons",
    "compare_teacher",
    "peak_load",
    "stats_teacher",
    "top_teacher"
)