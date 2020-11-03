import argparse
import csv
from pprint import pprint
import requests


"""
Esse script acessa a API do TSE e exporta um CSV com os links
das propostas feitas por candidatos a prefeito.

Pré-requisitos:
Instale o `requests` e baixe o arquivo de municípios do Brasil
em https://basedosdados.org/dataset/br-basedosdados-diretorios-brasil#

Coloque o arquivo baixado na mesma pasta que esse script.
Execute `python mayor_proposals.py` para exportar um CSV com os
links para as propostas.

Caso queira fazer download dos arquivos PDF, execute:
`python mayor_proposals.py --download-proposals`
"""

BASE_ENDPOINT = "http://divulgacandcontas.tse.jus.br/divulga/rest/v1"
ELECTION_CODE = "2030402020"

def get_positions_from(city):
    endpoint = f"{BASE_ENDPOINT}/eleicao/listar/municipios/{ELECTION_CODE}/{city}/cargos"
    response = requests.get(endpoint)
    if response:
        return response.json()
    return


def get_candidates_from(city, position_code):
    endpoint = f"{BASE_ENDPOINT}/candidatura/listar/2020/{city}/{ELECTION_CODE}/{position_code}/candidatos"
    response = requests.get(endpoint)
    if response:
        return response.json()
    return


def get_proposal_url(candidate_response):
    file_name = None
    url = None
    for file_ in candidate_response["arquivos"]:
        if file_["codTipo"] == "5":
            url = file_["url"]
            file_name = file_["nome"]
            break

    if url and file_name:
        return f"https://divulgacandcontas.tse.jus.br/{url}{file_name}"
    return


def download_proposals(url):
    response = requests.get(url)
    candidate_name = candidate_response["nomeUrna"].lower().replace(" ", "-")
    with open(f"proposta-candidato-{candidate_name}.pdf", "wb") as f:
        f.write(response.content)


def get_candidate(city, candidate_code):
    endpoint = f"{BASE_ENDPOINT}/candidatura/buscar/2020/{city}/{ELECTION_CODE}/candidato/{candidate_code}"
    response = requests.get(endpoint)
    if response:
        return response.json()
    return


def fill_zeroes(code):
    code = str(code)
    if len(code) < 5:  # expected code e.g. 00094
        zeroes = 5 - len(code)
        return f"{'0' * zeroes}{code}"
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exporte para um csv as propostas dos candidatos a prefeito.")
    parser.add_argument("--download-proposals", action="store_true", help="Faz download do PDF das propostas.")
    args = parser.parse_args()
    
    cities = {}
    with open("diretorio_municipios.csv", "r") as f:
        all_cities = csv.DictReader(f)
        for city in all_cities:
            cities[city["id_municipio_TSE"]] = {
                "code": city["id_municipio_TSE"],
                "city": city["municipio"],
                "state": city["estado_abrev"]
            }

    position_code = "11"  # prefeito
    with open("propostas-de-governo.csv", "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(["codigo_cidade_tse", "municipio", "sigla_estado", "codigo_prefeito_tse", "nome_urna", "url"])
        for city in cities.values():
            city_code = fill_zeroes(city["code"])
            candidates = get_candidates_from(city_code, position_code)
            print(city_code, city)
            for candidate in candidates["candidatos"]:
                candidate_details = get_candidate(city["code"], candidate["id"])
                url = get_proposal_url(candidate_details)
                spamwriter.writerow([city["code"], city["city"], city["state"], candidate_details[""], candidate_details[""], url])
                
                if args.download_proposals:
                    download_proposals(candidate_details)
