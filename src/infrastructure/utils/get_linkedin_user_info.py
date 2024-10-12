import os
import requests

# Récupérer le token d'accès depuis la variable d'environnement
access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')

# Vérifier si le token d'accès a été récupéré
if not access_token:
    print("Erreur : Le token d'accès LinkedIn n'est pas défini dans les variables d'environnement.")
    exit(1)

# URL de l'API LinkedIn pour obtenir les informations utilisateur
url = 'https://api.linkedin.com/v2/userinfo'

# En-têtes de la requête
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Effectuer la requête GET
response = requests.get(url, headers=headers)

# Vérifier le statut de la réponse
if response.status_code == 200:
    # La requête a réussi, afficher les informations utilisateur
    user_info = response.json()
    print("Informations utilisateur :")
    print(user_info)
else:
    # La requête a échoué, afficher le message d'erreur
    print(f"Erreur {response.status_code}: {response.text}")
