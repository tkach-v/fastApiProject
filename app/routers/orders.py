from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Request

from app.schemas.orders import OrderCreate, Order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", summary="Get list of orders", response_model=list[Order])
async def get_orders(request: Request):
    orders = await request.app.mongodb["orders"].find().to_list(1000)
    return orders


@router.get("/{id}", summary="Get order by id", response_model=Order)
async def get_order(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    order = await request.app.mongodb["orders"].find_one({"_id": ObjectId(id)})
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{id}", response_model=Order, summary="Mark order as completed")
async def mark_order_as_completed(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    order = await request.app.mongodb["orders"].find_one({"_id": ObjectId(id)})
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    update_data = {
        "completed": True
    }
    await request.app.mongodb["orders"].update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data},
    )

    updated_order = await request.app.mongodb["orders"].find_one({"_id": ObjectId(id)})
    return updated_order


@router.post("/", response_model=Order, summary="Create a new order")
async def create_order(order: OrderCreate, request: Request):
    try:
        customer_id = ObjectId(order.customer_id)
        performer_id = ObjectId(order.performer_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    customer = await request.app.mongodb["users"].find_one({"_id": customer_id})
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    performer = await request.app.mongodb["users"].find_one({"_id": performer_id})
    if performer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Performer not found")

    new_order = await request.app.mongodb["orders"].insert_one({
        **order.model_dump(),
        "customer_id": customer_id,
        "performer_id": performer_id,
        "completed": False,
    })
    created_order = await request.app.mongodb["orders"].find_one(
        {"_id": new_order.inserted_id}
    )

    return created_order
