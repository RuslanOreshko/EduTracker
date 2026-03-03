from pydantic import BaseModel


class TeacherSuggestItemDto(BaseModel):
    display_name: str

class TeacherSuggestResponseDto(BaseModel):
    items: list[TeacherSuggestItemDto]