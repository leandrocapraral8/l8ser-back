import requests
from django.utils import timezone
from .models import User
from django.contrib.auth.models import Group

def fetch_users():
    url = "https://l8group.freshdesk.com/api/v2/agents"
    api_key = "hMYwUkl5SRE95Jg0XDO"
    
    headers = {
        "Content-Type": "application/json"
    }

    while url:
        response = requests.get(url, auth=(api_key, 'X'), headers=headers)
        
        if response.status_code == 200:
            users_data = response.json()

            filtered_agents = [
                agent for agent in users_data
                if agent.get('contact', {}).get('email', '').endswith('@l8security.com.br')
            ]

            for user in filtered_agents:
                email = user.get('contact', {}).get('email', '')
                full_name = user.get('contact', {}).get('name', '')
                first_name, _, last_name = full_name.partition(' ')
                if not User.objects.filter(email=email).exists():
                    new_user = User.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=user.get('contact', {}).get('email', ''),
                        username=user.get('contact', {}).get('email', ''),
                        freshdesk_id=user.get('id'),
                        user_type='collaborator'
                    )
                    new_user.groups.add(Group.objects.get(name='Collaborator'))

            link_header = response.headers.get('link')
            if link_header:
                url = link_header.split(';')[0].strip('<>')
            else:
                url = None
        else:
            return f"Error fetching users: {response.status_code}"

    return "Users created successfully!"