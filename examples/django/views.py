from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .data import users, products, transactions, calculate_discounted_price, record_transaction
from .serializers import PurchaseRequestSerializer, RechargeRequestSerializer

@api_view(['GET'])
def get_users(request):
    return Response({"users": users})

@api_view(['GET'])
def get_products(request):
    return Response({"products": products})

@api_view(['GET'])
def get_transactions(request):
    user_id = request.query_params.get("user_id")
    if user_id:
        filtered = [t for t in transactions if t["user_id"] == int(user_id)]
        return Response({"transactions": filtered})
    return Response({"transactions": transactions})

@api_view(['POST'])
def purchase_product(request):
    serializer = PurchaseRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        user = next((u for u in users if u["id"] == data["user_id"]), None)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        product = next((p for p in products if p["id"] == data["product_id"]), None)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        discounted_price = calculate_discounted_price(product["price"], data["discount_rate"])
        total_price = discounted_price * data["quantity"]

        if user["balance"] < total_price:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        user["balance"] -= total_price
        transaction = record_transaction(data["user_id"], data["product_id"], data["quantity"], total_price)

        return Response({
            "message": "Purchase successful",
            "transaction": transaction,
            "new_balance": user["balance"]
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def recharge_account(request):
    serializer = RechargeRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        user = next((u for u in users if u["id"] == data["user_id"]), None)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user["balance"] += data["amount"]
        return Response({
            "message": "Recharge successful",
            "new_balance": user["balance"]
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def summary(request):
    total_users = len(users)
    total_transactions = len(transactions)
    total_revenue = round(sum(t["total_price"] for t in transactions), 2)
    return Response({
        "total_users": total_users,
        "total_transactions": total_transactions,
        "total_revenue": total_revenue
    })
