
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from itertools import count

app = FastAPI(
    title="Order Management API",
    version="1.0.0"
)


class Order(BaseModel):
    product_name: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class OrderStatus(BaseModel):
    status: Literal["created", "processing",
                    "completed", "cancelled"]


orders = []
order_ids = count(1)


@app.get("/")
def root():
    return {"message": "Welcome to Order Management API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/orders")
def get_orders():
    return orders


@app.post("/orders", status_code=201)
def create_order(order: Order):
    new_order = {
        "id": next(order_ids),
        "product_name": order.product_name,
        "quantity": order.quantity,
        "price": order.price,
        "total_price": order.quantity * order.price,
        "status": "created"
    }

    orders.append(new_order)
    return new_order


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )


@app.put("/orders/{order_id}")
def update_order(order_id: int, updated_order: Order):
    order = get_order(order_id)

    order["product_name"] = updated_order.product_name
    order["quantity"] = updated_order.quantity
    order["price"] = updated_order.price
    order["total_price"] = (
        updated_order.quantity * updated_order.price
    )

    return order


@app.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, data: OrderStatus):
    order = get_order(order_id)

    order["status"] = data.status

    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    order = get_order(order_id)

    orders.remove(order)

    return {"message": "Order deleted successfully"}
