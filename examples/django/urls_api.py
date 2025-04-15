from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.get_users),
    path("products/", views.get_products),
    path("transactions/", views.get_transactions),
    path("purchase/", views.purchase_product),
    path("recharge/", views.recharge_account),
    path("summary/", views.summary),
]
