""" API wrapper for Coingecko. """
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from ratelimit import ratelimit
from coingecko.helpers import from_iso_8601


EXIDS = {'ftx': 'ftx_spot'}                     # coingecko exchangeids
URL = 'https://api.coingecko.com/api/v3'        # coingecko endpoint


cache = {}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
@ratelimit(duration=2, sleep=True)
def fetch(endpoint: str) -> dict:
    """ Fetches data for method.

    Args:
        endpoint (str): endpoint to fetch data from

    Returns:
        dict: data from endpoint
    """
    headers = {'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}
    return requests.get(f'{URL}/{endpoint}', headers=headers).json()


def get_historical_price(coinid: str, date: str) -> float:
    """ Returns the price of a coin on a given date.

    Args:
        symbol (str): coin symbol
        date (str): date in iso 8601 format

    Returns:
        float: price of coin on given date
    """

    date = from_iso_8601(date)
    if date in cache.get(coinid, {}):
        return cache[coinid][date]
    result = fetch(f'coins/{coinid}/history?date={date}')
    price = result['market_data']['current_price']['usd'] if 'market_data' in result else 0
    if coinid not in cache:
        cache[coinid] = {}
    cache[coinid][date] = price
    return price


def get_exchange_tickers(exchange: str) -> dict:
    """ Returns a dict with all tickers for a given exchange.

    Args:
        exchange (str): exchange name

    Returns:
        dict: all tickers for a given exchange
    """
    result = {}
    page = 1
    exchange_id = EXIDS.get(exchange, exchange)
    while tickers := fetch(f'exchanges/{exchange_id}/tickers?page={page}').get('tickers', []):
        result.update({ticker['base']: ticker['coin_id'] for ticker in tickers if 'coin_id' in ticker})
        page += 1
    return result
