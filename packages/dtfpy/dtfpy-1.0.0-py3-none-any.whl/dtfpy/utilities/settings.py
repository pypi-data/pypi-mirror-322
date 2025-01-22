from pydantic_settings import BaseSettings as PydanticBaseSettings


class Settings(PydanticBaseSettings):
    development_mode: bool | None = False

    api_key: str | None = None

    db_host: str | None = None
    db_port: int | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_name: str | None = None
    db_pool_size: int | None = None
    db_max_overflow: int | None = None
    db_sslmode: bool = False

    redis_host: str | None = None
    redis_port: int | None = None
    redis_db: str | None = None
    redis_password: str | None = None
    redis_ssl: bool | None = False

    bucket_name: str | None = None
    bucket_s3_mode: bool = False
    bucket_endpoint_url: str | None = None
    bucket_access_key: str | None = None
    bucket_secret_key: str | None = None
    bucket_region_name: str | None = None

    hide_response_error: bool = True

