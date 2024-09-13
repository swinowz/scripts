
import base64
import urllib.parse

def replace_content_saml():
    user_choice = input("Enter the encoded string : ")
    url_decoded_txt = urllib.parse.unquote(user_choice)
    decoded_txt = base64.b64decode(url_decoded_txt, validate=True).decode('utf-8')
    res = decoded_txt.replace("useruser", "admin")
    reencoded_txt = base64.b64encode(res.encode('utf-8')).decode('utf-8')
    url_encoded_txt = urllib.parse.quote(reencoded_txt)
    return url_encoded_txt
