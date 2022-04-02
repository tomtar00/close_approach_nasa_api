import json
import requests
import urllib.parse
import pandas as pd

api_key = '6t4LffN3Hom6Z0NdediRtQpdFpfQnegzY2PpYyqt'

def get_json_from_url(url):
    response = requests.get(url)
    if(response.status_code != requests.codes.ok):
        raise Exception(
            f'Failed to read data from url ({url}) Status code {response.status_code}')
    return response.json()


def getDataFromApi(date_min, date_max, body):
    # create URL
    URL = "https://ssd-api.jpl.nasa.gov/cad.api?" + "date-min=" + \
        date_min + "&date-max=" + date_max + "&body=" + body
    print("Fetch data from: " + URL)

    # send request and turn into text
    response = requests.get(URL).text

    # parse response json into dictionary
    dictionary = json.loads(response)

    # if has values
    print("number of values: " + dictionary["count"])

    if dictionary["count"] != "0":
        # create dataset
        completeData = [dictionary["fields"]] + dictionary["data"]

        # turning dictionary into dataframe
        df = pd.DataFrame.from_dict(completeData)
        df.columns = df.iloc[0]
        df = df[1:]

        # changing values into numeric  -- TEMPORARY --
        df["orbit_id"] = pd.to_numeric(df["orbit_id"], errors='ignore')
        df["jd"] = pd.to_numeric(df["jd"])
        df["dist"] = pd.to_numeric(df["dist"])
        df["dist_min"] = pd.to_numeric(df["dist_min"])
        df["dist_max"] = pd.to_numeric(df["dist_max"])
        df["v_rel"] = pd.to_numeric(df["v_rel"])
        df["v_inf"] = pd.to_numeric(df["v_inf"])
        df["h"] = pd.to_numeric(df["h"])
        df["cd"] = pd.to_datetime(df["cd"], format='%Y-%b-%d %H:%M')

        return df
    return None


def format_json(json_str):
    return json.dumps(json_str, indent=4)


def text_to_ulr(text):
    return urllib.parse.quote_plus(text)
