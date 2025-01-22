from contextlib import contextmanager, asynccontextmanager
from sqlalchemy import create_engine, event, Pool, text, NullPool
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class DatabaseUtility:

    def __init__(self, settings):
        self.active_connections = 0

        # Build database connection URLs
        self.database_path = self._build_database_url(settings, async_mode=False)
        self.async_database_path = self._build_database_url(settings, async_mode=True)

        # Database settings
        db_settings = self._initialize_db_settings(settings)

        # Create synchronous and asynchronous engines and sessions
        self.engine = create_engine(self.database_path, **db_settings)
        self.scoped_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=True
        ))

        self.async_engine = create_async_engine(self.async_database_path, **db_settings)
        self.async_session_maker = async_sessionmaker(
            bind=self.async_engine, expire_on_commit=True, class_=AsyncSession,
            autocommit=False, autoflush=False
        )

        # Declarative base for ORM models
        self.base = declarative_base(name="Base")

    def _build_database_url(self, settings, async_mode=False):
        scheme = "postgresql+asyncpg" if async_mode else "postgresql"
        url = f"{scheme}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

        if getattr(settings, "db_sslmode", False):
            url += "?ssl=require" if async_mode else "?sslmode=require"
        return url

    def _initialize_db_settings(self, settings):
        db_settings = {"pool_pre_ping": True, "echo": False}

        if db_pool_size := getattr(settings, "db_pool_size", None):
            db_settings.update({
                "pool_size": db_pool_size,
                "pool_recycle": 300,
                "pool_use_lifo": True,
                "max_overflow": getattr(settings, "db_max_overflow", 0),
            })
        else:
            db_settings["poolclass"] = NullPool

        return db_settings

    def session_local(self):
        return self.scoped_session()

    def get_db(self):
        db = self.session_local()
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @contextmanager
    def get_db_cm(self):
        db = self.session_local()
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def get_clean_db(self):
        db = self.session_local()
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.expunge_all()
            db.close()

    @contextmanager
    def get_clean_db_cm(self):
        db = self.session_local()
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.expunge_all()
            db.close()

    def create_tables(self):
        self.base.metadata.create_all(self.engine)

    def close_all_connections(self):
        self.engine.dispose()
        print("All connections closed gracefully.")

    def setup_connection_monitoring(self):
        @event.listens_for(Pool, "connect")
        def connect_listener(dbapi_connection, connection_record):
            self.active_connections += 1
            print(f"New database connection created. Total active connections: {self.active_connections}")

        @event.listens_for(Pool, "close")
        def close_listener(dbapi_connection, connection_record):
            self.active_connections -= 1
            print(f"A database connection closed. Total active connections: {self.active_connections}")

    def check_database_health(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False

    def async_session_local(self):
        return self.async_session_maker()

    async def async_get_db(self):
        db = self.async_session_local()
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()

    async def async_get_clean_db(self):
        db = self.async_session_local()
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.expunge_all()
            await db.close()

    @asynccontextmanager
    async def async_get_db_cm(self):
        db = self.async_session_local()
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()

    @asynccontextmanager
    async def async_get_clean_db_cm(self):
        db = self.async_session_local()
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        finally:
            db.expunge_all()
            await db.close()
