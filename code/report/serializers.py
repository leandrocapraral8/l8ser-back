from rest_framework import serializers

from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Report
        fields = "__all__"
        depth = 1


# class FreshdeskTicketSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = FreshdeskTicket
#         fields = "__all__"