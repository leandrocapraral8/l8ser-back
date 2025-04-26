from rest_framework import routers

from .views import CustomerViewSet

customers_router = routers.SimpleRouter()
customers_router.register(r'customers', CustomerViewSet)
