import unittest.mock
from unittest.mock import ANY, Mock

import pytest
from fastapi.testclient import TestClient

import app.services.inquiries
from app.core.config import settings
from app.models import Inquiry, InquiryCreate


@pytest.fixture(autouse=True)
def create_inquiry_mock(monkeypatch):
    _mock = unittest.mock.MagicMock()
    monkeypatch.setattr(
        app.services.inquiries, app.services.inquiries.create_inquiry.__name__, _mock
    )
    return _mock


@pytest.fixture(autouse=True)
def get_inquiry_by_text_mock(monkeypatch):
    _mock = unittest.mock.MagicMock()
    monkeypatch.setattr(
        app.services.inquiries,
        app.services.inquiries.get_inquiry_by_text.__name__,
        _mock,
    )
    return _mock


def test_create_inquiry_api_calls_create_inquiry_service(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    create_inquiry_mock: Mock,
    get_inquiry_by_text_mock: Mock,
) -> None:
    text_content = "Why do birds suddenly appear every time you are near?"
    get_inquiry_by_text_mock.return_value = None
    create_inquiry_mock.return_value = Inquiry(text=text_content)
    data = {"text": text_content}
    response = client.post(
        f"{settings.API_V1_STR}/inquiries/",
        headers=superuser_token_headers,
        json=data,
    )

    get_inquiry_by_text_mock.assert_called_once()
    create_inquiry_mock.assert_called_once()
    create_inquiry_mock.assert_called_with(
        session=ANY, inquiry_in=InquiryCreate(text=text_content)
    )


def test_create_inquiry_does_not_create_duplicate(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    create_inquiry_mock: Mock,
    get_inquiry_by_text_mock: Mock,
) -> None:
    text_content = "Why do birds suddenly appear every time you are near?"
    get_inquiry_by_text_mock.return_value = Inquiry(text=text_content)
    create_inquiry_mock.return_value = Inquiry(text=text_content)
    data = {"text": text_content}
    response = client.post(
        f"{settings.API_V1_STR}/inquiries/",
        headers=superuser_token_headers,
        json=data,
    )

    get_inquiry_by_text_mock.assert_called_once()
    create_inquiry_mock.assert_not_called()
