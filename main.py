from pprint import pformat

import yagmail as yag
import requests
import os
from time import sleep

from logging import getLogger
logger = getLogger(__name__)

whatismyip_url = "https://api.ipify.org?format=json"
sleep_time = 60 * 60 * 1 # seconds

cloudflare_zone = os.environ.get('CLOUDFLARE_ZONE')
cloudflare_domain_id = os.environ.get('CLOUDFLARE_DOMAIN_ID')
gmail_user = os.environ.get('GMAIL_USER')
gmail_pass = os.environ.get('GMAIL_PASS')
gmail_send_to = os.environ.get('GMAIL_SEND_TO')


def notify( body):
    '''Handle the actual sending an email. A pre-defined bot (login details
    in email_details.json) will send an email.
    Inputs:
    -------
      body: str
        The main text of the email
    '''
    logger.info("I fucked up setting the new IP address. Sending an alert email")

    subject = "ERROR IN UPDATING CLOUDFLARE CREDENTIALS"

    # Construct the email contents
    contents = [body]

    try:
        # Send with yagmail
        client = yag.SMTP(gmail_user, gmail_pass)
        client.send(gmail_send_to, subject, contents)
        logger.info("Email sent!")
    except:
        logger.info("Failed to send email! Are your credentials set?")

    return

def main():
    response = requests.get(whatismyip_url)
    payload = response.json()
    my_IP = payload['ip']

    logger.info("My IP is {}\n\n".format(my_IP))

    # Documentation: https://api.cloudflare.com/
    cloudflare_endpoint = "https://api.cloudflare.com/client/v4"
    # I promise I'm me, guv
    headers = {
        "Authorization": "Bearer {}".format(cloudflare_zone),
        "Content-Type": "application/json",
    }


    # Test communicating with the server
    verify_endpoint = cloudflare_endpoint + "/user/tokens/verify"
    response = requests.get(verify_endpoint, headers=headers)
    logger.info("GETting with these headers:")
    logger.info(pformat(headers))
    logger.info("Recieved this response:")
    logger.info(pformat(response))
    logger.info(pformat(response.json()))

    payload = response.json()
    if payload['success']:
        logger.info("\nSuccess!\n\n")
    else:
        logger.info("Verification FAILED!!")
        exit()


    # This is the zone I'm gonna target:
    zone_endpoint = cloudflare_endpoint + "/zones/{}".format(cloudflare_domain_id)

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
    logger.info("DNS Records:")
    try:
        records = payload['result']
    except KeyError:
        logger.info("Payload doesn't have the result key! Here's a dump:")
        logger.info(pformat(payload))
    for record in records:
        logger.info("Record:")
        logger.info("    ID:       {}".format(record['id']))
        logger.info("    Name:     {}".format(record['name']))
        logger.info("    Type:     {}".format(record['type']))
        logger.info("    Content:  {}".format(record['content']))
        logger.info("    Proxied?  {}".format(record['proxied']))
        logger.info("\n")

        if record['type'] in types_to_update:
            logger.info("--> I need to alter this record to point to {}".format(my_IP))
            update_dns_endpoint = dns_endpoint + "/{}".format(record['id'])
            logger.info(pformat(update_dns_endpoint))

            package = {
                "type": record['type'],
                "name": record['name'],
                "content": my_IP,
                "ttl": 1,
                "proxied": record['proxied']
            }
            logger.info("\nData is now:")
            logger.info(pformat(package))

            # PUT the data
            put_resp = requests.put(
                update_dns_endpoint,
                json=package,
                headers=headers,
            )

            logger.info("\nResponses:")
            logger.info(pformat(put_resp))
            put_payload = put_resp.json()
            logger.info(pformat(put_payload))
            if not put_payload['success']:
                logger.info("Failed to update the record!!! I'll send an email.")

                body = pformat(put_payload)

                notify(body)

        logger.info("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")


if __name__ == "__main__":
    while True:
        main()
        logger.info("Sleeping for {} hour(s)...".format(sleep_time / 60 / 60))
        sleep(sleep_time)