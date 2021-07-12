import requests
import datetime

from shercon.abstracts import Source

COINGECKO = "https://api.coingecko.com/api/v3"

class CoingeckoSpotPrice(Source):
    def run(*args):
        url = COINGECKO + "/simple/price"
        payload = {"ids": ",".join(args), "vs_currencies": ["usd"]}
        return requests.get(url, params=payload).json()

class CoingeckoMovingAverage(Source):
    def run(*args):
        token, days = args

        url = COINGECKO + "/coins/%s/market_chart" % token

        payload = {"days": days, "vs_currency": "usd"}
        data = requests.get(url, params=payload).json()

        # TODO is this right way? Do we need to take into account time differences
        # between data points
        total = 0.0
        for dp in data["prices"]:
            timestamp, price = dp
            total += price
        return total / len(data["prices"])