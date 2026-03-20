# 🍔 Food Delivery API – FastAPI Project

This is a **FastAPI backend project** developed as part of the **February 2026 Internship**.  
The project simulates a real-world **Food Delivery Application Backend** with full CRUD operations, cart system, and order processing.

---

## 🚀 Project Features

- ✅ Menu Management (Add, Update, Delete Food Items)
- ✅ Filter, Search, Sort & Pagination
- ✅ Cart System (Add, Remove, View Items)
- ✅ Order Placement System
- ✅ Pydantic Validation
- ✅ REST API Design using FastAPI
- ✅ Swagger UI for API Testing

---

## 🛠️ Tech Stack

- **Python 3**
- **FastAPI**
- **Pydantic**
- **Uvicorn**

---

## 📂 Project Structure


YOUR_INTERNID_FASTAPI/
└── FINAL_PROJECT/
├── main.py
├── requirements.txt
├── README.md
└── screenshots/


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository


git clone https://github.com/Vyshnavi-1108/YOUR_INTERNID_FASTAPI.git

cd YOUR_INTERNID_FASTAPI


---

### 2️⃣ Install Dependencies


pip install -r requirements.txt


---

### 3️⃣ Run the Server


uvicorn main:app --reload


---

### 4️⃣ Open Swagger UI


http://127.0.0.1:8000/docs


---

## 📌 API Endpoints Overview

### 🥗 Menu APIs
- GET `/menu` → Get all food items  
- GET `/menu/{id}` → Get single item  
- POST `/menu` → Add food item  
- PUT `/menu/{id}` → Update food  
- DELETE `/menu/{id}` → Delete food  

### 🔍 Advanced Features
- GET `/menu/filter` → Filter food  
- GET `/menu/search` → Search food  
- GET `/menu/sort` → Sort by price  
- GET `/menu/paginate` → Pagination  

### 🛒 Cart APIs
- POST `/cart/add` → Add item to cart  
- GET `/cart` → View cart  
- DELETE `/cart/{id}` → Remove item  

### 📦 Order APIs
- POST `/cart/checkout` → Place order  
- GET `/orders` → View all orders  

---

## 🔄 Workflow

1. View Menu  
2. Add items to Cart  
3. Checkout  
4. Order gets created  

---

## 📸 Screenshots

Add your screenshots here:


screenshots/
├── Q1_Output.png
├── Q2_Output.png
├── Q3_Output.png


---

## 🎯 Project Objective

This project demonstrates:
- API development using FastAPI  
- Backend system design  
- Real-world application flow  
- CRUD + Business Logic Implementation  

---

## 🔗 GitHub Repository

👉 https://github.com/Vyshnavi-1108/YOUR_INTERNID_FASTAPI

---

## 📢 LinkedIn Submission

This project is part of the **Innomatics Research Labs Internship Program**.

---

## 🙌 Author

**Vyshnavi**  
FastAPI Intern 🚀  
