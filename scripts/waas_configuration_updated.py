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
    svr_ip_str = f.read()
    svr_ip = json.loads(svr_ip_str)
print("Backend server ip: \n")
print(json.loads(svr_ip_str))
print(svr_ip["ip"])

existing_svc = []
check_svc_exists = requests.get(create_svc_url, headers=login_info["headers"])
svc_data = json.loads(check_svc_exists.text)
for svc in range(len(svc_data["results"])):
    svc_name = svc_data["results"][svc]["name"]
    existing_svc.append(svc_name)
print(existing_svc)

for env in range(len(environment)):
    app_name = "juiceshopv1-"+environment[env]
    if app_name in existing_svc:
        print(app_name + " service exists")
    else:
        payload = {
        "applicationName": app_name,
        "backendPort": 3000,
        "useHttp": "true",
        "useExistingIp": "true",
        "backendIp": svr_ip["ip"],
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
        print(json.dumps(payload))
        create_svc_response = requests.post(create_svc_url, headers=login_info["headers"], data=json.dumps(payload)) 
        print(create_svc_response.text)
print("For GUI access visit: https://waas.barracudanetworks.com")

