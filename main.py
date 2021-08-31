import json
from pprint import pformat, pprint

import requests
from notify import notify

whatismyip_url = "https://api.ipify.org?format=json"

response = requests.get(whatismyip_url)
payload = response.json()
my_IP = payload['ip']

print("My IP is {}\n\n".format(my_IP))


# This is where I store my SENSITIVE PARTS
cred_file = open("credentials.json", 'r')
cred = json.load(cred_file)
cred_file.close()


# Documentation: https://api.cloudflare.com/
cloudflare_endpoint = "https://api.cloudflare.com/client/v4"
# I promise I'm me, guv
headers = {
    "Authorization": "Bearer {}".format(cred['zone']),
    "Content-Type": "application/json",
}


# Test communicating with the server
verify_endpoint = cloudflare_endpoint + "/user/tokens/verify"
response = requests.get(verify_endpoint, headers=headers)
print("GETting with these headers:")
pprint(headers)
print("Recieved this response:")
pprint(response)
pprint(response.json())

payload = response.json()
if payload['success']:
    print("\nSuccess!\n\n")
else:
    print("Verification FAILED!!")
    exit()


# This is the zone I'm gonna target:
zone_endpoint = cloudflare_endpoint + "/zones/{}".format(cred['domainID'])

# Lets see what we have to work with here...
dns_endpoint = zone_endpoint + "/dns_records"

resp = requests.get(dns_endpoint, headers=headers)
payload = resp.json()

# I only actually want to update the IP for  certain record types.
# This is a list of those types:
types_to_update = ['A']

# To update a zone:
#   PUT zones/:zone_identifier/dns_records/:identifier
update_dns_endpoint = dns_endpoint + "/{}"

# Humans are bad at reading raw data. Make it nice for the poor things.
print("DNS Records:")
try:
    records = payload['result']
except KeyError:
    print("Payload doesn't have the result key! Here's a dump:")
    print(payload)
for record in records:
    print("Record:")
    print("    ID:       {}".format(record['id']))
    print("    Name:     {}".format(record['name']))
    print("    Type:     {}".format(record['type']))
    print("    Content:  {}".format(record['content']))
    print("    Proxied?  {}".format(record['proxied']))
    print("\n")

    if record['type'] in types_to_update:
        print("--> I need to alter this record to point to {}".format(my_IP))
        update_dns_endpoint = dns_endpoint + "/{}".format(record['id'])
        print(update_dns_endpoint)

        package = {
            "type": record['type'],
            "name": record['name'],
            "content": my_IP,
            "ttl": 1,
            "proxied": record['proxied']
        }
        print("\nData is now:")
        pprint(package)

        # PUT the data
        put_resp = requests.put(
            update_dns_endpoint,
            json=package,
            headers=headers,
        )

        print("\nResponses:")
        print(put_resp)
        put_payload = put_resp.json()
        pprint(put_payload)
        if not put_payload['success']:
            print("Failed to update the record!!! I'll send an email.")

            body = pformat(put_payload)

            notify(send_to, body)

    print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
