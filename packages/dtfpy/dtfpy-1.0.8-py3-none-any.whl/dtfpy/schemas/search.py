from enum import Enum
from pydantic import BaseModel, field_validator
from .helpers import BaseModelEnumValue


class OrderingType(str, Enum):
    desc = 'desc'
    asc = 'asc'


class Sorting(BaseModel):
    sort_by: str
    order_by: OrderingType = OrderingType.asc


class SearchPayload(BaseModelEnumValue):
    page: int | None = 1
    items_per_page: int | None = 20
    sorting: list[Sorting] | None = None

    search: str | None = ''

    # Page number must be greater than or equal to one
    @field_validator('page')
    def validate_page(cls, page):
        if page is not None and page < 1:
            raise ValueError('page number must be greater than one')
        return page

    # Make limitation for items per page
    @field_validator('items_per_page')
    def validate_items_per_page(cls, items_per_page):
        if items_per_page is not None and items_per_page > 30:
            raise ValueError('Item per page should be lower than or equal to 30.')
        return items_per_page
