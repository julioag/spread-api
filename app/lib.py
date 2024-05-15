import requests

buda_url = "https://www.buda.com/api/v2"


def get_spread(data: dict) -> float:
    min_ask = float(data["ticker"]["min_ask"][0])
    max_bid = float(data["ticker"]["max_bid"][0])
    return min_ask - max_bid


def get_ticker_from_api(market_id):
    url = buda_url + "/markets/" + market_id + "/ticker"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Could not retreive external api data")
    data = response.json()
    return data


def get_markets():
    url = buda_url + "/markets"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Cannot retreive data from external api")
    data = response.json()
    return data
