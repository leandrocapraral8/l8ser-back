import requests
import calendar
import json
import pytz
from datetime import datetime, timezone
from requests.exceptions import RequestException, Timeout, HTTPError
from users.models import User

## Freshdesk
def fetch_tickets():
    url = f'https://l8group.freshdesk.com/api/v2/tickets'
    api_key = "hMYwUkl5SRE95Jg0XDO"

    headers = {
        "Content-Type": "application/json"
    }
    
    all_tickets = []

    while url:
        response = requests.get(url, auth=(api_key, "X"), headers=headers)
        if response.status_code == 200:
            tickets_data = response.json()
            all_tickets.extend(tickets_data)

            link_header = response.headers.get('link')
            if link_header:
                links = link_header.split(',')
                next_url = None
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link.split(';')[0].strip('<>')
                        break
                url = next_url
            else:
                url = None
        else:
            return f"Error fetching tickets: {response.status_code}"

    return all_tickets

def gerar_resumo_freshdesk(tickets, date, customer_name):
    first_day, last_day = get_month_start_end_dates(date)
    
    try:
        filtered_tickets = [
            ticket for ticket in tickets
            if isinstance(ticket, dict)
            and first_day <= datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) <= last_day
            and customer_name in ticket.get('tags', [])
        ]
    except (KeyError, TypeError) as e:
        raise ValueError(f"Erro ao processar os tickets: {e}")

    resumo = {
        "total_tickets": len(filtered_tickets),
        "tickets_prioridade": {
            "baixa": len([ticket for ticket in filtered_tickets if ticket.get('priority') == 1]),
            "media": len([ticket for ticket in filtered_tickets if ticket.get('priority') == 2]),
            "alta": len([ticket for ticket in filtered_tickets if ticket.get('priority') == 3]),
            "urgente": len([ticket for ticket in filtered_tickets if ticket.get('priority') == 4]),
        },
        "tickets_status": {
            "resolvido": len([ticket for ticket in filtered_tickets if ticket.get('status') == 5]),
            "nao_resolvido": len([ticket for ticket in filtered_tickets if ticket.get('status') != 5]),
        },
        "tickets_por_atendente": tickets_por_atendente(filtered_tickets)
    }

    return resumo

def checkpoint_login():
    url = f'https://10.110.99.208:443/web_api/login'
    # api_key = "FewSKeHWvxh3ILpvxnDpMw=="
    api_key = "1aPKm8h00Iqwr3GwVcAhZQ=="
    # user = ''
    # password = ''

    # data = {
    #     "user": user,
    #     "password": password
    # }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps({"api-key": api_key}), verify=False)
        # response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

        try:
            response_json = response.json()
            if "sid" in response_json:
                return response_json["sid"]
            else:
                raise ValueError("Resposta JSON inválida: 'sid' não encontrado.")
        except json.JSONDecodeError:
            raise ValueError("Resposta da API não é um JSON válido.")

    except ConnectionError as e:
        raise Exception(f"Erro ao fazer login no Checkpoint: {e}")


## Checkpoint
def fetch_checkpoint_info(date):
    try:
        first_day, last_day = get_month_start_end_dates(date)
        br_tz = pytz.timezone('America/Sao_Paulo')
        if first_day.tzinfo is None:
            first_day = br_tz.localize(first_day).isoformat()
        else:
            first_day = first_day.astimezone(br_tz).isoformat()

        if last_day.tzinfo is None:
            last_day = br_tz.localize(last_day).isoformat()
        else:
            last_day = last_day.astimezone(br_tz).isoformat()


        url = f'https://10.110.99.208:443/web_api/show-logs'
        sid = checkpoint_login()

        headers = {
            "Content-Type": "application/json",
            "X-chkp-sid": sid
        }

        data = {
            "new-query": {
                "time-frame": "custom",
                "custom-start": first_day,
                "custom-end": last_day,
                "filter": "action:(Bypass OR Detect) AND product_family:Threat AND severity:(Medium OR High OR Critical) AND confidence_level:(Medium OR Medium-High OR High) AND type:(Log OR Alert OR Session) AND (attack:(\"Scanner Enforcement Violation\" OR \"Port Scan\" OR \"Novell NMAP Protocol Violation\"))"
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
        except Timeout:
            raise Exception("A requisição para a API expirou (timeout).")
        except HTTPError as e:
            raise Exception(f"Erro HTTP na requisição: {e}")
        except RequestException as e:
            raise Exception(f"Erro ao realizar a requisição: {e}")

        if response.status_code == 200:
            try:
                response_json = response.json()
                logs = response_json.get("logs", [])

                hosts_scanned = set()
                scanner_counts = {}
                protection_counts = {}
                hosts_scanned_table = []
                scanners_table = []

                for log in logs:
                    dst_attr = log.get("dst_attr")
                    if dst_attr and isinstance(dst_attr, list) and dst_attr[0].get("resolved"):
                        host_resolved = dst_attr[0]["resolved"]
                        hosts_scanned.add(host_resolved)

                    src = log.get("src")
                    dst = log.get("dst")
                    service_id = log.get("service_id")
                    if src:
                        scanner_counts[src] = scanner_counts.get(src, 0) + 1

                    protection = log.get("protection_name")
                    if protection:
                        protection_counts[protection] = protection_counts.get(protection, 0) + 1

                    if src and host_resolved and dst:
                        hosts_scanned_table.append({"Scanner": src, "Host": f"{host_resolved + ' ' + dst}"})
                        scanners_table.append({"Host": host_resolved,"Scanner": src,"Service": service_id})

                top_scanning_attempts_per_scanner = dict(scanner_counts)
                top_protections = dict(protection_counts)

                resumo = {
                    "amount_hosts_scanned": len(hosts_scanned),
                    "hosts_scanned": hosts_scanned_table,
                    "scanners": scanners_table,
                    "top_scanning_attempts_per_scanner": top_scanning_attempts_per_scanner,
                    "top_protections": top_protections,
                }

                return resumo

            except (ValueError, KeyError, TypeError) as e:
                raise Exception(f"Erro ao processar o JSON da API: {e}")
        else:
            raise Exception(f"Erro na requisição à API: {response.status_code}")

    except Exception as e:
        print(f"Erro geral na execução de fetch_checkpoint_info: {e}")
        return None


def tickets_por_atendente(tickets):
    responder_ids = {ticket.get('responder_id') for ticket in tickets if ticket.get('responder_id')}
    users = User.objects.filter(freshdesk_id__in=responder_ids)
    user_map = {str(user.freshdesk_id): f"{user.first_name} {user.last_name}" for user in users}
    
    atendentes = {}

    for ticket in tickets:
        responder_id = ticket.get('responder_id')
        if responder_id:
            full_name = user_map.get(str(responder_id), "Desconhecido")
        else:
            full_name = "Desconhecido"

        atendentes[full_name] = atendentes.get(full_name, 0) + 1


    return atendentes

def get_month_start_end_dates(date):
    year, month = date.year, date.month
    first_day = datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59, tzinfo=timezone.utc)
    return first_day, last_day
