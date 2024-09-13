import base64
import urllib.parse
import re


def remove_signature_response(decoded_response):
    signature_value_pattern = re.compile(r'<ds:SignatureValue>(.*?)</ds:SignatureValue>', re.DOTALL)
    modified_response = re.sub(signature_value_pattern, '<ds:SignatureValue></ds:SignatureValue>', decoded_response)
    encoded_response = base64.b64encode(modified_response.encode('utf-8')).decode('utf-8')
    print("Result copied to your clipboard")
    return encoded_response