from typing import List, Any

from pydantic import BaseModel, Field


def paginate_data(
        query,
        query_with_conditions,
        start: int,
        size: int
):
    result = query_with_conditions.all()
    return BasePage(
        result=result[:size],
        has_next=len(result) > size,
        offset=start,
        limit=size,
        count=query.count(),
        next=start + size if len(result) > size else -1
    )


class BasePage(BaseModel):
    result: List[Any] = Field(..., description="資料")
    has_next: bool = Field(..., description="是否有下一頁")
    offset: int = Field(..., description="本次從第幾筆開始")
    limit: int = Field(..., description="每頁筆數")
    count: int = Field(..., description="實際回傳筆數")
    next: int = Field(..., description="下一頁第幾筆")
