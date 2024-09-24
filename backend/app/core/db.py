from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.models import User, UserCreate
from app.services import users

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=None,
            is_superuser=True,
        )
        print("session", session.bind.engine.url, id(session))

        user = users.create_user(session=session, user_create=user_in)
        print("created user in init_db", user)
        """
        created user in init_db full_name=None email='admin@example.com' 
        hashed_password='$2b$12$tq7nXZZ2Tfv9Hplrnj/0t.2Y5u6o5oVOLaOcnF9N/ClSZ5mX7Bu2i' 
        is_active=True is_superuser=True id=UUID('b5a9aaf9-d206-4420-adde-985a3751195c')
"""
