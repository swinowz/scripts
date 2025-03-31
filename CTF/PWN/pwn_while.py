import socket
import time

def reverse_string(s):
    return s[::-1]

def main():
    # Créer une connexion TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecter le socket à l'adresse du serveur
    server_address = ('localhost', 4000)
    sock.connect(server_address)

    try:
        while True:
            time.sleep(1)
            # Recevoir des données du serveur
            data = sock.recv(1024)
            print(f"Reçu : {data.decode()}")

            # Diviser le message en lignes
            lines = data.decode().split('\n')
            
            if 'Congratulations!! Here is your flag:' in lines:
                break

            for line in lines:
                # Vérifier si la ligne est une chaîne à inverser
                if line.startswith('>>>'):
                    # Supprimer les '>>>' et les espaces blancs au début de la chaîne
                    line = line.lstrip('>>> ').rstrip()

                    # Inverser la chaîne de caractères
                    response = reverse_string(line)
                    print(f"Envoi : {response}")

                    # Ajouter un caractère de fin de ligne à la réponse
                    response += '\n'

                    # Renvoyer la chaîne inversée au serveur
                    sock.sendall(response.encode())

    finally:
        # Fermer la connexion
        sock.close()

if __name__ == "__main__":
    main()
