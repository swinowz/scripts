#!/usr/bin/env python3
from pwn import *
import sys

# Utilisation des arguments en ligne de commande
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} host port")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

# Connexion au serveur distant
io = remote(HOST, PORT)

# Synchronisation avec le début
io.recvuntil(b">>> ")
io.sendline(b"Go!")

# On ignore deux lignes d'instructions
io.recvlines(2)

# Extraction de la valeur à ajouter (val)
val = int(io.recvline().strip().decode()[32:-41])

# Lecture du nombre donné par le serveur
io.recvuntil(b"Here is a number: ")
x = int(io.recvline().strip())

log.success(f"{x = }")

# Ajout de val et envoi du résultat
x = str(x + val).encode()
io.sendlineafter(b">>> ", x)

# Récupération du flag
io.recvline()
flag = io.recvline().strip().decode()
io.close()

print(flag)
