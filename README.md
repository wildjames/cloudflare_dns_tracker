# Cloudflare DNS Tracker

This utility updates the DNS records of a Cloudflare website programmatically to handle dynamic IPs. It's designed to work with Cloudflare's v4 REST API. The script performs a PUT request to update the DNS record with the IP address of the machine running the script.

## Prerequisites

### Environment Variables for Credentials

Instead of using JSON files, this Dockerized utility uses environment variables to securely pass credentials. The following environment variables are required:

- `CLOUDFLARE_ZONE`: Your Cloudflare API Token.
- `CLOUDFLARE_DOMAIN_ID`: The domain you wish to update.
- `GMAIL_USER`: Email address to send from.
- `GMAIL_PASS`: Password for the email account.
- `GMAIL_SEND_TO`: Recipient email address for notifications.

## Docker Deployment

This utility is containerized for easy deployment. To build and run the Docker container, execute the following commands:

```bash
docker build --tag cloudflare_ddns .
docker run /
    -e CLOUDFLARE_ZONE='your_zone' /
    -e CLOUDFLARE_DOMAIN_ID='your_domain_id'/
    -e GMAIL_USER='your_email' /
    -e GMAIL_PASS='your_pass' /
    -e GMAIL_SEND_TO='recipient_email' /
    cloudflare_ddns
```

The Docker container is configured to run the update script every hour.

## Notes to Future Self

Dear Future Me,

I know you might forget how this works, so here's a quick refresher:

- The `CLOUDFLARE_ZONE` environment variable corresponds to your Cloudflare API Token. You can find this in your [Cloudflare profile under the API section](https://dash.cloudflare.com/profile).

- The `CLOUDFLARE_DOMAIN_ID` is the ID of the website you want to manage. You can find this on the domain management page of your Cloudflare dashboard. Look for it on the right side, about halfway down the page.

- The script iterates through all DNS records associated with the domain, updating those that need it based on their type. If you ever need to change this behavior, it should be straightforward to modify the script to update records based on other criteria like name.

Best wishes,

Past Me
