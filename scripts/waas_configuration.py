import requests
import json
import sys
import logging
import argparse
import getpass

logging.basicConfig(level = logging.DEBUG, filename = 'output.log')

'''
parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="Email address to login to Barracuda WaaS")
parser.add_argument("-f", "--filename", help="Input file containing the list of ip addresses")
parser.add_argument("-a", "--action", help="Whether to allow or block the ip addresses. Defaults to 'allow'. Allowed values are 'allow' or 'block'")
parser.add_argument("-s", "--service_app_name", help="Service name into which configuration needs to be updates")
password=getpass.getpass()

args = parser.parse_args()
'''

username = "aravindan.acct@gmail.com"
password = "Gartner_demo123!"

def waas_login():
    base_url = "https://api.waas.barracudanetworks.com/v2/waasapi/"
    login_req_url = base_url + "api_login/"
    data = {"email": username, "password": password}
    login_req = requests.post(login_req_url, data=data)

    login_response = login_req.json()
    token = login_response['key']
    headers = {"Content-Type": "application/json", "auth-api": f'{token}'}
    login_info = {"base_url": base_url, "headers": headers}
    return login_info

login_info = waas_login()

print(login_info)

environment = ["production","staging"]

# Create Service

create_svc_url = login_info["base_url"]+"applications/"

with open("/home/vsts/svc_ip","r") as f:
    svr_ip = f.read()

print(svr_ip)

for env in range(len(environment)):
    payload = {
    "applicationName": "juiceshopv1-"+environment[env],
    "backendPort": 3000,
    "useHttp": "true",
    "useExistingIp": "true",
    "backendIp": json.loads(svr_ip["ip"]),
    "maliciousTraffic": "Passive",
    "serviceIp": "2.2.2.2",
    "httpsServicePort": "443",
    "redirectHTTP": "true",
    "useHttps": "true",
    "httpServicePort": 3000,
    "backendType": "HTTP",
    "serviceType": "HTTP",
    "account_ips": {},
    "hostnames": [
        {
        "hostname": environment[env]+".juiceshopv1.cudatech.info"
        }
    ]
    }
    print("Creating WAAS Configuration for the " + environment[env] + " environment")
    check_svc_exists = requests.get(create_svc_url, headers=login_info["headers"])
    print(check_svc_exists.text)
    print(json.dumps(payload))
    create_svc_response = requests.post(create_svc_url, headers=login_info["headers"], data=json.dumps(payload)) 
    print(create_svc_response.text)
print("For GUI access visit: https://waas.barracudanetworks.com")