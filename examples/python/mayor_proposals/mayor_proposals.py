import argparse
import csv
from pathlib import Path
from pprint import pprint
import random
import os
import time, datetime

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
Os PDFs baixados estarão na subpasta `pdfs`, separados
por estado e cidade.
"""

BASE_ENDPOINT = "http://divulgacandcontas.tse.jus.br/divulga/rest/v1"
ELECTION_CODE = "2030402020" # eleições municipais de 2020
POSITION_CODE = "11"  # prefeito
# espera entre requisições (mínimo e máximo em segundos)
WAIT_INTERVAL = (3, 10)
TIMEOUT = 20 # se não responder em 20 segundos vai falhar
SCHEMA = (
    "codigo_cidade_tse", "municipio", "sigla_estado",
    "codigo_prefeito_tse", "nome_urna", "sigla_partido", "url"
)

def get_positions_from(city):
    endpoint = f"{BASE_ENDPOINT}/eleicao/listar/municipios/{ELECTION_CODE}/{city}/cargos"
    response = requests.get(endpoint, timeout=TIMEOUT)
    if response:
        return response.json()
    return


def get_candidates_from(city, position_code):
    endpoint = f"{BASE_ENDPOINT}/candidatura/listar/2020/{city}/{ELECTION_CODE}/{position_code}/candidatos"
    response = requests.get(endpoint, timeout=TIMEOUT)
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


def download_proposals(url, state, city, candidate_name):
    Path(f"pdfs/{state}/{city}").mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=TIMEOUT)
    candidate_name = candidate_name.lower().replace(" ", "-")
    file_name = f"pdfs/{state}/{city}/proposta-candidato-{candidate_name}.pdf"
    with open(file_name, "wb") as f:
        f.write(response.content)


def get_candidate(city, candidate_code):
    endpoint = f"{BASE_ENDPOINT}/candidatura/buscar/2020/{city}/{ELECTION_CODE}/candidato/{candidate_code}"
    response = requests.get(endpoint, timeout=TIMEOUT)
    if response:
        return response.json()
    return


def fill_zeroes(code):
    code = str(code)
    if len(code) < 5:  # verifica se tem tamanho esperado e.g. 00094
        zeroes = 5 - len(code)
        return f"{'0' * zeroes}{code}"
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=\
        "Exporte para um csv as propostas dos candidatos a prefeito."
        )
    parser.add_argument(
        "--download-proposals",
        action="store_true",
        help="Faz download do PDF das propostas."
        )
    parser.add_argument("--state", help="Sigla do estado desejado.")
    parser.add_argument(
        "--continue-from",
        help="Arquivo CSV parcial a continuar"
        )
    args = parser.parse_args()

    start = datetime.datetime.now()

    state_label = f"-{args.state}" if args.state else ""
    file_name = f"propostas-de-governo{state_label}.csv"
    skip_cities = set() # essas já foram coletadas
    skip_proposals = set()
    if args.continue_from:
        file_name = args.continue_from
        if not os.path.exists(file_name):
            raise ValueError(f"O arquivo não existe: {file_name}")
        with open(file_name, "r") as f:
            reader = csv.DictReader(f)
            if tuple(reader.fieldnames) != SCHEMA:
                raise ValueError(
                    f"Os campos do arquivo {file_name} não correspondem"
                    " ao esquema esperado:\n\n" +
                    ",".join(SCHEMA))
            for row in reader:
                city_code = row['codigo_cidade_tse']
                if city_code not in skip_cities: # nova cidade
                    skip_proposals = set() # não precisa guardar os anteriores
                skip_cities.add(city_code)
                skip_proposals.add(row['codigo_prefeito_tse'])
            # o último não deve ser pulado pois pode estar incompleto
            skip_cities.remove(city_code)
            print(f"Continuando a partir de {city_code}...")

    cities = {}
    with open("diretorio_municipios.csv", "r") as f:
        all_cities = csv.DictReader(f)
        for city in all_cities:
            cities[city["id_municipio_TSE"]] = {
                "code": city["id_municipio_TSE"],
                "city": city["municipio"],
                "state": city["estado_abrev"]
            }

    with open(
        file_name,
        "a" if args.continue_from else "w",
        newline=""
        ) as csvfile:
        spamwriter = csv.writer(csvfile)
        if not args.continue_from:
            spamwriter.writerow(SCHEMA)
        for city in cities.values():
            city_code = fill_zeroes(city["code"])
            follow_city = \
                (
                    (args.state and args.state.upper() == city["state"]) \
                    or not args.state
                ) and \
                (
                    city_code not in skip_cities \
                    or not args.continue_from
                )
            if follow_city:
                candidates = get_candidates_from(
                    city_code, POSITION_CODE)
                print(city_code, city)
                time.sleep(random.randint(*WAIT_INTERVAL))

                candidates_to_follow = (
                    candidate for candidate in candidates["candidatos"] \
                    if str(candidate["id"]) not in skip_proposals
                )
                for candidate in candidates_to_follow:
                    candidate_details = get_candidate(
                        city_code,
                        candidate["id"]
                        )
                    time.sleep(random.randint(*WAIT_INTERVAL))
                    url = get_proposal_url(candidate_details)
                    spamwriter.writerow([
                        city_code, city["city"], city["state"],
                        candidate_details["id"],
                        candidate_details["nomeUrna"],
                        candidate_details["partido"]["sigla"],
                        url
                        ])

                    if args.download_proposals:
                        download_proposals(
                            url, city["state"], city["city"],
                            candidate_details["nomeUrna"]
                            )
                        time.sleep(random.randint(*WAIT_INTERVAL))
    end = datetime.datetime.now()
    print(f"Tempo de execução: {str(end - start)}")
