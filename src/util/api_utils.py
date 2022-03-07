import json
import requests
from urllib.request import urlopen
import urllib.parse

def get_json_from_url(url):
    response = requests.get(url)
    if(response.status_code != requests.codes.ok):
        raise Exception(f'Failed to read data from url ({url}) Status code {response.status_code}')
    return response.json()

def format_json(json_str):
    return json.dumps(json_str, indent=4)

def text_to_ulr(text):
    return urllib.parse.quote_plus(text)