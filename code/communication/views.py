from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Communication
from .serializers import CommunicationCreateSerializer, CommunicationListSerializer

class CommunicationViewSet(viewsets.ModelViewSet):
    queryset = Communication.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'description': ['exact', 'icontains']}
    ordering_fields = ("__all__")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Communication.objects.all()
        return Communication.objects.filter(customer=self.request.user.customer)

    def get_serializer_class(self):
        if self.action == 'create':
            return CommunicationCreateSerializer 
        return CommunicationListSerializer 

    def perform_create(self, serializer):
        serializer.save()
