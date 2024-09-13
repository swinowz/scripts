import base64
import urllib.parse

def decode_saml_response():
    saml_response = input("Enter the encoded SAML response: ")
    url_decoded_txt = urllib.parse.unquote(saml_response)
    decoded_txt = base64.b64decode(url_decoded_txt, validate=True).decode('utf-8')
    return decoded_txt