from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
import io
import base64

# Créer les données pour les graphiques
vulnerabilities = ['LFI', 'XSS', 'SQLi']
counts = [10, 15, 5]

# Générer un graphique
fig, ax = plt.subplots()
ax.bar(vulnerabilities, counts)
ax.set_title('Répartition des vulnérabilités')

# Sauvegarder le graphique dans une image base64
img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)
graph_url = base64.b64encode(img.getvalue()).decode('utf8')
graph_vulnerabilities = 'data:image/png;base64,{}'.format(graph_url)

# Exemple de requêtes HTTP
http_requests = """
GET /bWAPP/portal.php HTTP/1.1
Host: 10.161.11.142
...
"""

# Charger le modèle HTML
env = Environment(loader=FileSystemLoader('/home/kali/Desktop/Projets/examen'))
template = env.get_template('rapport.html')

# Rendre le modèle avec les données
html_content = template.render(graph_vulnerabilities=graph_vulnerabilities, http_requests=http_requests)

# Sauvegarder le rapport final dans un fichier HTML
with open('rapport_final.html', 'w') as f:
    f.write(html_content)
