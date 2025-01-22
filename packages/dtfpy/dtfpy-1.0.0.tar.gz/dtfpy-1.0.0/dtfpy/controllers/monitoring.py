from sqlalchemy import text
from ..utilities.redis import RedisUtility
from ..utilities.database import DatabaseUtility


def is_redis_connected(redis: RedisUtility) -> tuple[bool, Exception | None]:
    try:
        return redis.get_redis_client().ping(), None
    except Exception as e:
        return False, e


def is_database_connected(db: DatabaseUtility) -> tuple[bool, Exception | None]:
    try:
        if db.separate_read_write:
            with db.read_engine.connect() as read_connection, db.write_engine.connect() as write_connection:
                read_connection.execute(text("SELECT 1"))
                write_connection.execute(text("SELECT 1"))
        else:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

        return True, None

    except Exception as e:
        return False, e
