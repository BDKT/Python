import requests
from bs4 import BeautifulSoup, Comment

def afficher_code_source(soup):
    print(soup.prettify())

def afficher_formulaires(soup):
    print("\nFormulaires trouvés sur la page:")
    for form in soup.find_all('form'):
        print(form)

def afficher_pages_authentification(soup):
    print("\nPages d'authentification possibles:")
    forms = soup.find_all('form')
    for form in forms:
        if 'password' in str(form).lower():
            print(form)

def extraire_commentaires_html(soup):
    print("\nCommentaires HTML trouvés sur la page:")
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        print("Comment found:", comment)

def extraire_scripts_javascript(soup):
    print("\nScripts JavaScript trouvés sur la page:")
    for script in soup.find_all('script'):
        print(script)

def extraire_meta_informations(soup):
    print("\nMéta-informations trouvées sur la page:")
    for meta in soup.find_all('meta'):
        print(meta)

def afficher_liens(soup):
    print("\nLiens trouvés sur la page:")
    for link in soup.find_all('a', href=True):
        print(link['href'])

def afficher_images(soup):
    print("\nImages trouvées sur la page:")
    for img in soup.find_all('img'):
        print(img['src'])

def afficher_balises_specifiques(soup):
    tag = input("Entrez le nom de la balise à rechercher: ")
    print(f"\nBalises <{tag}> trouvées sur la page:")
    for element in soup.find_all(tag):
        print(element)

def rechercher_mots_cles(soup):
    keywords = input("Entrez les mots-clés à rechercher (séparés par des virgules): ").split(',')
    keywords = [keyword.strip() for keyword in keywords]
    
    print("\nRecherche de mots-clés dans le texte visible...")
    for keyword in keywords:
        results = soup.find_all(string=lambda text: keyword.lower() in text.lower())
        if results:
            print(f"\nOccurrences de '{keyword}':")
            for result in results:
                print(result.strip())
        else:
            print(f"Aucune occurrence de '{keyword}' trouvée dans le texte visible.")
    
    print("\nRecherche de mots-clés dans les commentaires...")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for keyword in keywords:
        results = [comment for comment in comments if keyword.lower() in comment.lower()]
        if results:
            print(f"\nOccurrences de '{keyword}' dans les commentaires:")
            for comment in results:
                print(comment.strip())
        else:
            print(f"Aucune occurrence de '{keyword}' trouvée dans les commentaires.")

def afficher_options():
    print("\nOptions disponibles :")
    print("1. Afficher le code source complet")
    print("2. Afficher les formulaires")
    print("3. Afficher les pages d'authentification")
    print("4. Extraire les commentaires HTML")
    print("5. Extraire les scripts JavaScript")
    print("6. Extraire les méta-informations")
    print("7. Afficher les liens")
    print("8. Afficher les images")
    print("9. Afficher des balises spécifiques")
    print("10. Rechercher des mots-clés")
    print("0. Quitter")

def main():
    url = input("Entrez l'URL de la page à analyser: ")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    afficher_code_source(soup)

    while True:
        afficher_options()
        choix = input("\nChoisissez une option (0 pour quitter) : ")
        
        if choix == '1':
            afficher_code_source(soup)
        elif choix == '2':
            afficher_formulaires(soup)
        elif choix == '3':
            afficher_pages_authentification(soup)
        elif choix == '4':
            extraire_commentaires_html(soup)
        elif choix == '5':
            extraire_scripts_javascript(soup)
        elif choix == '6':
            extraire_meta_informations(soup)
        elif choix == '7':
            afficher_liens(soup)
        elif choix == '8':
            afficher_images(soup)
        elif choix == '9':
            afficher_balises_specifiques(soup)
        elif choix == '10':
            rechercher_mots_cles(soup)
        elif choix == '0':
            print("Au revoir!")
            break
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
