
import requests

def post_to_api(url, data):
    response = requests.post(url, json=data)
    return response.json()
    