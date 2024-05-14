def get_spread(data: dict) -> float:
    min_ask = float(data["ticker"]["min_ask"][0])
    max_bid = float(data["ticker"]["max_bid"][0])
    return min_ask - max_bid
