"""
FollowLine Pro AI V3

Binance Service

Bu servis Binance ile haberleşen tek katmandır.
"""

import time
from requests.exceptions import ReadTimeout
from binance.client import Client
import pandas as pd
from config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)


def test_connection():
    """
    Binance bağlantısını test eder.
    """

    try:

        client.ping()

        return True

    except Exception as e:

        print(f"❌ Binance Connection Error : {e}")

        return False
def get_futures_symbols():
    """
    Binance Futures işlem gören sembolleri döndürür.
    """

    exchange_info = client.futures_exchange_info()

    symbols = []

    for symbol in exchange_info["symbols"]:

        if symbol["status"] == "TRADING":

            symbols.append(symbol["symbol"])

    return symbols
def get_klines(symbol="BTCUSDT", interval="5m", limit=200):

    for attempt in range(3):

        try:

            klines = client.futures_klines(
                symbol=symbol,
                interval=interval,
                limit=limit,
            )

            break

        except ReadTimeout:

            print(f"⏳ {symbol} timeout... Tekrar deneniyor ({attempt+1}/3)")
            time.sleep(2)

        except Exception as e:

            print(f"❌ {symbol} -> {e}")
            time.sleep(2)

    else:

        return None

    df = pd.DataFrame(
        klines,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_volume",
            "trades",
            "tb_base",
            "tb_quote",
            "ignore",
        ],
    )

    df = df.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float,
    })

    return df

def get_price(symbol):
    
    print("PRICE REQUEST ->", symbol)
    ...

    try:

        ticker = client.futures_symbol_ticker(
            symbol=symbol
        )

        return float(ticker["price"])

    except Exception as e:

        print(f"❌ Price Error ({symbol}) : {e}")

        return None
    
def get_current_price(symbol):

    ticker = client.futures_symbol_ticker(symbol=symbol)

    return float(ticker["price"])
    
    
    
    
    