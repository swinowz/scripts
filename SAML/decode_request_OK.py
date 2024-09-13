import base64
import urllib.parse
import zlib
import io
from lxml import etree


def decode_saml_request():
    saml_request = input("Enter the encoded SAML request: ")
    decoded_request = urllib.parse.unquote(saml_request)
    xml = zlib.decompress(base64.b64decode(decoded_request), -15).decode('utf-8')
    buf = io.BytesIO(xml.encode('utf-8'))
    doc = etree.parse(buf)
    print("Result copied to your clipboard")
    return etree.tostring(doc.getroot(), pretty_print=True).decode('utf-8')