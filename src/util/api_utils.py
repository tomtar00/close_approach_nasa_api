import json
from urllib.request import urlopen
import urllib.parse

def get_json_from_url(url):
    return json.loads(urlopen(url).read())

def text_to_ulr(text):
    return urllib.parse.quote_plus(text)