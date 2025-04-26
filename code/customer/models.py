from django.db import models
from django.utils import timezone
from product.models import Product

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    domains = models.TextField(blank=True, null=True)
    freshdesk_id = models.IntegerField(unique=True)
    creation_date = models.DateTimeField(default=timezone.now)
    ativa = models.BooleanField(default=False, null=True)
    l8security = models.BooleanField(default=False, null=True)
    products = models.ManyToManyField(Product, related_name='customers')
    
    def __str__(self):
        return self.name

    @property
    def domain_list(self):
        return self.domains.split(', ')

    @domain_list.setter
    def domain_list(self, value):
        self.domains = ', '.join(value)
    
    class Meta:
        ordering = ['name']
    