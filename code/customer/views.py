from rest_framework import permissions, viewsets
from .models import Customer
from .serializers import CustomerSerializer
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'name': ['exact', 'icontains'],}
    ordering_fields = ("__all__")
    