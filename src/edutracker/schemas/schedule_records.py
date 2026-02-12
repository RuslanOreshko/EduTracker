from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class ScheduleRecordOut(BaseModel):
    id: int
    schedule_date: date
    schedule_file_id: str
    schedule_file_name: str

    group_emails_list: str | None
    teachers_emails_list: str | None

    schedule_type: str | None
    bell_type: str | None

    schedule_for_groups: str | None
    schedule_for_teachers: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)