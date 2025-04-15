from django.contrib import admin
from django.urls import path, include
from . import urls_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls_api)),
]
