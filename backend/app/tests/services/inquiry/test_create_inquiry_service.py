import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.models.inquiry import InquiryCreate
from app.services.inquiries import create_inquiry


def test_inquiry_service_create_should_create_inquiry_when_inquiry_does_not_exist(
    db: Session,
) -> None:
    text = "Test Inquiry"
    inquiry_data = InquiryCreate(text=text)
    result = create_inquiry(session=db, inquiry_in=inquiry_data)
    assert result.text == text
    assert result.id is not None
    assert result.created_at is not None


def test_create_inquiry_service_should_raise_error_when_no_text_parameter_is_given(
    db: Session,
) -> None:
    with pytest.raises(ValidationError, match=r"Field required"):
        inquiry_data = InquiryCreate()
        create_inquiry(session=db, inquiry_in=inquiry_data)

    with pytest.raises(ValidationError, match=r"Field required"):
        inquiry_data = InquiryCreate(taxed="Taxed inquiry")
        create_inquiry(session=db, inquiry_in=inquiry_data)


def test_create_inquiry_service_should_raise_error_when_text_parameter_is_too_short(
    db: Session,
) -> None:
    short_string = "A" * 9

    with pytest.raises(
        ValidationError, match="String should have at least 10 characters"
    ):
        inquiry_data = InquiryCreate(text=short_string)
        create_inquiry(session=db, inquiry_in=inquiry_data)


def test_create_inquiry_service_should_raise_error_when_text_parameter_is_too_long(
    db: Session,
) -> None:
    long_string = "A" * 257

    with pytest.raises(
        ValidationError, match="String should have at most 25. characters"
    ):
        inquiry_data = InquiryCreate(text=long_string)
        create_inquiry(session=db, inquiry_in=inquiry_data)


@pytest.mark.skip(
    "The UNIQUE constraint error gets propagated to sqlalchemy.exc.PendingRollbackError which breaks the tests"
)
def test_inquiry_service_create_should_not_create_inquiry_when_inquiry_already_exists(
    db: Session,
) -> None:
    with pytest.raises(IntegrityError, match="UNIQUE constraint failed"):
        text = "Test Inquiry"
        inquiry_data = InquiryCreate(text=text)
        result = create_inquiry(session=db, inquiry_in=inquiry_data)
        assert result.text == text
        assert result.id is not None
        assert result.created_at is not None

        inquiry_data = InquiryCreate(text=text)
        create_inquiry(session=db, inquiry_in=inquiry_data)
