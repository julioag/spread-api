import requests
import redis

from fastapi import FastAPI, status

from lib import get_spread
from models import SpreadAlert

api = FastAPI()

buda_url = "https://www.buda.com/api/v2"

rd = redis.Redis(host="redis", port=6379, db=0)


@api.get("/spread/{market_id}")
async def get_market_spread(market_id: str):
    url = buda_url + "/markets/" + market_id + "/ticker"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "market not found"}
    data = response.json()
    spread = get_spread(data)
    return {"spread": spread}


@api.get("/spread/")
async def get_all_markets_spread():
    url = buda_url + "/markets"
    response = requests.get(url)
    data = response.json()
    markets = list(map(lambda market: market["name"], data["markets"]))
    spreads = {}
    for market in markets:
        url = buda_url + "/markets/" + market + "/ticker"
        response = requests.get(url)
        data = response.json()
        spreads[market] = get_spread(data)
    return spreads


@api.post("/spread-alert/", status_code=status.HTTP_201_CREATED)
async def post_new_spread_alert(spread_alert: SpreadAlert):
    rd.set(spread_alert.market, spread_alert.spread)
    return {"market": spread_alert.market, "spread": spread_alert.spread}


@api.get("/spread-alert/{market_id}")
async def get_spread_alert(market_id: str):
    spread = rd.get(market_id)
    if spread is None:
        return {"error": "market not found"}
    return {"spread": float(spread)}


@api.get("/spread-alert-check/")
async def check_spread_alerts(market_id: str, spread: float):
    alert = rd.get(market_id)
    if alert is None:
        return {"error": "alert not found"}
    if float(spread) > float(alert):
        return {"alert": "spread is higher than the alert"}
    return {"alert": "spread is lower than the alert"}
