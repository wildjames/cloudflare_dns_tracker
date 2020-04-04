import yagmail as yag
import os


def notify(send_to, body):
    '''Handle the actual sending an email. A pre-defined bot (login details
    in email_details.json) will send an email.
    Inputs:
    -------
      send_to: str, list of str
        The email (or list of emails) to send to
      body: str
        The main text of the email
    '''
    print("I fucked up setting the new IP address. Sending an alert email")

    # Who do we send the email to?
    # Also contains email bot login
    location = __file__.split('/')[:-1] + ["email_details.json"]
    details_loc = '/'.join(location)
    if not os.path.isfile(details_loc):
        print("Couldn't find the file {}! Creating it now.")
        with open(details_loc, 'w') as f:
            s = '{\n  "user": "Bot email address",\n  "pass": "Bot email password"\n}'
            f.write(s)

    with open(details_loc, 'r') as f:
        details = json.load(f)

    send_from = details['user']
    pword = details['pass']

    if send_from == "Bot email address":
        print("Please set up the bot email in {} to enable email reporting!".format(details_loc))
        return

    subject = "ERROR IN UPDATING CLOUDFLARE CREDENTIALS"

    # Construct the email contents
    contents = [body]

    # Send with yagmail
    client = yag.SMTP(send_from, pword)
    client.send(send_to, subject, contents)
    print("Email sent!")

    return
