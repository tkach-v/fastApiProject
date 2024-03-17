from typing import Optional

from pydantic import BaseModel


class OrdersBase(BaseModel):
    title: str
    description: str
    customer_id: int
    performer_id: int


class OrdersCreate(OrdersBase):
    pass


class OrdersGet(OrdersBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True