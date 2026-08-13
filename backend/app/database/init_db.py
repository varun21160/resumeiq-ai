from app.database.base import Base
from app.database.session import engine

# Import all models so SQLAlchemy knows about them.
from app.models.user import User
from app.models.resume import Resume
from app.models.ats_analysis import ATSAnalysis


def init_db() -> None:
    """
    Create all database tables that do not already exist.
    """

    Base.metadata.create_all(
        bind=engine
    )