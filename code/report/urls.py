from rest_framework import routers

from .views import ReportViewSet

reports_router = routers.SimpleRouter()
reports_router.register(r'reports', ReportViewSet)

# tickets_router = routers.SimpleRouter()
# tickets_router.register(r'tickets', FreshdeskTicketViewSet)
