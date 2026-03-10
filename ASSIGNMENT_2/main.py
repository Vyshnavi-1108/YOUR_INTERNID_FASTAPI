# importing required libraries
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

# creating FastAPI app
app = FastAPI()

# sample product database (list of dictionaries)
products = [
    {"id": 1, "name": "Wireless Mouse", "category": "electronics", "price": 500, "in_stock": True},
    {"id": 2, "name": "Keyboard", "category": "electronics", "price": 700, "in_stock": True},
    {"id": 3, "name": "Headphones", "category": "electronics", "price": 1200, "in_stock": False},
    {"id": 4, "name": "Notebook", "category": "stationery", "price": 100, "in_stock": True},
    {"id": 5, "name": "Pen Pack", "category": "stationery", "price": 200, "in_stock": True}
]

# list to store feedback
feedback = []

# -------------------------------
# TASK 1 : Filter products
# -------------------------------
@app.get("/products/filter")
def filter_products(
    category: str = Query(None),
    max_price: int = Query(None),
    min_price: int = Query(None)
):

    # start with full product list
    result = products

    # filter by category
    if category:
        result = [p for p in result if p["category"] == category]

    # filter by maximum price
    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    # filter by minimum price
    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    return result


# -------------------------------
# TASK 2 : Get product price only
# -------------------------------
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    # searching product by id
    for product in products:

        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    # if product not found
    return {"error": "Product not found"}


# -------------------------------
# TASK 3 : Customer Feedback Model
# -------------------------------
class CustomerFeedback(BaseModel):

    # name must have minimum 2 characters
    customer_name: str = Field(..., min_length=2)

    # product id must be greater than 0
    product_id: int = Field(..., gt=0)

    # rating must be between 1 and 5
    rating: int = Field(..., ge=1, le=5)

    # comment is optional
    comment: Optional[str] = Field(None, max_length=300)


# endpoint to submit feedback
@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    # saving feedback
    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }


# -------------------------------
# TASK 4 : Product Summary
# -------------------------------
@app.get("/products/summary")
def product_summary():

    # products available in stock
    in_stock = [p for p in products if p["in_stock"]]

    # products not available
    out_stock = [p for p in products if not p["in_stock"]]

    # most expensive product
    expensive = max(products, key=lambda p: p["price"])

    # cheapest product
    cheapest = min(products, key=lambda p: p["price"])

    # unique product categories
    categories = list(set(p["category"] for p in products))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {
            "name": expensive["name"],
            "price": expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }


# -------------------------------
# TASK 5 : Bulk Order System
# -------------------------------

# model for order item
class OrderItem(BaseModel):

    # product id must be positive
    product_id: int = Field(..., gt=0)

    # quantity must be between 1 and 50
    quantity: int = Field(..., gt=0, le=50)


# model for bulk order
class BulkOrder(BaseModel):

    # company name
    company_name: str = Field(..., min_length=2)

    # contact email
    contact_email: str

    # list of order items
    items: List[OrderItem]


# endpoint to place bulk order
@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    # loop through each order item
    for item in order.items:

        product = None

        # searching product
        for p in products:
            if p["id"] == item.product_id:
                product = p
                break

        # product not found
        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        # product out of stock
        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
            continue

        # calculating subtotal
        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed_orders": confirmed,
        "failed_orders": failed,
        "grand_total": grand_total
    }