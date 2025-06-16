from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from .views import CustomTokenObtainPairView
from rest_framework import routers

from users.urls import users_router
from customer.urls import customers_router
from product.urls import products_router, productcategories_router
from report.urls import reports_router
from communication.urls import communications_router

router = routers.DefaultRouter()
#Users
router.registry.extend(users_router.registry)

#Customer
router.registry.extend(customers_router.registry)

#Product
router.registry.extend(products_router.registry)
router.registry.extend(productcategories_router.registry)

#Reports
router.registry.extend(reports_router.registry)

#Communications
router.registry.extend(communications_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),

    #General routes
    path('', include(router.urls)),

    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Swagger
# OpenAPI 3 documentation with Swagger UI
urlpatterns.append(path('schema/', SpectacularAPIView.as_view(urlconf=urlpatterns), name="schema"))

urlpatterns.append(path('docs/', SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"))
