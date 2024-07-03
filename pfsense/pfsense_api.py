from time import sleep
import requests
import ipaddress

#endpoints api
static_ip_endpoint = "/api/v1/services/dhcpd/static_mapping"
dns_endpoint = "/api/v1/services/unbound/host_override"
vpn_endpoint = "/api/v1/user"

#network range
network_dev_env = ''
dev_env_start_range = ''
dev_env_end_range = ''
ignore_ips = ['', '']

#pfsense credenctials
pfsense_user = ''
pfsense_password = ''
url = ''

#vms params
macaddr = ''
vm_name = ''
ip = ''
dns = ['', '', '']
domain = "com"

#vpn
create_username = ''
create_password = ''
disable_username = ''
delete_username = ''
disabled = ''


def get_static_ip(pfsense_user, pfsense_password, url):
    
    url_static_ip = url + static_ip_endpoint

    network = network_dev_env
    start_range = ipaddress.IPv4Address(dev_env_start_range)
    end_range = ipaddress.IPv4Address(dev_env_end_range)
    available_ips = []

    response = requests.get(url_static_ip, params={'interface': 'LAN'}, auth=(pfsense_user, pfsense_password))

    if response.status_code == 200:
        data = response.json()
        static_mappings = data['data']
        
        #conjunto IPs estáticos alocados
        static_ips = set()
        for mapping in static_mappings:
            ip_address = mapping['ipaddr']
            static_ips.add(ipaddress.IPv4Address(ip_address))

        #conjunto de IPs a serem ignorados
        ignored_ips = set(ipaddress.IPv4Address(ip) for ip in ignore_ips)
        
        for ip in ipaddress.IPv4Network(network):
            if start_range <= ip <= end_range and ip not in static_ips and ip not in ignored_ips:
                available_ips.append(str(ip))
        if available_ips:
            print(available_ips=available_ips)
        else:
            print(f"Erro, lista de Ips disponíveis vazia: {response.status_code}: {response.text}")
    else:
        print(f"Erro ao buscas Ips disponíveis: {response.status_code}: {response.text}")

def post_static_ip(pfsense_user, pfsense_password, macaddr, vm_name, ip, url):
    
    url_static_ip = url + static_ip_endpoint
    
    headers = {'Content-Type': 'application/json'}

    data_static_mapping = {
    "interface": "LAN",
    "mac": macaddr,
    "cid": vm_name,
    "ipaddr": ip,
    "hostname": "",
    "descr": "",
    "filename": "",
    "rootpath": "",
    "defaultleasetime": "",
    "maxleasetime": "",
    "gateway": "",
    "domain": "",
    "domainsearchlist": "",
    "ddnsdomain": "",
    "ddnsdomainprimary": "",
    "ddnsdomainsecondary": "",
    "ddnsdomainkeyname": "",
    "ddnsdomainkeyalgorithm": "hmac-md5",
    "ddnsdomainkey": "",
    "tftp": "",
    "ldap": "",
    "nextserver": "",
    "filename32": "",
    "filename64": "",
    "filename32arm": "",
    "filename64arm": "",
    "uefihttpboot": "",
    "numberoptions": ""
    }

    # post ip
    response = requests.post(url_static_ip, json=data_static_mapping, auth=(pfsense_user, pfsense_password), headers=headers)
    if response.status_code == 200:
        sleep(5)
        print(f"Ip {ip} e MAC ADDRES: {macaddr} fixados para {vm_name}.")
    else:
        print(f"Erro ao registrar macaddr: {response.status_code}: {response.text}")

