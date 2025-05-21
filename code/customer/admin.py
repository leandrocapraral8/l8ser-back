from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import Customer
from .utils import fetch_customers

class DomainFilter(admin.SimpleListFilter):
    title = 'domain'
    parameter_name = 'domain'

    def lookups(self, request, model_admin):
        all_domains = set()
        for customer in Customer.objects.all():
            all_domains.update(customer.domain_list)
        return [(domain, domain) for domain in all_domains]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(domains__icontains=self.value())
        return queryset

def get_customers_by_domain(domain):
    return Customer.objects.filter(domains__icontains=domain)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'domains', 'freshdesk_id', 'ativa', 'l8security')
    list_filter = ('l8security', 'ativa', DomainFilter)
    filter_horizontal = ('products',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('fetch-create-companies/', self.admin_site.admin_view(self.fetch_and_create_companies_action), name='fetch-create-companies'),
        ]
        return custom_urls + urls

    def fetch_and_create_companies_action(self, request):
        message = fetch_customers()
        self.message_user(request, message)
        return redirect('..')

    def fetch_and_create_companies_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Fetch and Create Companies</a>',
            '/admin/customer/fetch-create-companies/'
        )
    fetch_and_create_companies_button.short_description = 'Fetch and Create Companies'
    fetch_and_create_companies_button.allow_tags = True

    change_list_template = 'customer/change_list_with_button.html'
