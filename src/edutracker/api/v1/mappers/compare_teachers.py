from edutracker.application.dto.compare_teacher_result import TeacherCompareResult
from edutracker.api.v1.schemas.teacher_compare import (
    TeacherCompareOut,
    TeacherCompareSide,
    NameCount,
    ComparisonBlock,
)

def to_schema(result: TeacherCompareResult) -> TeacherCompareOut:
    return TeacherCompareOut(
        date_from=result.date_from,
        date_to=result.date_to,
        teacher_a=TeacherCompareSide(
            name=result.teacher_a.name,
            total_lessons=result.teacher_a.total_lessons,
            by_subject_top=[
                NameCount(name=i.name, count=i.count)
                for i in result.teacher_a.by_subject_top
            ],
            by_group_top=[
                NameCount(name=i.name, count=i.count)
                for i in result.teacher_a.by_group_top
            ],
        ),
        teacher_b=TeacherCompareSide(
            name=result.teacher_b.name,
            total_lessons=result.teacher_b.total_lessons,
            by_subject_top=[
                NameCount(name=i.name, count=i.count)
                for i in result.teacher_b.by_subject_top
            ],
            by_group_top=[
                NameCount(name=i.name, count=i.count)
                for i in result.teacher_b.by_group_top
            ],
        ),
        comparison=ComparisonBlock(
            winner=result.comparison.winner,
            difference_lessons=result.comparison.difference_lessons,
            difference_percent=result.comparison.difference_percent,
        ),
        summary=result.summary,
    )