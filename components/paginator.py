from typing import List, Any, Callable, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')

def paginate_data(
        query,
        data,
        transform_data_function: Callable,
        start: int,
        size: int
):
    return BasePage(
        result=transform_data_function(data[:size]),
        has_next=len(data) > size,
        offset=start,
        limit=size,
        count=query.count(),
        next=start + size if len(data) > size else -1
    )


class BasePage(BaseModel):
    result: List[Any] = Field(..., description="資料")
    has_next: bool = Field(..., description="是否有下一頁")
    offset: int = Field(..., description="本次從第幾筆開始")
    limit: int = Field(..., description="每頁筆數")
    count: int = Field(..., description="實際回傳筆數")
    next: int = Field(..., description="下一頁第幾筆")


class BasePageOut(BaseModel, Generic[T]):
    result: List[Any] = Field(..., description="資料")
    has_next: bool = Field(..., description="是否有下一頁")
    offset: int = Field(..., description="本次從第幾筆開始")
    limit: int = Field(..., description="每頁筆數")
    count: int = Field(..., description="實際回傳筆數")
    next: int = Field(..., description="下一頁第幾筆")