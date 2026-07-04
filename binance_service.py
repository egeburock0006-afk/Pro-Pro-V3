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
    
    Returns:
        bool: Bağlantı başarılıysa True, başarısızsa False
    """
    try:
        client.ping()
        print("✅ Binance Connection Successful")
        return True
    except Exception as e:
        print(f"❌ Binance Connection Error: {e}")
        return False


def get_futures_symbols():
    """
    Binance Futures işlem gören sembolleri döndürür.
    
    Returns:
        list: İşlem halindeki sembollerin listesi
    """
    try:
        exchange_info = client.futures_exchange_info()
        symbols = []

        for symbol in exchange_info["symbols"]:
            if symbol["status"] == "TRADING":
                symbols.append(symbol["symbol"])

        return symbols
    except Exception as e:
        print(f"❌ Get Futures Symbols Error: {e}")
        return []


def get_klines(symbol="BTCUSDT", interval="5m", limit=200):
    """
    Belirtilen sembol için kline verilerini döndürür.
    
    Args:
        symbol (str): İşlem sembolü (örn: BTCUSDT)
        interval (str): Zaman aralığı (örn: 5m, 1h, 1d)
        limit (int): Dönecek kline sayısı
    
    Returns:
        pd.DataFrame: Kline verilerini içeren DataFrame ya da None
    """
    klines = None
    
    for attempt in range(3):
        try:
            klines = client.futures_klines(
                symbol=symbol,
                interval=interval,
                limit=limit,
            )
            break

        except ReadTimeout:
            print(f"⏳ {symbol} timeout... Tekrar deneniyor ({attempt + 1}/3)")
            time.sleep(2)

        except Exception as e:
            print(f"❌ {symbol} -> {e}")
            time.sleep(2)
    
    # Eğer veri alınamadıysa None döndür
    if klines is None:
        print(f"❌ {symbol} - Tüm deneyler başarısız")
        return None

    try:
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
    
    except Exception as e:
        print(f"❌ DataFrame oluşturma hatası ({symbol}): {e}")
        return None


def get_price(symbol):
    """
    Binance Futures sembolünün güncel fiyatını döndürür.
    
    Args:
        symbol (str): İşlem sembolü (örn: BTCUSDT)
    
    Returns:
        float: Sembolün güncel fiyatı ya da None (hata durumunda)
    """
    try:
        ticker = client.futures_symbol_ticker(symbol=symbol)
        price = float(ticker["price"])
        print(f"✅ PRICE REQUEST -> {symbol}: {price}")
        return price

    except Exception as e:
        print(f"❌ Price Error ({symbol}): {e}")
        return None
