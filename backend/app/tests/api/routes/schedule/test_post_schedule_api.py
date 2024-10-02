import re

from fastapi.testclient import TestClient

from app.core.config import settings

first_valid_schedule = {
    "schedule": {
        "startDate": "2024-10-02",
        "endDate": "2024-11-01",
        "daysBetween": 1,
        "skipWeekends": "false",
        "skipHolidays": "false",
        "timesOfDay": ["08:00"],
    }
}

second_valid_schedule = {
    "schedule": {
        "startDate": "2024-12-12",
        "endDate": "2024-12-22",
        "daysBetween": 1,
        "skipWeekends": "true",
        "skipHolidays": "true",
        "timesOfDay": ["18:00"],
    }
}

schedule_with_missing_attribute = {
    "schedule": {
        "startDate": "2024-12-12",
        "endDate": "2024-12-22",
        "daysBetween": 1,
        "skipWeekends": "true",
        "skipHolidays": "false",
        "timesOfDay": ["six o'clock"],
    }
}

schedule_with_bad_time = {
    "schedule": {
        "startDate": "2024-12-12",
        "endDate": "2024-12-22",
        "daysBetween": 1,
        "skipWeekends": "true",
        "skipHolidays": "false",
        "timesOfDay": ["six o'clock"],
    }
}

schedule_with_bad_date = {
    "schedule": {
        "startDate": "December 10 2024",
        "endDate": "2024-12-22",
        "daysBetween": 1,
        "skipWeekends": "true",
        "skipHolidays": "false",
        "timesOfDay": ["18:00"],
    }
}

not_a_schedule_string = "why do birds suddenly appear every time you are near?"


def test_create_schedule_when_there_is_no_schedule_should_make_new_schedule(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=first_valid_schedule,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["daysBetween"] == first_valid_schedule["schedule"]["daysBetween"]
    assert content["endDate"] == first_valid_schedule["schedule"]["endDate"]
    assert content["startDate"] == first_valid_schedule["schedule"]["startDate"]
    assert content["timesOfDay"] == first_valid_schedule["schedule"]["timesOfDay"]
    assert not content["skipWeekends"]
    assert not content["skipHolidays"]


def test_create_schedule_when_there_is_already_a_schedule_should_return_the_new_schedule(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=first_valid_schedule,
    )
    response = client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=second_valid_schedule,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["daysBetween"] == second_valid_schedule["schedule"]["daysBetween"]
    assert content["endDate"] == second_valid_schedule["schedule"]["endDate"]
    assert content["startDate"] == second_valid_schedule["schedule"]["startDate"]
    assert content["timesOfDay"] == second_valid_schedule["schedule"]["timesOfDay"]
    assert content["skipWeekends"]
    assert content["skipHolidays"]


def test2_create_schedule_when_there_is_already_a_schedule_should_return_the_new_schedule(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=schedule_with_missing_attribute,
    )
    assert response.status_code == 422
    assert re.search("Schedule input is not valid", response.content.decode("utf-8"))


def test_create_schedule_when_time_is_malformed_should_return_error(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=schedule_with_bad_time,
    )
    assert response.status_code == 422
    assert response.status_code == 422
    assert re.search("Schedule input is not valid", response.content.decode("utf-8"))


def test4_create_schedule_when_there_is_already_a_schedule_should_return_the_new_schedule(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=schedule_with_bad_date,
    )
    assert response.status_code == 422
    assert re.search("Schedule input is not valid", response.content.decode("utf-8"))


def test5_create_schedule_when_there_is_already_a_schedule_should_return_the_new_schedule(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=not_a_schedule_string,
    )
    assert response.status_code == 422
    assert re.search(
        "Input should be a valid dictionary or object to extract fields from",
        response.content.decode("utf-8"),
    )
