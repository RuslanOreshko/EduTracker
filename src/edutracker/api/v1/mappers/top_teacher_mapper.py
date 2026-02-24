from edutracker.application.dto.top_teachers_result import TopTeachersResult
from edutracker.api.v1.schemas.top_teachers import TopTeachersOut, TopTacherItem

def to_schame(result: TopTeachersResult) -> TopTeachersOut:
    return TopTeachersOut(
        date_from=result.date_from,
        date_to=result.date_to,
        top=[
            TopTacherItem(teacher=item.teacher, total_lessons=item.total_lessons)
            for item in result.top
        ],
    )