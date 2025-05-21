import calendar
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from django.utils import timezone
from datetime import datetime
from report.utils import fetch_tickets, get_month_start_end_dates
from .models import Report
from .serializers import ReportSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    filter_backends = [DjangoFilterBackend]
    filter_fields = ()
    ordering_fields = ("__all__")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Report.objects.all()
        return Report.objects.filter(customer=self.request.user.customer)

# class GenerateReportView(APIView):
#     def get(self, request, format=None):
#         report_id = request.query_params.get('report_id')
#         if not report_id:
#             return Response({"error": "Report ID não fornecido"}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             report = Report.objects.get(id=report_id)
#         except Report.DoesNotExist:
#             return Response({"error": "Report não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
#         tickets = fetch_tickets()
#         if isinstance(tickets, str):
#             return Response({"error": tickets}, status=status.HTTP_400_BAD_REQUEST)
#         resumo = self.gerar_resumo(tickets)

#         report.freshdesk_info = resumo
#         report.save()
        
#         return Response(resumo, status=status.HTTP_200_OK)

#     @staticmethod
#     def gerar_resumo(tickets):
#         first_day, last_day = get_month_start_end_dates(timezone.now())
        
#         filtered_tickets = [ticket for ticket in tickets if first_day <= datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ') <= last_day]

#         resumo = {
#             "total_tickets": len(filtered_tickets),
#             "tickets_prioridade_alta": len([ticket for ticket in filtered_tickets if ticket.get('priority') == 1]),
#             "tickets_por_atendente": GenerateReportView.tickets_por_atendente(filtered_tickets)
#         }

#         return resumo

#     @staticmethod
#     def tickets_por_atendente(tickets):
#         atendentes = {}
#         for ticket in tickets:
#             responder_id = ticket.get('responder_id')
#             if responder_id in atendentes:
#                 atendentes[responder_id] += 1
#             else:
#                 atendentes[responder_id] = 1
#         return atendentes

# from rest_framework import permissions, viewsets, status
# from rest_framework.response import Response
# from .models import Report, FreshdeskTicket
# from .serializers import ReportSerializer, FreshdeskTicketSerializer
# from django_filters.rest_framework import DjangoFilterBackend


# class ReportViewSet(viewsets.ModelViewSet):
#     queryset = Report.objects.all()
#     serializer_class = ReportSerializer
#     permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
#     filter_backends = [DjangoFilterBackend]
#     filter_fields = ()
#     ordering_fields = ("__all__")


# class FreshdeskTicketViewSet(viewsets.ModelViewSet):
#     queryset = FreshdeskTicket.objects.all()
#     serializer_class = FreshdeskTicketSerializer
#     permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
#     filter_backends = [DjangoFilterBackend]
#     filter_fields = ()
#     ordering_fields = ("__all__")