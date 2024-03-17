from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.db.connection import get_db
from app.schemas.orders import OrdersCreate, OrdersGet

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", summary="list of orders", response_model=list[OrdersGet])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Orders).all()
    return orders


@router.get("/{id}", response_model=OrdersGet)
def get_order(id: int, db: Session = Depends(get_db)):
    order = db.query(models.Orders).filter(models.Orders.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{id}", response_model=OrdersGet, summary="Mark order as completed")
def mark_order_as_completed(id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Orders).filter(models.Orders.id == id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.completed = True

    db.commit()
    db.refresh(db_order)
    return db_order


@router.post("/", response_model=OrdersGet)
def create_order(order: OrdersCreate, db: Session = Depends(get_db)):
    new_order = models.Users(**order.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
