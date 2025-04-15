import random
from datetime import datetime

# In-memory data
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

def calculate_discounted_price(price, discount_rate):
    return price * (1 - discount_rate / 100)

def generate_transaction_id():
    return random.randint(100000, 999999)

def record_transaction(user_id, product_id, quantity, total_price):
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
