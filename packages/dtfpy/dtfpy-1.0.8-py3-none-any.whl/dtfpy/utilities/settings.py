from functools import lru_cache
from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict
from typing import Type, TypeVar, Optional

T = TypeVar('T', bound='BaseSettings')


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding='utf-8',
        extra='ignore'
    )


class Settings(BaseSettings):
    service_name: Optional[str] = None
    development_mode: bool = False

    api_key: Optional[str] = None

    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_name: Optional[str] = None
    db_pool_size: Optional[int] = None
    db_max_overflow: Optional[int] = None
    db_sslmode: bool = False

    redis_host: Optional[str] = None
    redis_port: Optional[int] = None
    redis_db: Optional[str] = None
    redis_password: Optional[str] = None
    redis_ssl: bool = False

    bucket_name: Optional[str] = None
    bucket_s3_mode: bool = False
    bucket_endpoint_url: Optional[str] = None
    bucket_access_key: Optional[str] = None
    bucket_secret_key: Optional[str] = None
    bucket_region_name: Optional[str] = None

    hide_response_error: bool = True

    logging_ms_url: Optional[str] = None
    logging_ms_key: Optional[str] = None

    log_level: str = 'error'
    log_print: bool = False
    log_store: bool = False


@lru_cache
def get_settings(attr: Optional[str] = None, cls: Type[T] = Settings) -> T:
    settings = cls()
    return getattr(settings, attr) if attr is not None else settings
