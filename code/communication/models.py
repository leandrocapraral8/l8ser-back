from django.db import models
from customer.models import Customer
from users.models import User

# Create your models here.
class Communication(models.Model):
    SEVERITY_CHOICES = [
        ('altissimo', 'Altíssimo'),
        ('alto', 'Alto'),
        ('elevado', 'Elevado'),
        ('medio', 'Médio'),
        ('baixo', 'Baixo'),
    ]

    IMPACT_TYPE_CHOICES = [
        ('confidencialidade', 'Confidencialidade'),
        ('integridade', 'Alto'),
        ('disponibilidade', 'Elevado'),
    ]

    customer = models.ManyToManyField(Customer, related_name='communications')
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    incident_detail = models.TextField()
    incident_treatment = models.TextField()
    message = models.TextField()
    alert_source = models.CharField(max_length=255)
    incident_severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    impact_type = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    notification_time = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description
    