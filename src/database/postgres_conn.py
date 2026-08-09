from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from ..config import settings

def create_database_engine() -> Engine:
    return create_engine(
        url = settings.DATABASE_URL,
        echo = False,
        pool_pre_ping = True,
    )

engine = create_database_engine()