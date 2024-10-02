from sqlmodel import Session

from app.models import ScheduleCreate, ScheduleData
from app.services.schedule import create_schedule

first_valid_schedule = {
    "startDate": "2024-10-02",
    "endDate": "2024-11-01",
    "daysBetween": 1,
    "skipWeekends": "false",
    "skipHolidays": "false",
    "timesOfDay": ["08:00"],
}


second_valid_schedule = {
    "startDate": "2024-12-12",
    "endDate": "2024-12-22",
    "daysBetween": 1,
    "skipWeekends": "true",
    "skipHolidays": "true",
    "timesOfDay": ["18:00"],
}


def test_create_schedule_service_when_schedule_does_exist_should_create_schedule(
    db: Session,
) -> None:
    schedule_data = ScheduleData(**first_valid_schedule)  # type: ignore
    schedule_create = ScheduleCreate(schedule=schedule_data)
    result = create_schedule(session=db, schedule_in=schedule_create)
    assert result.id is not None
    assert (
        result.schedule
        == '"{\\"startDate\\":\\"2024-10-02\\",\\"endDate\\":\\"2024-11-01\\",\\"daysBetween\\":1,\\"skipWeekends\\":false,\\"skipHolidays\\":false,\\"timesOfDay\\":[\\"08:00\\"]}"'
    )


def test_create_schedule_service_when_schedule_already_exists_should_create_schedule(
    db: Session,
) -> None:
    first_schedule_data = ScheduleData(**first_valid_schedule)  # type: ignore
    first_schedule_create = ScheduleCreate(schedule=first_schedule_data)
    create_schedule(session=db, schedule_in=first_schedule_create)
    second_schedule_data = ScheduleData(**second_valid_schedule)  # type: ignore
    second_schedule_create = ScheduleCreate(schedule=second_schedule_data)
    result = create_schedule(session=db, schedule_in=second_schedule_create)
    assert result.id is not None
    assert (
        result.schedule
        == '"{\\"startDate\\":\\"2024-12-12\\",\\"endDate\\":\\"2024-12-22\\",\\"daysBetween\\":1,\\"skipWeekends\\":true,\\"skipHolidays\\":true,\\"timesOfDay\\":[\\"18:00\\"]}"'
    )
