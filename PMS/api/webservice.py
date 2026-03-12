import requests

BASE_URL = "http://localhost:3000/api"


def request(method, endpoint, datos=None):

    url = BASE_URL + endpoint

    try:
        response = requests.request(method, url, json=datos)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print("Error en el webservice:", e)
        return None


def get(endpoint):
    return request("GET", endpoint)


def post(endpoint, datos):
    return request("POST", endpoint, datos)


def put(endpoint, datos):
    return request("PUT", endpoint, datos)


def patch(endpoint, datos):
    return request("PATCH", endpoint, datos)

def delete(endpoint):
    return request("DELETE", endpoint)