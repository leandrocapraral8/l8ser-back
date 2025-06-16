from django.contrib import admin

from .models import Communication

class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('description', 'customer_names')
    filter_horizontal = ('customer',)

    def customer_names(self, obj):
        return ", ".join([customer.name for customer in obj.customer.all()])
    
    customer_names.short_description = "Customers"

admin.site.register(Communication, CommunicationAdmin)
