from rest_framework import routers

from .views import CommunicationViewSet

communications_router = routers.SimpleRouter()
communications_router.register(r'communications', CommunicationViewSet)
