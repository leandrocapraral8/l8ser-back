from rest_framework import serializers

from .models import Communication
from customer.models import Customer

class CommunicationListSerializer(serializers.ModelSerializer):
    customers = serializers.SerializerMethodField(read_only=True)
    sent_by = serializers.CharField(read_only=True)
    
    class Meta:
        model = Communication
        fields = [
            'id', 'customers', 'date_start', 'date_end', 'description',
            'incident_detail', 'incident_treatment', 'message', 'alert_source',
            'incident_severity', 'impact_type', 'notification_time', 'sent_by'
        ]

    def get_customers(self, obj):
        return [customer.name for customer in obj.customer.all()]
    
class CommunicationCreateSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        many=True,
        source="customers"
    )

    class Meta:
        model = Communication
        fields = [
            'id', 'customer', 'date_start', 'date_end', 'description',
            'incident_detail', 'incident_treatment', 'message', 'alert_source',
            'incident_severity', 'impact_type', 'notification_time', 'sent_by'
        ]
