from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import random

app = FastAPI()

# --- In-memory Data ---

users = [
    {"id": 1, "name": "Alice", "balance": 1000.0},
    {"id": 2, "name": "Bob", "balance": 750.0},
    {"id": 3, "name": "Charlie", "balance": 500.0}
]

products = [
    {"id": 1, "name": "Widget", "price": 19.99},
    {"id": 2, "name": "Gadget", "price": 29.99},
    {"id": 3, "name": "Doohickey", "price": 9.99}
]

transactions = []

# --- Models ---

class PurchaseRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1
    discount_rate: float = 0.0

class RechargeRequest(BaseModel):
    user_id: int
    amount: float

# --- Helpers ---

def calculate_discounted_price(price: float, discount_rate: float) -> float:
    return price * (1 - discount_rate / 100)

def generate_transaction_id() -> int:
    return random.randint(100000, 999999)

def record_transaction(user_id: int, product_id: int, quantity: int, total_price: float):
    transaction = {
        "transaction_id": generate_transaction_id(),
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity,
        "total_price": total_price,
        "timestamp": datetime.now().isoformat()
    }
    transactions.append(transaction)
    return transaction

# --- Routes ---

@app.get("/users")
def get_users():
    return {"users": users}

@app.get("/products")
def get_products():
    return {"products": products}

@app.get("/transactions")
def get_transactions(user_id: Optional[int] = Query(None)):
    if user_id:
        filtered = [t for t in transactions if t["user_id"] == user_id]
        return {"transactions": filtered}
    return {"transactions": transactions}

@app.post("/purchase")
def purchase_product(request: PurchaseRequest):
    user = next((u for u in users if u["id"] == request.user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = next((p for p in products if p["id"] == request.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    discounted_price = calculate_discounted_price(product["price"], request.discount_rate)
    total_price = discounted_price * request.quantity

    if user["balance"] < total_price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user["balance"] -= total_price
    transaction = record_transaction(request.user_id, request.product_id, request.quantity, total_price)

    return {
        "message": "Purchase successful",
        "transaction": transaction,
        "new_balance": user["balance"]
    }

@app.post("/recharge")
def recharge_account(request: RechargeRequest):
    user = next((u for u in users if u["id"] == request.user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["balance"] += request.amount
    return {
        "message": "Recharge successful",
        "new_balance": user["balance"]
    }

@app.get("/summary")
def summary():
    total_users = len(users)
    total_transactions = len(transactions)
    total_revenue = sum(t["total_price"] for t in transactions)
    return {
        "total_users": total_users,
        "total_transactions": total_transactions,
        "total_revenue": round(total_revenue, 2)
    }
