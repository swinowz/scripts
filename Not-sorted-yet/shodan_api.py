import shodan

SHODAN_API_KEY = ''
api = shodan.Shodan(SHODAN_API_KEY)

def search_minecraft_servers():
    try:
        query = 'net:82.0.0.0/8 port:25565 version:1.21.1'
        results = api.search(query)
        for result in results['matches']:
            ip = result['ip_str']
            if ip.endswith('.21'):
                print(f"Serveur Minecraft trouvé: {ip}")
                print(f"Données: {result}\n")

    except shodan.APIError as e:
        print(f"Erreur API Shodan: {e}")

search_minecraft_servers()