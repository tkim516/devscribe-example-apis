from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Mock database
customers = {}
charges = {}
subscriptions = {}

# Authentication Middleware
def authenticate():
    api_key = request.headers.get("Authorization")
    if not api_key or api_key != "Bearer test_secret_key":
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/v1/customers", methods=["POST"])
def create_customer():
    auth_error = authenticate()
    if auth_error:
        return auth_error
    
    data = request.json
    customer_id = f"cus_{uuid.uuid4().hex}"
    customers[customer_id] = {"id": customer_id, "email": data.get("email"), "name": data.get("name"), "balance": 0}
    return jsonify(customers[customer_id]), 201

@app.route("/v1/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    auth_error = authenticate()
    if auth_error:
        return auth_error
    
    customer = customers.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer)

@app.route("/v1/charges", methods=["POST"])
def create_charge():
    auth_error = authenticate()
    if auth_error:
        return auth_error
    
    data = request.json
    charge_id = f"ch_{uuid.uuid4().hex}"
    charges[charge_id] = {"id": charge_id, "amount": data.get("amount"), "currency": data.get("currency", "usd"), "customer": data.get("customer"), "status": "succeeded"}
    return jsonify(charges[charge_id]), 201

@app.route("/v1/charges/<charge_id>", methods=["GET"])
def get_charge(charge_id):
    auth_error = authenticate()
    if auth_error:
        return auth_error
    
    charge = charges.get(charge_id)
    if not charge:
        return jsonify({"error": "Charge not found"}), 404
    return jsonify(charge)

@app.route("/v1/subscriptions", methods=["POST"])
def create_subscription():
    auth_error = authenticate()
    if auth_error:
        return auth_error
    
    data = request.json
    subscription_id = f"sub_{uuid.uuid4().hex}"
    subscriptions[subscription_id] = {"id": subscription_id, "customer": data.get("customer"), "status": "active", "plan": data.get("plan"), "interval": "monthly"}
    return jsonify(subscriptions[subscription_id]), 201

@app.route("/v1/subscriptions/<subscription_id>", methods=["GET"])
def get_subscription(subscription_id):
    auth_error = authenticate()
    if auth_error:
        return auth_error
    
    subscription = subscriptions.get(subscription_id)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404
    return jsonify(subscription)

if __name__ == "__main__":
    app.run(debug=True)
