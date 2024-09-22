from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from app.models.inquiry import Inquiry, InquiryCreate
from app.services.inquiries import create_inquiry


@pytest.fixture
def mock_session() -> Mock:
    return Mock()


def test_create_inquiry_service_should_correctly_invoke_database_commands(
    mock_session: Mock,
) -> None:
    inquiry_data = InquiryCreate(text="Test inquiry")
    expected_inquiry = Inquiry(id=1, text="Test inquiry")
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    result = create_inquiry(session=mock_session, inquiry_in=inquiry_data)

    assert result.text == expected_inquiry.text
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_create_inquiry_service_should_raise_error_when_no_text_parameter_is_given(
    mock_session: Mock,
) -> None:
    with pytest.raises(ValidationError, match=r"Field required"):
        inquiry_data = InquiryCreate()
        create_inquiry(session=mock_session, inquiry_in=inquiry_data)

    with pytest.raises(ValidationError, match=r"Field required"):
        inquiry_data = InquiryCreate(taxed="Taxed inquiry")
        create_inquiry(session=mock_session, inquiry_in=inquiry_data)


def test_create_inquiry_service_should_raise_error_when_text_parameter_is_too_short(
    mock_session: Mock,
) -> None:
    short_string = "A" * 9

    with pytest.raises(
        ValidationError, match="String should have at least 10 characters"
    ):
        inquiry_data = InquiryCreate(text=short_string)
        create_inquiry(session=mock_session, inquiry_in=inquiry_data)


def test_create_inquiry_service_should_raise_error_when_text_parameter_is_too_long(
    mock_session: Mock,
) -> None:
    long_string = "A" * 257

    with pytest.raises(
        ValidationError, match="String should have at most 25. characters"
    ):
        inquiry_data = InquiryCreate(text=long_string)
        create_inquiry(session=mock_session, inquiry_in=inquiry_data)
