from django.db import models
from customer.models import Customer
from users.models import User

class Report(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    month = models.DateField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    freshdesk_info = models.JSONField(null=True, blank=True, verbose_name="Freshdesk info: Item 5.1")
    checkpoint_info = models.JSONField(null=True, blank=True, verbose_name="Checkpoint info: Item 7.1")
    harmony_info = models.JSONField(null=True, blank=True, verbose_name="Harmony: Item 8.2")

    def __str__(self):
        return f'Report for {self.customer.name if self.customer else "No Customer"} - {self.month.strftime("%B %Y")}'
    