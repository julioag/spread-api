from typing import Union
import requests

from fastapi import FastAPI

app = FastAPI()

buda_url = 'https://www.buda.com/api/v2'


@app.get("/spread/{market_id}")
def get_market_spread(market_id: str):
    url = buda_url + '/markets/' + market_id + '/ticker'
    response = requests.get(url)
    data = response.json()
    spread = float(data['ticker']['min_ask'][0]) - float(data['ticker']['max_bid'][0])
    return {"spread": spread}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}