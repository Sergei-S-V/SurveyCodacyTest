from app.api.routes.schedule import convert_db_schedule_to_json
from app.models import Schedule, SchedulePublic


def test_convert_db_schedule_to_json_should_convert_db_to_serializable_object() -> None:
    # pylint disable=redefined-builtin
    id = "f202037b-71c0-42a5-913f-60270eb476a5"  # pylint: disable=W0622
    startDate = "2024-10-02"
    endDate = "2024-11-01"
    timesOfDay = ["08:00"]
    skipHolidays = False
    skipWeekends = True
    daysBetween = 1
    db_sched = Schedule(
        id=id,
        schedule='"{\\"startDate\\":\\"2024-10-02\\",\\"endDate\\":\\"2024-11-01\\",\\"daysBetween\\":1,\\"skipWeekends\\":true,\\"skipHolidays\\":false,\\"timesOfDay\\":[\\"08:00\\"]}"',
    )
    sched_public = SchedulePublic(
        skipHolidays=skipHolidays,
        skipWeekends=skipWeekends,
        startDate=startDate,
        endDate=endDate,
        timesOfDay=timesOfDay,
        daysBetween=daysBetween,
    )
    db_convert_output = convert_db_schedule_to_json(db_sched)
    assert db_convert_output == sched_public
