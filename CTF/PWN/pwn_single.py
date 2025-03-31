import socket
import math

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('147.182.245.126', 33001))

data = sock.recv(1024).decode()
lines = data.splitlines()

for line in lines:
    print(f"Reçu : {line}")
    number = line.lstrip('Calculate the factorial of ').rstrip('.')
    print(f"Nombre : {number}")
    facto = math.factorial(int(number))
    print(f"Envoi : {facto}")
    response = str(facto)
    sock.sendall(response.encode())
    break

while True:  # pour recup le flag
    data = sock.recv(1024).decode()
    if not data:
        break
    print(f"Flag : {data}")

sock.close()