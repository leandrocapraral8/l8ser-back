from rest_framework import routers

from .views import ProductViewSet, ProductCategoryViewSet

productcategories_router = routers.SimpleRouter()
productcategories_router.register(r'productcategories', ProductCategoryViewSet)

products_router = routers.SimpleRouter()
products_router.register(r'products', ProductViewSet)
