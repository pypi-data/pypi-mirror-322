from typing import Any, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from .. import ViewType


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(populate_by_name=True)

    def model_dump(self, **kw) -> dict[str, Any]:
        kw = {"exclude_none": True, "exclude_unset": True, **kw}
        return super().model_dump(**kw)


class EnqueueItem(BaseModel):
    payload: str
    delay: float = 0.0
    for_: Optional[str] = Field(default=None, alias="for")
    priority: int = 0
    unique_id: Optional[str] = None
    timeout: float = 600.0
    max_claims: int = 2
    topic: Optional[str] = None


class DequeueItem(BaseModel):
    topic: Optional[str] = None
    for_: Optional[str] = Field(default=None, alias="for")
    by: Optional[str] = None
    after: Optional[int] = None
    before: Optional[int] = None
    no_ack: bool = False


class AckItem(BaseModel):
    message_id: int


class PushItem(BaseModel):
    payload: str


class PopItem(BaseModel):
    by: Optional[str] = None


class ViewItem(BaseModel):
    after: float | None = None
    before: float | None = None
    by: str | None = None
    dead: bool = False
    for_: str | None = Field(default=None, alias="for")
    topic: str | None = None
    view_type: ViewType | None = "front"


class DeleteItem(BaseModel):
    before: float | None = None


class SearchItem(BaseModel):
    after: float | None = None
    before: float | None = None
    by: str | None = None
    claimed: bool | None = False
    completed: bool | None = False
    dead: bool | None = False
    for_: str | None = Field(default=None, alias="for")
    limit: int | None = None
    topic: str | None = None
