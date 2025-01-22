from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class NumberRange(BaseModel):
    min: int | None = None
    max: int | None = None


class TimeRange(BaseModel):
    min: datetime | None = None
    max: datetime | None = None


class DateRange(BaseModel):
    min: date | None = None
    max: date | None = None


class BaseModelEnumValue(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
