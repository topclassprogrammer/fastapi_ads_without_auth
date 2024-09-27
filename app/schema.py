import datetime

from pydantic import BaseModel


class IdReturnBase(BaseModel):
    id: int


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    owner: int
    created_at: datetime.datetime


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: float
    owner: int


class CreateAdvertisementResponse(IdReturnBase):
    pass


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class UpdateAdvertisementResponse(IdReturnBase):
    pass


class DeleteAdvertisementResponse(BaseModel):
    status: str
