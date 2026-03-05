# Import FastAPI library
from fastapi import FastAPI

# Create FastAPI app
app = FastAPI()

# Sample product database (list of dictionaries)
products = [
    {"id": 1, "name": "Notebook", "price": 120, "category": "Stationery", "in_stock": True},
    {"id": 2, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Wireless Mouse", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "USB Cable", "price": 199, "category": "Electronics", "in_stock": True},

    # Task 1: Add new products
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1599, "category": "Electronics", "in_stock": False}
]


# ------------------------------
# Task 1: Show all products
# ------------------------------
@app.get("/products")
def get_products():
    # Return all products and total count
    return {
        "products": products,
        "total": len(products)
    }


# ------------------------------
# Task 2: Filter products by category
# ------------------------------
@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):

    # Find products matching the category
    result = [p for p in products if p["category"].lower() == category_name.lower()]

    # If no products found
    if len(result) == 0:
        return {"error": "No products found in this category"}

    return result


# ------------------------------
# Task 3: Show only in-stock products
# ------------------------------
@app.get("/products/instock")
def get_instock():

    # Filter products where in_stock = True
    available = [p for p in products if p["in_stock"] == True]

    return {
        "in_stock_products": available,
        "count": len(available)
    }


# ------------------------------
# Task 4: Store summary endpoint
# ------------------------------
@app.get("/store/summary")
def store_summary():

    # Count in-stock products
    in_stock_count = len([p for p in products if p["in_stock"]])

    # Out of stock products
    out_stock_count = len(products) - in_stock_count

    # Unique categories using set
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }


# ------------------------------
# Task 5: Search product by name
# ------------------------------
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    # Case insensitive search
    result = [p for p in products if keyword.lower() in p["name"].lower()]

    if len(result) == 0:
        return {"message": "No products matched your search"}

    return {
        "matched_products": result,
        "count": len(result)
    }


# ------------------------------
# Bonus Task: Best Deal & Premium Pick
# ------------------------------
@app.get("/products/deals")
def get_deals():

    # Find cheapest product
    cheapest = min(products, key=lambda p: p["price"])

    # Find most expensive product
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }