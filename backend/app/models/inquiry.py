import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

# Shared properties
class InquiryBase(SQLModel):
    text: str = Field(min_length=10, max_length=255)


# Properties to receive on inquiry creation
class InquiryCreate(InquiryBase):
    text: str = Field(min_length=10, max_length=255)


# Database model, database table inferred from class name
class Inquiry(InquiryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    text: str = Field(min_length=10, max_length=255, unique=True)


# Properties to return via API, id is always required
class InquiryPublic(InquiryBase):
    id: uuid.UUID
