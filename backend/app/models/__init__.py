"""
Survey models
~~~~~~~~~~~~~

Basic usage:
    >>> from app.models import User, UserCreate

Important:
    Models that inherit from SQLModel and are configured with table=true, should be added as strings to __all__,
    otherwise migrations will not work properly.

    https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/?h=metadata#sqlmodel-metadata
"""

from .auth import Message, NewPassword, Token, TokenPayload, UpdatePassword
from .inquiry import (
    Inquiry,
    InquiryCreate,
    InquiryPublic,
    InquiryUpdate,
    InquriesPublic,
)
from .item import Item, ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from .theme import Theme, ThemeCreate, ThemePublic, ThemesPublic
from .user import (
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

# https://realpython.com/python-all-attribute/#names-from-a-package
__all__ = [
    # auth model
    "Message",
    "NewPassword",
    "Token",
    "TokenPayload",
    "UpdatePassword",
    # inquiry model
    "Inquiry",
    "InquiryCreate",
    "InquiryPublic",
    "InquiryPublic",
    "InquriesPublic",
    "InquiryUpdate",
    # theme model
    "Theme",
    "ThemeCreate",
    "ThemePublic",
    "ThemesPublic",
    # item model
    "Item",
    "ItemCreate",
    "ItemPublic",
    "ItemsPublic",
    "ItemUpdate",
    # user model
    "User",
    "UserCreate",
    "UserPublic",
    "UserRegister",
    "UsersPublic",
    "UserUpdate",
    "UserUpdateMe",
]
