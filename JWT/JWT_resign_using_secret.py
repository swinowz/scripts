import hmac
import hashlib
import base64

header = ''
payload = ''
secret = ''

message = f'{header}.{payload}'
signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip('=')

token = f'{header}.{payload}.{signature_encoded}'
print(token)
