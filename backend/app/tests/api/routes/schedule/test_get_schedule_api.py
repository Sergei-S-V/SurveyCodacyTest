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


def test_get_schedule_when_there_is_no_schedule_should_return_none(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content is None


def test_get_schedule_when_there_is_a_schedule_should_retrieve_schedule(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=first_valid_schedule,
    )
    response = client.get(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["daysBetween"] == first_valid_schedule["schedule"]["daysBetween"]
    assert content["endDate"] == first_valid_schedule["schedule"]["endDate"]
    assert content["startDate"] == first_valid_schedule["schedule"]["startDate"]
    assert content["timesOfDay"] == first_valid_schedule["schedule"]["timesOfDay"]
    assert not content["skipWeekends"]
    assert not content["skipHolidays"]


def test_get_schedule_when_a_schedule_has_been_added_twice_should_return_the_latest_schedule(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=first_valid_schedule,
    )
    client.post(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
        json=second_valid_schedule,
    )
    response = client.get(
        f"{settings.API_V1_STR}/schedule/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["daysBetween"] == second_valid_schedule["schedule"]["daysBetween"]
    assert content["endDate"] == second_valid_schedule["schedule"]["endDate"]
    assert content["startDate"] == second_valid_schedule["schedule"]["startDate"]
    assert content["timesOfDay"] == second_valid_schedule["schedule"]["timesOfDay"]
    assert content["skipWeekends"]
    assert content["skipHolidays"]
