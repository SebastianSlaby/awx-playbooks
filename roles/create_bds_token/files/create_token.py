#!/usr/bin/python
import urllib3
from getpass import getpass
import json


token=getpass("Token: ")
token = "Br5r9d8Fu6UotyJTPh490YmuL5iDqA"
urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE')

print("Enter tower url, for example: https://ansible-tower.ocp3.sr1.eu1.sp.ibm.local ")
tower_url = input("URL: ")

# Get list of organizations
r = http.request('GET', '{}/api/v2/organizations/?page_size=500'.format(tower_url), headers={"Authorization": "Bearer {}".format(token)})
orgs = json.loads(r.data.decode('utf-8'))


#Find credential type ID
r_cred_type = http.request('GET', '{}/api/v2/credential_types/?name=BDS%20Master%20Access%20Tokens'.format(tower_url), headers={"Authorization": "Bearer {}".format(token)})
cred_tmp  = json.loads(r_cred_type.data.decode('utf-8'))
cred_type_id = cred_tmp["results"][0]["id"]

# org['name'] is tricode
# cred name: <org>_cred_bds_master_tokens

for org in orgs["results"]:
    tricode = org["name"]
    org_id = org["id"]
    cred_name = "{}_cred_bds_master_tokens".format(tricode)
    data = {
        "name": cred_name,
        "organization": org_id,
        "credential_type": cred_type_id,
        "inputs": {
            "bds_repo_user_ag": "placeholder",
            "bds_repo_user_ap": "placeholder",
            "bds_repo_user_eu": "placeholder",
            "bds_repo_user_password_ag": "placeholder",
            "bds_repo_user_password_ap": "placeholder",
            "bds_repo_user_password_eu": "placeholder"
        }
        }
    encoded_data = json.dumps(data).encode('utf-8')
    t = http.request('POST', '{}/api/v2/organizations/{}/credentials/'.format(tower_url, org_id),
                 body=encoded_data,
                 headers={"Authorization": "Bearer {}".format(token), 'Content-Type': 'application/json'})
