import json

# On recherche tout les comptes ayant un UserAccountControl spécifique, donc pour commencer on les récup tous
with open('ldap.json') as file:
    data = json.load(file)

def search_user_account_control(data, table):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "userAccountControl":
                table.append((value, data.get('sAMAccountName', 'N/A')))
            elif isinstance(value, (dict, list)):
                search_user_account_control(value, table)
    elif isinstance(data, list):
        for item in data:
            search_user_account_control(item, table)

table = []
search_user_account_control(data, table)
remove_dupe = list(set(table))

#On cherche pour les flag UAC spécifique : 
# UAC --> convertir en binaire
# DONT_REQ_PREAUTH (4194304) --> Convertir en binaire
# Faire un ET sur chaque bit ( opérateur : '&') entre les deux valeurs 
# Si le résultat est égale à la valeur de DONT_REQ_PREAUTH alors on affiche le compte 
for value, sam_account_name in remove_dupe:
    if (value & 4194304) == 4194304:
        print(f"Test pour : {value}")
        print(f"Compte trouvé : {sam_account_name}")
    else:
        continue