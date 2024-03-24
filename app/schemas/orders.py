from pydantic import BaseModel, Field

from app.schemas.common import PyObjectId


class OrderBase(BaseModel):
    title: str
    description: str
    customer_id: PyObjectId
    performer_id: PyObjectId


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: PyObjectId = Field(alias="_id")
    completed: bool

    class Config:
        orm_mode = True
