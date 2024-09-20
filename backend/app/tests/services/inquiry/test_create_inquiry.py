from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from app.models.inquiry import Inquiry, InquiryCreate
from app.services.inquiries import create_inquiry


@pytest.fixture
def mock_session():
    return Mock()


def test_should_create_with_valid_data(mock_session):
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


def test_should_raise_error_with_missing_text(mock_session):
    with pytest.raises(ValidationError) as ve:
        inquiry_data = InquiryCreate()
        create_inquiry(session=mock_session, inquiry_in=inquiry_data)
        assert "Validation error for InquiryCreate" in ve.value

    with pytest.raises(ValidationError) as ve:
        inquiry_data = InquiryCreate(taxed="Taxed inquiry")
        create_inquiry(session=mock_session, inquiry_in=inquiry_data)
        assert "Validation error for InquiryCreate" in ve.value


def test_should_raise_error_with_wrong_text_length(mock_session):
    short_string = "A" * 9
    long_string = "A" * 257
    with pytest.raises(ValidationError) as ve:
        inquiry_data = InquiryCreate(text=short_string)
        create_inquiry(session=mock_session, inquiry_in=inquiry_data)
        assert "String should have at least 10 characters" in ve.value

    with pytest.raises(ValidationError) as ve:
        inquiry_data = InquiryCreate(text=long_string)
        create_inquiry(session=mock_session, inquiry_in=inquiry_data)
        assert "String should have at most 255 characters" in ve.value
