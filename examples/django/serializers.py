from rest_framework import serializers

class PurchaseRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    discount_rate = serializers.FloatField(default=0.0)

class RechargeRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.FloatField()
