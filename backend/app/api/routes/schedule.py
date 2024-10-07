import datetime

from fastapi import APIRouter, HTTPException

import app.services.schedule as schedule_service
from app.api.deps import SessionDep
from app.models import ScheduleCreate, ScheduleData, SchedulePublic

router = APIRouter()


def verify_schedule(schedule: ScheduleData) -> None:
    try:
        datetime.datetime.strptime(
            f"{schedule.startDate} {schedule.timesOfDay[0]}", "%Y-%m-%d %H:%M"
        )
        if hasattr(schedule, "endDate"):
            datetime.datetime.strptime(
                f"{schedule.endDate} {schedule.timesOfDay[0]}", "%Y-%m-%d %H:%M"
            )

    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Schedule input is not valid.",
        )


def convert_schedule_string_to_schedule_data(
    schedule_string: str,
) -> ScheduleData:
    try:
        return ScheduleData.model_validate_json(schedule_string)
    except Exception:
        raise ValueError("Could not retrieve schedule")


@router.post("/", response_model=SchedulePublic)
def create_schedule(
    *, session: SessionDep, schedule_in: ScheduleCreate
) -> SchedulePublic | None:
    verify_schedule(schedule_in.schedule)
    db_schedule = schedule_service.create_schedule(
        session=session, schedule_in=schedule_in
    )
    schedule_data = convert_schedule_string_to_schedule_data(
        schedule_string=db_schedule.schedule
    )
    return SchedulePublic(id=db_schedule.id, schedule=schedule_data)


@router.get("/", response_model=SchedulePublic | None)
def get_schedule(*, session: SessionDep) -> SchedulePublic | None:
    db_schedule = schedule_service.get_schedule(session)
    if db_schedule is None:
        return None
    schedule_data = convert_schedule_string_to_schedule_data(
        schedule_string=db_schedule.schedule
    )
    return SchedulePublic(id=db_schedule.id, schedule=schedule_data)
