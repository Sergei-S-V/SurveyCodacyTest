import datetime
import json

from fastapi import APIRouter, HTTPException

import app.services.schedule as schedule_service
from app.api.deps import SessionDep
from app.models import Schedule, ScheduleCreate, ScheduleData, SchedulePublic

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


def convert_db_schedule_to_json(db_schedule: Schedule | None) -> SchedulePublic | None:
    if db_schedule is None:
        return None
    try:
        schedule_as_string = db_schedule.schedule
        schedule_as_json = json.loads(schedule_as_string)
        return SchedulePublic.parse_raw(schedule_as_json)
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
    return convert_db_schedule_to_json(db_schedule=db_schedule)


@router.get("/", response_model=SchedulePublic | None)
def get_schedule(*, session: SessionDep) -> SchedulePublic | None:
    db_schedule = schedule_service.get_schedule(session)
    if db_schedule is None:
        return None
    return convert_db_schedule_to_json(db_schedule=db_schedule)
