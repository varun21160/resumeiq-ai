from app.database.base import Base
from app.database.session import engine

# Import models here
from app.models import user


def init_db():
    Base.metadata.create_all(bind=engine)