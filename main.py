import requests
from bs4 import BeautifulSoup
import json

# URL cible
url = 'https://fr.glosbe.com/mg/fr/tiako%20ianao'

# Requête HTTP pour obtenir le contenu de la page
response = requests.get(url)
if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Dictionnaire pour stocker les résultats
    results = {
        "translations": [],
        "examples": [],
        "context_translations": []
    }

    # Extraire la traduction principale (je t'aime)
    translation_elem = soup.find('p', {'class': 'text-xs text-gray-600 line-clamp-2', 'id': 'content-summary'})
    if translation_elem:
        translation_text = translation_elem.get_text(strip=True)
        results["translations"].append(translation_text)

    # Extraire les exemples de phrases
    examples = soup.select('div.translation__example')
    if examples:
        for example in examples:
            malagasy_elem = example.select_one('p[lang="mg"]')
            french_elem = example.select_one('p:not([lang="mg"])')
            
            malagasy = malagasy_elem.get_text(strip=True) if malagasy_elem else None
            french = french_elem.get_text(strip=True) if french_elem else None

            if malagasy and french:
                results["examples"].append({
                    "malagasy": malagasy,
                    "french": french
                })

    # Extraire les traductions en contexte
    context_section = soup.find_all('div', class_='border-gray-300')
    if context_section:
        for context in context_section:
            context_text = context.get_text(strip=True)
            if context_text:
                results["context_translations"].append(context_text)

    # Afficher les résultats en JSON
    print(json.dumps(results, ensure_ascii=False, indent=4))
else:
    print(f"Erreur lors de la requête : {response.status_code}")
