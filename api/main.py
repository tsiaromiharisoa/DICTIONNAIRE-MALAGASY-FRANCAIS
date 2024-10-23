from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def scrape_definitions(alpha, page):
    # Construire l'URL
    url = f"http://dico.malgache.free.fr/franc_malg.php3?alpha={alpha}&first={page}"
    
    # Envoyer la requête GET
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Analyser le contenu HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver toutes les définitions dans le tableau
        definitions = []
        for row in soup.find_all('tr'):
            # Chaque définition est dans une cellule <td>
            cells = row.find_all('td')
            if cells:
                # Extraire le texte et nettoyer
                definition = cells[0].get_text(strip=True)
                definitions.append(definition)
        
        # Formater les résultats en JSON
        return json.dumps(definitions, ensure_ascii=False, indent=4)
    else:
        return None

@app.route('/recherche', methods=['GET'])
def recherche():
    dictionnaire = request.args.get('dictionnaire', default='A', type=str)
    page = request.args.get('page', default=0, type=int)
    
    # Appel de la fonction de scraping
    result = scrape_definitions(dictionnaire, page)
    
    if result:
        return jsonify({"definitions": json.loads(result)})
    else:
        return jsonify({"error": "Erreur lors de la récupération des données."}), 500

@app.route('/recherche/query', methods=['GET'])
def recherche_query():
    query = request.args.get('query', type=str)
    
    if not query:
        return jsonify({"error": "Aucune requête fournie."}), 400

    # Scraping pour récupérer les définitions
    all_definitions = []
    for page in range(0, 100, 25):  # Ajustez la plage si nécessaire
        result = scrape_definitions(query[0], page)  # Utiliser la première lettre pour l'alpha
        if result:
            all_definitions.extend(json.loads(result))
    
    # Filtrer les définitions en fonction de la requête
    filtered_definitions = [definition for definition in all_definitions if query in definition]
    
    return jsonify({"results": filtered_definitions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                
