from django.contrib import admin
from .models import Report
from .utils import fetch_tickets, gerar_resumo_freshdesk, fetch_checkpoint_info

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('customer', 'month', 'user')
    actions = ['gerar_resumo_freshdesk_action', 'gerar_resumo_checkpoint_action']

    def gerar_resumo_freshdesk_action(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "Por favor, selecione apenas um relatório por vez.", level='error')
            return

        report_id = queryset.first().id
        customer_name = queryset.first().customer.name.upper()
        date = queryset.first().month
        if not report_id:
            self.message_user(request, f"Report ID não fornecido")
        
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist: 
            self.message_user(request, f"Report não encontrado")
        
        try:
            tickets = fetch_tickets()
            if isinstance(tickets, str):
                self.message_user(request, f"Erro ao buscar tickets: {tickets}")
                return

            resumo = gerar_resumo_freshdesk(tickets, date, customer_name)

            report.freshdesk_info = resumo
            report.save()

            self.message_user(request, "Resumo do Freshdesk gerado com sucesso!")
        except Exception as e:
            self.message_user(request, f"Erro ao gerar resumo do Freshdesk: {str(e)}", level='error')

    gerar_resumo_freshdesk_action.short_description = "Gerar Resumo Freshdesk"


    def gerar_resumo_checkpoint_action(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "Por favor, selecione apenas um relatório por vez.", level='error')
            return

        report_id = queryset.first().id
        date = queryset.first().month

        if not report_id or not date:
            self.message_user(request, "Report ID ou data não fornecidos.", level='error')
            return

        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            self.message_user(request, "Report não encontrado.", level='error')
            return
        except Exception as e:
            self.message_user(request, f"Erro inesperado ao buscar o Report: {str(e)}", level='error')
            return

        try:
            resumo = fetch_checkpoint_info(date)
            if resumo is None:
                self.message_user(request, "Erro ao gerar o resumo: dados inválidos ou API falhou.", level='error')
                return
            
            report.checkpoint_info = resumo
            report.save()
            self.message_user(request, "Resumo do Checkpoint gerado com sucesso!")
        except Exception as e:
            self.message_user(request, f"Erro ao gerar resumo do Checkpoint: {str(e)}", level='error')

    gerar_resumo_checkpoint_action.short_description = "Gerar Resumo Checkpoint"
