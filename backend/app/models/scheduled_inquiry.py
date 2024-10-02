import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.mixins import IdMixin

if TYPE_CHECKING:
    from app.models.inquiry import Inquiry


# Shared properties
class ScheduledInquiryBase(SQLModel, IdMixin):
    inquiry_id: int = Field(foreign_key="inquiry.id")
    rank: int = Field(ge=1)  # rank starts at 1


# Properties to receive on ScheduledInquiry creation
class ScheduledInquiryCreate(ScheduledInquiryBase):
    pass


# Database model
class ScheduledInquiry(ScheduledInquiryBase, IdMixin, table=True):
    # Relationships
    inquiry: "Inquiry" = Relationship(back_populates="scheduled_inquiries")


# Properties to return via API for a single ScheduledInquiry
class ScheduledInquiryPublic(ScheduledInquiryBase):
    id: int


# Properties to return via API for multiple ScheduledInquiries
class ScheduledInquiriesPublic(SQLModel):
    data: list[ScheduledInquiryPublic]
    count: int
