"""
FollowLine Pro AI V3
Scanner Engine

Sembol taraması ve sinyal bulma
"""

import time
import logging
from datetime import datetime

from config import INTERVAL

from services.binance_service import (
    get_futures_symbols,
    get_klines,
)

from services.telegram_service import (
    send_message,
    update_dashboard,
)

from strategies.alphatrend import AlphaTrend

from utils.indicators import ema, atr
from utils.mfi import mfi

from indicators.macd import macd
from indicators.adx import adx

from ai.score import calculate_ai_score
from core.score_engine import calculate_score

from database.trade_db import (
    save_trade,
    has_open_trade,
    get_open_trades,
)

from database.signal_db import (
    get_last_signal,
    save_signal,
)

from core.dashboard import build_dashboard

from bot_ui.menus.dashboard import (
    dashboard_keyboard,
)

from helpers.telegram_formatter import (
    format_trade_card,
)

from core.test_engine import (
    get_wallet,
    get_position_size,
)

logger = logging.getLogger(__name__)
alpha = AlphaTrend()


def scan_symbol(symbol):
    """
    Tek sembolü tarar ve sinyal bulur.
    
    Args:
        symbol (str): Sembol adı (örn: BTCUSDT)
    
    Returns:
        dict: Sinyal verisi ya da None
    """
    try:
        logger.debug(f"🔍 Scanning {symbol}")

        if has_open_trade(symbol):
            return None

        df = get_klines(
            symbol=symbol,
            interval=INTERVAL
        )

        if df is None:
            return None

        # Göstergeler
        df["EMA200"] = ema(df["close"], 200)
        df["ATR"] = atr(df, 14)
        df["MFI"] = mfi(df)

        macd_line, signal_line, hist = macd(df["close"])

        df["MACD"] = macd_line
        df["MACD_SIGNAL"] = signal_line
        df["ADX"] = adx(df)

        # AlphaTrend sinyali
        result = alpha.last_signal(df)

        if result is None or result.get("signal") is None:
            return None

        entry = result["price"]
        atr_value = result["atr"]

        # TP ve Stop hesapla
        if result["signal"] == "BUY":
            tp1 = entry + atr_value * 2
            tp2 = entry + atr_value * 4
            tp3 = entry + atr_value * 6
            stop = entry - atr_value * 2
        else:  # SELL
            tp1 = entry - atr_value * 2
            tp2 = entry - atr_value * 4
            tp3 = entry - atr_value * 6
            stop = entry + atr_value * 2

        # Score hesapla
        ai_score = calculate_ai_score(
            result,
            df["EMA200"].iloc[-1],
            result["price"],
            df["MFI"].iloc[-1],
            df["MACD"].iloc[-1],
            df["ADX"].iloc[-1]
        )

        score = calculate_score(result)

        return {
            "symbol": symbol,
            "signal": result["signal"],
            "entry": entry,
            "tp1": tp1,
            "tp2": tp2,
            "tp3": tp3,
            "stop": stop,
            "score": score,
            "ai": ai_score,
            "strength": result.get("strength", 0),
            "atr": atr_value,
        }

    except Exception as e:
        logger.error(f"❌ Error scanning {symbol}: {e}")
        return None


def choose_best_signal(signals):
    """
    Sinyallerden en iyi olanını seçer.
    
    Args:
        signals (list): Sinyal listesi
    
    Returns:
        dict: En iyi sinyal ya da None
    """
    if not signals:
        logger.warning("No signals found")
        return None

    try:
        signals = sorted(
            signals,
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        logger.info("\n" + "="*30)
        logger.info("🏆 TOP 10 SIGNALS")
        logger.info("="*30)

        for i, s in enumerate(signals[:10], 1):
            logger.info(
                f"{i}. {s['symbol']} | "
                f"{s['signal']} | "
                f"Score={s['score']}"
            )

        best = signals[0]
        logger.info(f"\n✅ Best signal: {best['symbol']} (Score: {best['score']})\n")
        return best
    
    except Exception as e:
        logger.error(f"❌ Error choosing best signal: {e}")
        return None


async def start_scan():
    """
    Ana tarama döngüsünü başlatır.
    """
    logger.info("🚀 FollowLine Pro AI V3 Başlatıldı")

    while True:
        try:
            # Dashboard güncelle
            try:
                update_dashboard(
                    build_dashboard(),
                    dashboard_keyboard()
                )
            except Exception as e:
                logger.warning(f"⚠️ Dashboard update error: {e}")

            # Açık işlem varsa yeni işlem arama
            open_trades = get_open_trades()
            if len(open_trades) > 0:
                logger.info(f"🟡 {len(open_trades)} açık işlem var. Tarama bekliyor...")
                time.sleep(20)
                continue

            logger.info("\n" + "="*30)
            logger.info("🔍 Tarama Başladı")
            logger.info("="*30)

            # Sembolleri al
            symbols = get_futures_symbols()
            if not symbols:
                logger.warning("❌ Sembol listesi alınamadı")
                time.sleep(60)
                continue

            logger.info(f"📊 Taranacak sembol: {len(symbols)}")

            # Sembolleri tara
            signals = []
            for symbol in symbols:
                result = scan_symbol(symbol)
                if result is not None:
                    signals.append(result)

            logger.info(f"✅ Bulunan Sinyal: {len(signals)}")

            # En iyi sinyali seç
            best_signal = choose_best_signal(signals)

            if best_signal is None:
                logger.warning("❌ Uygun sinyal bulunamadı.")
                time.sleep(60)
                continue

            logger.info("\n" + "="*30)
            logger.info("🏆 EN İYİ SİNYAL")
            logger.info("="*30)
            logger.info(best_signal)

            wallet = get_wallet()
            position = get_position_size()

            best_signal["wallet"] = wallet
            best_signal["position"] = position

            # Trade Kaydet
            try:
                save_trade(
                    best_signal["symbol"],
                    best_signal["signal"],
                    best_signal["entry"],
                    best_signal["tp1"],
                    best_signal["tp2"],
                    best_signal["tp3"],
                    best_signal["stop"]
                )

                save_signal(
                    best_signal["symbol"],
                    best_signal["signal"]
                )

                # Telegram mesaj
                try:
                    send_message(
                        format_trade_card(best_signal)
                    )
                except Exception as e:
                    logger.error(f"❌ Telegram error: {e}")

                logger.info(f"💰 Wallet: {wallet}$")
                logger.info(f"📦 Position: {position}$")
                logger.info(f"⭐ Score: {best_signal['score']}")
                logger.info("⏳ 60 saniye bekleniyor...\n")

            except Exception as e:
                logger.error(f"❌ Error saving trade: {e}")

            time.sleep(60)

        except Exception as e:
            logger.error(f"❌ Critical error in start_scan: {e}")
            time.sleep(60)