def post_dns(pfsense_user, pfsense_password, ip, dns, url):
    
    url_host_override = url + dns_endpoint

    headers = {'Content-Type': 'application/json'}
    results_dns = []

    def check_entry(host, ip):
        response = requests.get(url_host_override, auth=(pfsense_user, pfsense_password))
        if response.status_code == 200:
            data = response.json()
            for entry in data['data']:
                if entry['host'] == host:
                    if ip == entry['ip']:
                        return True  
                    else:
                        print(f"Erro, host já possui registro com outro ip. Host: {host}, ip cadastrado: {entry['ip']} e ip utilizado {ip}")
            return False
        else:
            print(f"Erro ao verificar dns: {response.status_code}: {response.text}")

    for host in dns:
        if not check_entry(host, ip):
            data_dns = {
                "aliases": [],
                "apply": True,
                "descr": "",
                "domain": dev_domain,
                "host": host,
                "ip": [ip]
                }

            response = requests.post(url_host_override, json=data_dns, auth=(pfsense_user, pfsense_password), headers=headers)
            if response.status_code == 200:
                results_dns.append(f"{host} gravada com sucesso.")
                sleep(5)
            else:
                print(f"Erro ao registrar dns: {response.status_code}: {response.text}")

    if not results_dns:
        print(f"Entradas de DNS já existentes.")
    else:
        print(f"Entradas: {results_dns}.")

def validate_macaddr(pfsense_user, pfsense_password, macaddr, url):

    url_static_ip = url + static_ip_endpoint
    
    response = requests.get(url_static_ip, params={'interface': 'LAN'}, auth=(pfsense_user, pfsense_password))

    ip_address = None

    if response.status_code == 200:
        data = response.json()
        validate_data = data['data']
        
        #encontrar macaddres e ip
        for mapping in validate_data:
            if macaddr == mapping['mac']:
                ip_address = mapping['ipaddr']
                break
        
        if ip_address:
            print(ip_address=ip_address, macaddr=macaddr)
        else:
            print(f"MAC : {macaddr} não associado com ip estáticos.")
    else:
        print(f"Erro ao buscar registro de macaddres: {response.status_code}: {response.text}")

def delete_static_ip_if_exists(pfsense_user, pfsense_password, ip, url):

    url_static_ip = url + static_ip_endpoint

    get_response = requests.get(url_static_ip, params={'interface': 'LAN'}, auth=(pfsense_user, pfsense_password))

    #mapeia id de acordo com o ip (ATENÇAO - API Pfsense reajusta os IDs, os ids devem ser descoberto de acordo com o ip)
    if get_response.status_code == 200:
        data = get_response.json()
        data_map = data['data']

        for mapping in data_map:
            if mapping['ipaddr'] == ip:
                map_id = mapping['id']
                cid = mapping['cid']
                break
        else:
            print(f"Ip: {ip} não encontrado para realizar remoção.")

        # monta /api/v1/services/dhcpd/static_mapping/?interface=LAN&id={map_id}
        delete_response = requests.delete(url_static_ip, params={'interface': 'LAN','id': map_id}, auth=(pfsense_user, pfsense_password))
        sleep(5)

        if delete_response.status_code == 200:
            print(f"Ip: {ip} correspondente a {cid} removido com sucesso.")
        else:
            print(f"Erro ao remover ip {ip}: {delete_response.status_code}: {delete_response.text}")

def delete_dns_if_exists(pfsense_user, pfsense_password, url, dns, domain):

    url_host_override = url + dns_endpoint
    deleted_dns = []

    for host in dns:
        host_response = requests.get(url_host_override, params={'host': host}, auth=(pfsense_user, pfsense_password))

        if host_response.status_code == 200:
            data = host_response.json()
            if data['data']:
                discovery_id = next(iter(data['data']))
                if data['data'][discovery_id]['domain'] == domain:
                    host_id = discovery_id

                    delete_dns_response = requests.delete(url_host_override, params={'host': host, 'id': host_id}, auth=(pfsense_user, pfsense_password))
                    sleep(5)

                    if delete_dns_response.status_code == 200:
                        deleted_dns.append(data['data'][host_id]['host'])
                    else:
                        print(f"Erro ao deletar host: {data['data'][host_id]['host']}, status: {delete_dns_response.status_code}, erro: {delete_dns_response.text}")
        else:
            print(f"Erro ao buscar dns, status: {host_response.status_code}, erro: {host_response.text}")
    #lista vazia
    if not deleted_dns:
        print(f"Nenhum DNS foi encontrado para {dns} com dominio .{domain}.")
    else:
        print(f"DNS deletados: {deleted_dns}")

