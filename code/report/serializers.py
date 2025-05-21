from rest_framework import serializers

from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    month_and_year = serializers.CharField(read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
        depth = 1
    
    def get_month_and_year(self, obj):
        return obj.month_and_year


# class FreshdeskTicketSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = FreshdeskTicket
#         fields = "__all__"