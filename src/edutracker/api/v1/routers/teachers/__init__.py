from .average_lessons_router import router as avg_router
from .top_teachers import router as top_teacher_router
from .peak_load_teacher_router import router as peak_load_router
from .teachers_stats import router as stats_router
from .teacher_compare import router as compare_router


__all__ = [
    "avg_router",
    "top_teacher_router",
    "peak_load_router",
    "stats_router",
    "compare_router",
]