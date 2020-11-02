from pprint import pprint
import requests


BASE_ENDPOINT = "http://divulgacandcontas.tse.jus.br/divulga/rest/v1"

def get_positions_from(city, state):
    endpoint = f"{BASE_ENDPOINT}/eleicao/listar/municipios/{city}/{state}/cargos"
    response = requests.get(endpoint)
    if response:
        return response.json()
    return


def get_candidates_from(state, city, position_code):
    endpoint = f"{BASE_ENDPOINT}/candidatura/listar/2020/{state}/{city}/{position_code}/candidatos"
    response = requests.get(endpoint)
    if response:
        return response.json()
    return


def download_proposals(candidate_response):
    file_name = None
    url = None
    for file_ in candidate_response["arquivos"]:
        if file_["codTipo"] == "5":
            url = file_["url"]
            file_name = file_["nome"]
            break

    if url and file_name:
        url = f"https://divulgacandcontas.tse.jus.br/{url}{file_name}"
        print(url)
        response = requests.get(url)
        candidate_name = candidate_response["nomeUrna"].lower().replace(" ", "-")
        with open(f"proposta-candidato-{candidate_name}.pdf", "wb") as f:
            f.write(response.content)
    return


def get_candidate(state, city, candidate_code):
    endpoint = f"{BASE_ENDPOINT}/candidatura/buscar/2020/{state}/{city}/candidato/{candidate_code}"
    response = requests.get(endpoint)
    if response:
        return response.json()
    return


if __name__ == "__main__":
    # TODO receber cidade e estado pela linha de comando
    city = "2030402020"
    state = "35157"
    positions_response = get_positions_from(city, state)
    # pprint(positions_response)
    position_code = positions_response["cargos"][0]["codigo"]  # prefeito
    candidates = get_candidates_from(state, city, position_code)
    # pprint(candidates)
    for candidate in candidates["candidatos"]:
        candidate_details = get_candidate(state, city, candidate["id"])
        download_proposals(candidate_details)
