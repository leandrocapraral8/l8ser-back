import requests
from django.utils import timezone
from .models import Customer

def fetch_customers():
    url = "https://l8group.freshdesk.com/api/v2/companies"
    api_key = "hMYwUkl5SRE95Jg0XDO"
    
    headers = {
        "Content-Type": "application/json"
    }

    while url:
        response = requests.get(url, auth=(api_key, 'X'), headers=headers)
        
        if response.status_code == 200:
            customers_data = response.json()

            for customer in customers_data:
                name = customer.get('name', '')
                if not Customer.objects.filter(name=name).exists():
                    domains = customer.get('domains', [])
                    domains_str = ', '.join(domains)
                    Customer.objects.create(
                        name=name,
                        description=customer.get('description', ''),
                        note=customer.get('note', ''),
                        domains=domains_str,
                        freshdesk_id=customer.get('id'),
                        creation_date=customer.get('created_at', timezone.now()),
                        ativa=customer.get('custom_fields', {}).get('ativa', False),
                        l8security=customer.get('custom_fields', {}).get('l8security', False)
                    )

            link_header = response.headers.get('link')
            if link_header:
                url = link_header.split(';')[0].strip('<>')
            else:
                url = None
        else:
            return f"Error fetching customers: {response.status_code}"

    return "Customers created successfully!"