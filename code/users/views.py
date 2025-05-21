from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('email',)
    ordering_fields = ("__all__")

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     if not serializer.is_valid():
    #         print(f"Erros de validação: {serializer.errors}")
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def me(self, request):
        self.kwargs['pk'] = request.user.pk

        if request.method == 'GET':
            return self.retrieve(request)
        else:
            raise Exception('Not implemented')
    