from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ()
    ordering_fields = ("__all__")
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'category': ['exact'],
        'category__name': ['icontains'],
    }
    ordering_fields = ("__all__")