def check_vpn_user_exist(user, url, pfsense_user, pfsense_password):
    url_get_user = url + vpn_endpoint

    response_get = requests.get(url_get_user, auth=(pfsense_user, pfsense_password))
    if response_get.status_code == 200:
        sleep(5)
        data = response_get.json()
        
        for entry in data['data']:
            if user == entry['name']:
                return True
        return False
    else:
        print(f"Erro ao verificar usuário: {user}, {response_get.status_code}: {response_get.text}")

def create_vpn_user(pfsense_user, pfsense_password, url, create_username, create_password):

    url_create_user = url + vpn_endpoint
    headers = {'Content-Type': 'application/json'}

    if not check_vpn_user_exist(create_username, url, pfsense_user, pfsense_password):

        data_user = {
            "authorizedkeys": "",
            "cert": [],
            "descr": "",
            "disabled": False,
            "ipsecpsk": "",
            "password": create_password,
            "priv": [],
            "username": create_username,
            }

        response = requests.post(url_create_user, json=data_user, auth=(pfsense_user, pfsense_password), headers=headers)

        if response.status_code == 200:
            sleep(5)
            print(f"Usuário {create_username} criado com sucesso.")
        else:
            print(f"Erro ao criar usuário: {response.status_code}: {response.text}")
    else:
        print(f"Usuário {create_username} já existente.")

def disable_vpn_user_if_exists(pfsense_user, pfsense_password, url, disable_username, disabled):
      
    url_disable_user = url + vpn_endpoint
    headers = {'Content-Type': 'application/json'}

    data_disable = {
    "disabled": disabled,
    "username": disable_username,
    }

    if check_vpn_user_exist(disable_username, url, pfsense_user, pfsense_password):

        response = requests.put(url_disable_user, json=data_disable, auth=(pfsense_user, pfsense_password), headers=headers)

        if response.status_code == 200:
            sleep(5)
            print(f"Usuário {disable_username} desabilitado com sucesso. {response.text}")
        else:
            print(f"Erro ao desabilitar usuário: {response.status_code}: {response.text}")
    else:
        print(f"Usuário {disable_username} não possui registro no pfsense.")   

def delete_vpn_user_if_exists(pfsense_user, pfsense_password, url, delete_username):
        
    url_delete_user = url + vpn_endpoint

    if check_vpn_user_exist(delete_username, url, pfsense_user, pfsense_password):

        # monta /api/v1/user?username={delete_username}
        response = requests.delete(url_delete_user, params={'username': delete_username}, auth=(pfsense_user, pfsense_password))

        if response.status_code == 200:
            sleep(5)
            print(f"Usuário {delete_username} deletado com sucesso. {response.text}")
        else:
            print(f"Erro ao deletar usuário: {response.status_code}: {response.text}")
    else:
        print(f"Usuário {delete_username} não possui registro no pfsense.")  

if __name__ == '__main__':
    # get_static_ip(pfsense_user, pfsense_password, url)

    # post_static_ip(pfsense_user, pfsense_password, macaddr, vm_name, ip, url)

    # post_dns(pfsense_user, pfsense_password, ip, dns, url)

    # validate_macaddr(pfsense_user, pfsense_password, macaddr, url)

    # delete_static_ip_if_exists(pfsense_user, pfsense_password, ip, url)

    # delete_dns_if_exists(pfsense_user, pfsense_password, url, dns, domain)

    # create_vpn_user(pfsense_user, pfsense_password, url, create_username, create_password)

    # disable_vpn_user_if_exists(pfsense_user, pfsense_password, url, disable_username, disabled)

    # delete_vpn_user_if_exists(pfsense_user, pfsense_password, url, delete_username)
