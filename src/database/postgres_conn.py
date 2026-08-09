from sqlalchemy import Engine, create_engine
from ..config import settings

def create_database_engine() -> Engine:
    return create_engine(
        url = settings.DATABASE_URL,
        echo = False,
        pool_pre_ping = True,
    )

engine = create_database_engine()