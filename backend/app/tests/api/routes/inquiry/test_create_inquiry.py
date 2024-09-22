from unittest.mock import ANY, MagicMock, Mock

import pytest
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

import app.services.inquiries
from app.core.config import settings
from app.models import Inquiry, InquiryCreate

inquiry_text = "Why do birds suddenly appear every time you are near?"


@pytest.fixture(autouse=True)
def create_inquiry_mock(monkeypatch: MonkeyPatch) -> MagicMock:
    _mock = MagicMock()
    monkeypatch.setattr(
        app.services.inquiries, app.services.inquiries.create_inquiry.__name__, _mock
    )
    return _mock


@pytest.fixture(autouse=True)
def get_inquiry_by_text_mock(monkeypatch: MonkeyPatch) -> MagicMock:
    _mock = MagicMock()
    monkeypatch.setattr(
        app.services.inquiries,
        app.services.inquiries.get_inquiry_by_text.__name__,
        _mock,
    )
    return _mock


def test_create_inquiry_route_should_invoke_create_inquiry_service_with_correct_arguments_when_inquiry_does_not_exist(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    create_inquiry_mock: Mock,
    get_inquiry_by_text_mock: Mock,
) -> None:
    get_inquiry_by_text_mock.return_value = None
    create_inquiry_mock.return_value = Inquiry(text=inquiry_text)
    data = {"text": inquiry_text}
    client.post(
        f"{settings.API_V1_STR}/inquiries/",
        headers=superuser_token_headers,
        json=data,
    )

    get_inquiry_by_text_mock.assert_called_once()
    create_inquiry_mock.assert_called_once()
    create_inquiry_mock.assert_called_with(
        session=ANY, inquiry_in=InquiryCreate(text=inquiry_text)
    )


def test_create_inquiry_route_should_not_ask_inquiry_service_to_create_inquiry_when_inquiry_already_exists(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    create_inquiry_mock: Mock,
    get_inquiry_by_text_mock: Mock,
) -> None:
    get_inquiry_by_text_mock.return_value = Inquiry(text=inquiry_text)
    create_inquiry_mock.return_value = None
    data = {"text": inquiry_text}
    client.post(
        f"{settings.API_V1_STR}/inquiries/",
        headers=superuser_token_headers,
        json=data,
    )

    get_inquiry_by_text_mock.assert_called_once()
    create_inquiry_mock.assert_not_called()
