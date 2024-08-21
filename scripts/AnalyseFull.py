import requests
from bs4 import BeautifulSoup
import nmap
import itertools
from urllib.parse import urljoin

# Configuration de Nmap pour scanner les ports de l'application
def scan_ports(host):
    nm = nmap.PortScanner()
    scan_result = nm.scan(host, arguments='-Pn')  # '-Pn' pour désactiver le ping
    report = []
    for host in scan_result['scan']:
        report.append(f"\nHost : {host}")
        for proto in scan_result['scan'][host].all_protocols():
            ports = scan_result['scan'][host][proto].keys()
            for port in ports:
                state = scan_result['scan'][host][proto][port]['state']
                name = scan_result['scan'][host][proto][port]['name']
                report.append(f"Port : {port}, State : {state}, Service : {name}")
    return report

# Extraction des formulaires pour effectuer du fuzzing
def extract_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')
    return forms

# Analyse de la réponse pour détecter des vulnérabilités potentielles
def analyze_response(response):
    indicators = {
        'SQL Injection': ['syntax error', 'unclosed quotation mark', 'SQL'],
        'XSS': ['<script>', 'alert(', 'onerror='],
        'LFI': ['etc/passwd', 'root:x:', 'No such file or directory']
    }

    vulnerabilities = []
    for vuln_type, patterns in indicators.items():
        for pattern in patterns:
            if pattern.lower() in response.text.lower():
                vulnerabilities.append(vuln_type)
                break
    return vulnerabilities

# Fuzzing basique sur les formulaires
def fuzz_forms(url, forms, fuzz_data):
    fuzz_report = []
    for i, form in enumerate(forms, start=1):
        action = form.get('action')
        method = form.get('method', 'GET').upper()
        action_url = urljoin(url, action)

        fuzz_report.append(f"\nFuzzing Form {i}:")
        for combo in fuzz_data:
            data = {}
            for input_tag in form.find_all('input'):
                input_name = input_tag.get('name')
                if input_name:
                    data[input_name] = combo

            if method == "POST":
                response = requests.post(action_url, data=data)
            else:
                response = requests.get(action_url, params=data)
            
            fuzz_report.append(f"Test avec : {data}")
            fuzz_report.append(f"Code réponse : {response.status_code}")
            vulnerabilities = analyze_response(response)
            if vulnerabilities:
                fuzz_report.append(f"Vulnérabilités détectées : {', '.join(vulnerabilities)}")
            else:
                fuzz_report.append("Aucune vulnérabilité détectée.")
    return fuzz_report

def generate_fuzz_data():
    # Génération simple de données pour le fuzzing
    fuzz_data = ['<script>alert(1)</script>', "' OR '1'='1", '" OR "1"="1', '../../../etc/passwd']
    return list(itertools.permutations(fuzz_data, 2))  # Combinaisons possibles de 2 éléments

def save_report(report, filename):
    with open(filename, 'w') as file:
        for line in report:
            file.write(line + '\n')

def scan_website(url):
    report = []

    # Analyse des ports pour détecter les services potentiellement vulnérables
    host = url.replace('http://', '').replace('https://', '').split('/')[0]
    report.append("\n--- Scan des ports ---")
    port_report = scan_ports(host)
    report.extend(port_report)

    # Extraction des formulaires et fuzzing
    report.append("\n--- Fuzzing des formulaires ---")
    forms = extract_forms(url)
    fuzz_data = generate_fuzz_data()
    fuzz_report = fuzz_forms(url, forms, fuzz_data)
    report.extend(fuzz_report)

    # Sauvegarde du rapport
    report_filename = "vulnerability_report.txt"
    save_report(report, report_filename)
    print(f"Rapport sauvegardé dans : {report_filename}")

if __name__ == "__main__":
    url = input("Entrez l'URL de l'application : ")
    scan_website(url)
