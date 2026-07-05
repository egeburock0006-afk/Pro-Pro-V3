"""
FollowLine Pro AI V3

Binance Service

Bu servis Binance ile haberleşen tek katmandır.
"""

import time
import logging
from requests.exceptions import ReadTimeout
from binance.client import Client
import pandas as pd
from config import BINANCE_API_KEY, BINANCE_API_SECRET

logger = logging.getLogger(__name__)

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)


def test_connection():
    """
    Binance bağlantısını test eder.
    
    Returns:
        bool: Bağlantı başarılıysa True, başarısızsa False
    """
    try:
        client.ping()
        logger.info("✅ Binance Connection Successful")
        return True
    except Exception as e:
        logger.error(f"❌ Binance Connection Error: {e}")
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

        logger.debug(f"Found {len(symbols)} trading symbols")
        return symbols
    
    except Exception as e:
        logger.error(f"❌ Get Futures Symbols Error: {e}")
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
            logger.warning(f"⏳ {symbol} timeout... Tekrar deneniyor ({attempt + 1}/3)")
            time.sleep(2)

        except Exception as e:
            logger.error(f"❌ {symbol} Error: {e}")
            time.sleep(2)
    
    # Eğer veri alınamadıysa None döndür
    if klines is None:
        logger.error(f"❌ {symbol} - Tüm deneyler başarısız")
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

        logger.debug(f"{symbol}: {len(df)} klines fetched")
        return df
    
    except Exception as e:
        logger.error(f"❌ DataFrame oluşturma hatası ({symbol}): {e}")
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
        logger.debug(f"{symbol}: {price}")
        return price

    except Exception as e:
        logger.error(f"❌ Price Error ({symbol}): {e}")
        return None


def get_current_price(symbol):
    """
    Binance Futures sembolünün güncel fiyatını döndürür.
    Alias for get_price().
    
    Args:
        symbol (str): İşlem sembolü (örn: BTCUSDT)
    
    Returns:
        float: Sembolün güncel fiyatı ya da None (hata durumunda)
    """
    return get_price(symbol)
