import redis

from fastapi import FastAPI, status, HTTPException

from app.lib import get_spread, get_ticker_from_api, get_markets
from app.models import SpreadAlert

api = FastAPI()

buda_url = "https://www.buda.com/api/v2"

rd = redis.Redis(host="redis", port=6379, db=0)


@api.get("/spread/{market_id}")
def get_market_spread(market_id: str):
    try:
        data = get_ticker_from_api(market_id)
        spread = get_spread(data)
        return {"spread": spread}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.get("/spread/")
def get_all_markets_spread():
    try:
        data = get_markets()
        markets = list(map(lambda market: market["name"], data["markets"]))
        spreads = {}
        for market in markets:
            data = get_ticker_from_api(market)
            spreads[market] = get_spread(data)
        return spreads
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.post("/spread-alert/", status_code=status.HTTP_201_CREATED)
def post_new_spread_alert(spread_alert: SpreadAlert):
    rd.set(spread_alert.market, spread_alert.spread)
    return {"market": spread_alert.market, "spread": spread_alert.spread}


@api.get("/spread-alert/{market_id}")
def get_spread_alert(market_id: str):
    spread = rd.get(market_id)
    if spread is None:
        return {"error": "market not found"}
    return {"spread": float(spread)}


@api.get("/compare-spread-alert")
async def compare_spread_alerts(market_id: str, spread: float):
    alert = rd.get(market_id)
    if alert is None:
        return {"error": "alert not found"}
    if float(spread) > float(alert):
        return {"alert": "spread is higher than the alert"}
    if float(spread) == float(alert):
        return {"alert": "spread is equal to the alert"}
    return {"alert": "spread is lower than the alert"}
