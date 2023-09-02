# Cloudflare DNS Tracker

This utility updates the DNS records of a Cloudflare website programmatically to handle dynamic IPs. It's designed to work with Cloudflare's v4 REST API. The script performs a PUT request to update the DNS record with the IP address of the machine running the script.

## Prerequisites

### Credentials Setup

You need to create two JSON files for storing credentials:

1. **`credentials.json`**: Contains Cloudflare information.
    - `zone`: Your Cloudflare API Token.
    - `domainID`: The domain you wish to update.

2. **`email_credentials.json`**: Contains Gmail account information for sending notifications.
    - `user`: Email address to send from.
    - `pass`: Password for the email account.
    - `send_to`: Recipient email address for notifications.

## Docker Deployment

This utility is containerized for easy deployment on an unRAID server. To build and run the Docker container, execute the following commands:

```bash
docker build --tag cloudflare_ddns .
docker run cloudflare_ddns
```

The Docker container is configured to run the update script every hour.

---

## Notes to Future Self

Dear Future James,

I know you might forget how this works, so here's a quick refresher:

- The `Authorization` token in the `credentials.json` (labeled as `Bearer: {}`) is your Cloudflare API Token. You can find this in your [Cloudflare profile under the API section](https://dash.cloudflare.com/profile).
  
- The `domainID` is the ID of the website you want to manage. You can find this on the domain management page of your Cloudflare dashboard. Look for it on the right side, about halfway down the page.

- The script iterates through all DNS records associated with the domain, updating those that need it based on their type. If you ever need to change this behavior, it should be straightforward to modify the script to update records based on other criteria like name.

Best wishes,

Past James
