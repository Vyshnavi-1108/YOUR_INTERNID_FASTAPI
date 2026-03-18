from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# ================= MODELS =================

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    delivery_address: str = Field(..., min_length=10)

class NewProduct(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool = True

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

# ================= DATA =================

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook', 'price': 99, 'category': 'Stationery', 'in_stock': True},
    {'id': 3, 'name': 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set', 'price': 49, 'category': 'Stationery', 'in_stock': True},
]

orders = []
cart = []
order_counter = 1

# ================= HELPERS =================

def find_product(product_id):
    for p in products:
        if p['id'] == product_id:
            return p
    return None

def calculate_total(product, quantity):
    return product['price'] * quantity

# ================= DAY 1 =================

@app.get("/")
def home():
    return {"message": "Welcome to E-commerce API"}

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

@app.get("/products/{product_id}")
def get_single_product(product_id: int):
    product = find_product(product_id)
    if not product:
        return {"error": "Product not found"}
    return {"product": product}

# ================= DAY 2 =================

@app.get("/products/filter")
def filter_products(
    category: str = Query(None),
    min_price: int = Query(None),
    max_price: int = Query(None),
    in_stock: bool = Query(None)
):
    result = products

    if category:
        result = [p for p in result if p['category'] == category]

    if min_price:
        result = [p for p in result if p['price'] >= min_price]

    if max_price:
        result = [p for p in result if p['price'] <= max_price]

    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]

    return {"filtered_products": result, "count": len(result)}

@app.post("/orders")
def place_order(order_data: OrderRequest, response: Response):
    global order_counter

    product = find_product(order_data.product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    if not product['in_stock']:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Out of stock"}

    total = calculate_total(product, order_data.quantity)

    order = {
        "order_id": order_counter,
        "customer_name": order_data.customer_name,
        "product": product['name'],
        "quantity": order_data.quantity,
        "delivery_address": order_data.delivery_address,
        "total_price": total
    }

    orders.append(order)
    order_counter += 1

    return {"message": "Order placed", "order": order}

@app.get("/orders")
def get_orders():
    return {"orders": orders}

# ================= DAY 3 =================

@app.get("/products/compare")
def compare_products(
    product_id_1: int = Query(...),
    product_id_2: int = Query(...)
):
    p1 = find_product(product_id_1)
    p2 = find_product(product_id_2)

    if not p1 or not p2:
        return {"error": "Invalid product ID"}

    cheaper = p1 if p1['price'] < p2['price'] else p2

    return {
        "product_1": p1,
        "product_2": p2,
        "cheaper": cheaper['name']
    }

# ================= DAY 4 =================

@app.post("/products")
def add_product(new_product: NewProduct):
    new_id = max(p['id'] for p in products) + 1

    product = {
        "id": new_id,
        "name": new_product.name,
        "price": new_product.price,
        "category": new_product.category,
        "in_stock": new_product.in_stock
    }

    products.append(product)
    return {"message": "Product added", "product": product}

@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = Query(None), in_stock: bool = Query(None)):
    product = find_product(product_id)

    if not product:
        return {"error": "Product not found"}

    if price:
        product['price'] = price

    if in_stock is not None:
        product['in_stock'] = in_stock

    return {"message": "Updated", "product": product}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    product = find_product(product_id)

    if not product:
        return {"error": "Product not found"}

    products.remove(product)
    return {"message": "Deleted"}

# ================= DAY 5 =================

@app.post("/cart/add")
def add_to_cart(product_id: int = Query(...), quantity: int = Query(1)):
    product = find_product(product_id)

    if not product:
        return {"error": "Product not found"}

    item = {
        "product_id": product_id,
        "name": product['name'],
        "quantity": quantity,
        "subtotal": calculate_total(product, quantity)
    }

    cart.append(item)
    return {"message": "Added to cart", "cart": item}

@app.get("/cart")
def view_cart():
    total = sum(item['subtotal'] for item in cart)
    return {"cart": cart, "total": total}

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):
    global order_counter

    if not cart:
        return {"error": "Cart empty"}

    created_orders = []

    for item in cart:
        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "product": item['name'],
            "quantity": item['quantity'],
            "delivery_address": data.delivery_address,
            "total_price": item['subtotal']
        }
        orders.append(order)
        created_orders.append(order)
        order_counter += 1

    cart.clear()
    return {"message": "Checkout done", "orders": created_orders}

# ================= DAY 6 =================

@app.get("/products/search")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p['name'].lower()]
    return {"results": result}

@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):
    sorted_data = sorted(products, key=lambda x: x[sort_by], reverse=(order == "desc"))
    return {"products": sorted_data}

@app.get("/products/page")
def paginate(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return {"products": products[start:start + limit]}

@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [o for o in orders if customer_name.lower() in o['customer_name'].lower()]
    return {"orders": result}

@app.get("/products/sort-by-category")
def sort_category():
    return {"products": sorted(products, key=lambda x: (x['category'], x['price']))}

@app.get("/products/browse")
def browse(
    keyword: str = None,
    page: int = 1,
    limit: int = 2
):
    result = products

    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]

    start = (page - 1) * limit
    return {"products": result[start:start + limit]}

@app.get("/orders/page")
def orders_page(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return {"orders": orders[start:start + limit]}