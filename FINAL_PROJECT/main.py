from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# ================= MODELS =================

class FoodItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str
    available: bool = True


class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    address: str = Field(..., min_length=5)


# ================= DATA =================

menu = [
    {"id": 1, "name": "Burger", "price": 120, "category": "FastFood", "available": True},
    {"id": 2, "name": "Pizza", "price": 250, "category": "FastFood", "available": True},
    {"id": 3, "name": "Biryani", "price": 180, "category": "MainCourse", "available": False},
]

cart = []
orders = []
order_id_counter = 1


# ================= HELPER =================

def find_food(food_id):
    for item in menu:
        if item["id"] == food_id:
            return item
    return None


# ================= HOME =================

@app.get("/")
def home():
    return {"message": "Welcome to Food Delivery API"}


# ================= MENU =================

@app.get("/menu")
def get_menu():
    return {"menu": menu}


# ⚠️ IMPORTANT: KEEP FIXED ROUTES BEFORE VARIABLE ROUTE

# filter menu ✅ FIXED
@app.get("/menu/filter")
def filter_menu(
    category: str = Query(None),
    available: bool = Query(None)
):
    result = menu

    if category:
        result = [i for i in result if i["category"].lower() == category.lower()]

    if available is not None:
        result = [i for i in result if i["available"] == available]

    return {"filtered": result}


# search menu ✅ FIXED
@app.get("/menu/search")
def search_food(keyword: str = Query(...)):
    result = [i for i in menu if keyword.lower() in i["name"].lower()]
    return {"results": result}


# sort menu
@app.get("/menu/sort")
def sort_menu(order: str = Query("asc")):
    sorted_menu = sorted(menu, key=lambda x: x["price"], reverse=(order == "desc"))
    return {"sorted": sorted_menu}


# pagination
@app.get("/menu/paginate")
def paginate(skip: int = 0, limit: int = 2):
    return {"data": menu[skip: skip + limit]}


# 🔴 VARIABLE ROUTE MUST BE LAST
@app.get("/menu/{food_id}")
def get_food(food_id: int):
    item = find_food(food_id)
    if not item:
        return {"error": "Food not found"}
    return item


# ================= CRUD =================

@app.post("/menu")
def add_food(item: FoodItem, response: Response):
    new_id = max(i["id"] for i in menu) + 1

    food = {
        "id": new_id,
        "name": item.name,
        "price": item.price,
        "category": item.category,
        "available": item.available
    }

    menu.append(food)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Food added", "food": food}


@app.put("/menu/{food_id}")
def update_food(
    food_id: int,
    available: bool = Query(None),
    price: int = Query(None)
):
    item = find_food(food_id)

    if not item:
        return {"error": "Food not found"}

    if available is not None:
        item["available"] = available

    if price is not None:
        item["price"] = price

    return {"message": "Updated", "food": item}


@app.delete("/menu/{food_id}")
def delete_food(food_id: int):
    item = find_food(food_id)

    if not item:
        return {"error": "Food not found"}

    menu.remove(item)
    return {"message": "Deleted"}


# ================= CART =================

@app.post("/cart/add")
def add_to_cart(
    food_id: int = Query(...),
    quantity: int = Query(1)
):
    item = find_food(food_id)

    if not item:
        return {"error": "Food not found"}

    if not item["available"]:
        return {"error": "Food not available"}

    cart_item = {
        "food_id": food_id,
        "name": item["name"],
        "quantity": quantity,
        "price": item["price"],
        "total": item["price"] * quantity
    }

    cart.append(cart_item)
    return {"message": "Added to cart", "item": cart_item}


@app.get("/cart")
def view_cart():
    total = sum(i["total"] for i in cart)
    return {"cart": cart, "total": total}


@app.delete("/cart/{food_id}")
def remove_cart(food_id: int):
    for i in cart:
        if i["food_id"] == food_id:
            cart.remove(i)
            return {"message": "Removed"}
    return {"error": "Item not in cart"}


# ================= ORDERS =================

@app.post("/cart/checkout")
def checkout(order: OrderRequest):
    global order_id_counter

    if not cart:
        return {"error": "Cart empty"}

    total = sum(i["total"] for i in cart)

    new_order = {
        "order_id": order_id_counter,
        "customer": order.customer_name,
        "address": order.address,
        "items": cart.copy(),
        "total": total
    }

    orders.append(new_order)
    cart.clear()
    order_id_counter += 1

    return {"message": "Order placed", "order": new_order}


@app.get("/orders")
def get_orders():
    return {"orders": orders}