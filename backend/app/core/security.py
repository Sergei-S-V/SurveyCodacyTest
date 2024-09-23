from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(
        plain_password, hashed_password
    )  # '$2b$12$VlLv03E6yEyZOgWhLBckL.7vAEODWIy/nxdB08m7FLt7DqK96UEaa'


def get_password_hash(password: str) -> str:  # 'ywxzvmhzcsquyxdfimmlqotedvvtkdcs'
    pw_hash = pwd_context.hash(password)
    print(pw_hash)  # '$2b$12$elQrED551O0IAaituKpLReIYT26hkthHIsreAb3e9YG3IxWPGQ7s2'
    return pw_hash  # '$2b$12$0r.599atzWi3rrN0Jdokde0bBAfoBvKS2IGtcgWG0ijOoSt5ohoVS'
