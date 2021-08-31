# cloudflare_dns_tracker
Update the DNS records of a cloudflare website programmatically, for dynamic IPs. 
I looked about and the tools that exist don't seem to work for my use-case, which bummed me out. This was written for the v4 cloudflare REST API.

This is basic stuff, really (though the [cloudflare API](https://api.cloudflare.com) documentation was an arse to understand, IMO).
Literally just takes a DNS record, and does a PUT request to update it with the IP address of the computer running this script. 
But, I figure that I'll want this again and I don't want to have to ssh into my server every damn time, so here it is.

## DON'T FORGET TO SET UP THE CREDENTIALS

you need two credentials files, stored as JSON.
  - `credentials.json`: Cloudflare info
    - `zone`: API Token
    - `domainID`: The domain to update
  - `email_credentials.json`: gmail account info (will send you an email if updating the records fails)
    - `user`: email address to send from
    - `pass`: password
    - `send_to`: Who to notify

## A letter from you

Dear Future James,

I know you're an idiot, and you're gonna forget how this script works. 
One day it will break, and you're gonna have to learn this all again. Neither of us want that.

Here are some things that you used to know:
  - Authorisation token (this is the bit that says `Bearer: {}`, and is `zone` in the JSON file) is the relevant API *token* from [the API subsection here](https://dash.cloudflare.com/profile)
  - The bit of the URL that has `/zones/{}` (AKA domainID) wants the ID key of the relevant website - you can find that on the domain management page on your cloudflare website. At time of writing, it's on the right, about halfway down.
  - In the `/dns_records/{}`, you're putting the ID for the specific *record* you want to edit. The API can report the IDs of all the records associated with the domain, so I loop through them all, checking if they want updating based on their type. This probably wont need changing, but would be trivial to alter and have it change records based on name or whatever.

Love,

Past James 

(xoxox)
