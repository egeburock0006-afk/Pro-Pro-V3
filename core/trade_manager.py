"""
Trade Manager

Açık işlemleri izler ve TP/SL kontrolü yapar.
"""

import logging
from core.trade_engine import calculate_roi, calculate_profit
from core.test_engine import update_balance
from database.trade_db import (
    get_open_trades,
    close_trade,
    mark_tp1,
    mark_tp2,
    mark_tp3,
    mark_stop,
)
from services.binance_service import get_klines
from services.telegram_service import send_message

logger = logging.getLogger(__name__)


def calculate_pnl(entry, current, margin, leverage, signal):
    """
    Kâr/Zarar (P&L) hesaplar.
    
    Args:
        entry (float): Entry fiyatı
        current (float): Güncel fiyat
        margin (float): Margin
        leverage (float): Kaldıraç
        signal (str): "BUY" ya da "SELL"
    
    Returns:
        tuple: (percent, usdt)
    """
    try:
        if signal == "BUY":
            percent = ((current - entry) / entry) * 100
        else:  # SELL
            percent = ((entry - current) / entry) * 100

        position = margin * leverage
        pnl = position * (percent / 100)

        return round(percent, 2), round(pnl, 2)
    
    except Exception as e:
        logger.error(f"❌ Error calculating PNL: {e}")
        return 0, 0


def check_trades():
    """
    Açık işlemleri izler ve TP/SL kontrolü yapar.
    """
    try:
        trades = get_open_trades()

        if not trades:
            logger.debug("No open trades to check")
            return

        logger.info(f"📊 Checking {len(trades)} open trades...")

        for trade in trades:
            try:
                (
                    trade_id,
                    symbol,
                    signal,
                    entry,
                    tp1,
                    tp2,
                    tp3,
                    stop,
                    margin,
                    leverage,
                    tp1_hit,
                    tp2_hit,
                    tp3_hit,
                    stop_hit,
                ) = trade

                # Klines al
                df = get_klines(symbol)
                if df is None:
                    logger.warning(f"⚠️ No klines for {symbol}")
                    continue

                price = float(df["close"].iloc[-1])
                logger.debug(f"{symbol}: {price}$")

                if signal == "BUY":
                    check_buy_signal(
                        trade_id, symbol, entry, tp1, tp2, tp3, stop,
                        margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit, price
                    )
                else:  # SELL
                    check_sell_signal(
                        trade_id, symbol, entry, tp1, tp2, tp3, stop,
                        margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit, price
                    )

            except ValueError as e:
                logger.error(f"❌ Trade unpacking error: {e}")
                continue
            except Exception as e:
                logger.error(f"❌ Error checking trade: {e}")
                continue

    except Exception as e:
        logger.error(f"❌ Critical error in check_trades: {e}")


def check_buy_signal(trade_id, symbol, entry, tp1, tp2, tp3, stop, margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit, price):
    """
    BUY sinyali için TP/SL kontrolü.
    """
    try:
        # TP1
        if price >= tp1 and tp1_hit == 0:
            percent, usdt = calculate_pnl(entry, price, margin, leverage, "BUY")
            message = f"🎯 {symbol}\n\nTP1 HIT ✅\n\nPrice: {price}\nProfit: {usdt}$ ({percent}%)"
            send_message(message)
            mark_tp1(trade_id)
            logger.info(f"✅ TP1 HIT: {symbol}")

        # TP2
        elif price >= tp2 and tp2_hit == 0:
            percent, usdt = calculate_pnl(entry, price, margin, leverage, "BUY")
            message = f"🚀 {symbol}\n\nTP2 HIT ✅\n\nPrice: {price}\nProfit: {usdt}$ ({percent}%)"
            send_message(message)
            mark_tp2(trade_id)
            logger.info(f"✅ TP2 HIT: {symbol}")

        # TP3
        elif price >= tp3 and tp3_hit == 0:
            roi, profit = calculate_profit(entry, price, margin, leverage, "BUY")
            wallet = update_balance(profit)
            message = f"💎 {symbol}\n\nTP3 HIT ✅\n\nPrice: {price}\nROI: {roi}%\nProfit: {profit}$\nWallet: {wallet}$"
            send_message(message)
            mark_tp3(trade_id)
            close_trade(trade_id, "TP3", roi, profit)
            logger.info(f"✅ TP3 HIT: {symbol} - Profit: {profit}$")

        # Stop Loss
        elif price <= stop and stop_hit == 0:
            roi, profit = calculate_profit(entry, price, margin, leverage, "BUY")
            wallet = update_balance(profit)
            message = f"🛑 {symbol}\n\nSTOP LOSS ❌\n\nPrice: {price}\nROI: {roi}%\nLoss: {profit}$\nWallet: {wallet}$"
            send_message(message)
            mark_stop(trade_id)
            close_trade(trade_id, "STOP", roi, profit)
            logger.warning(f"❌ STOP HIT: {symbol} - Loss: {profit}$")

    except Exception as e:
        logger.error(f"❌ Error in check_buy_signal: {e}")


def check_sell_signal(trade_id, symbol, entry, tp1, tp2, tp3, stop, margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit, price):
    """
    SELL sinyali için TP/SL kontrolü.
    """
    try:
        # TP1
        if price <= tp1 and tp1_hit == 0:
            message = f"🎯 {symbol}\n\nTP1 HIT ✅\n\nPrice: {price}"
            send_message(message)
            mark_tp1(trade_id)
            logger.info(f"✅ TP1 HIT: {symbol}")

        # TP2
        elif price <= tp2 and tp2_hit == 0:
            message = f"🚀 {symbol}\n\nTP2 HIT ✅\n\nPrice: {price}"
            send_message(message)
            mark_tp2(trade_id)
            logger.info(f"✅ TP2 HIT: {symbol}")

        # TP3
        elif price <= tp3 and tp3_hit == 0:
            roi, profit = calculate_profit(entry, price, margin, leverage, "SELL")
            wallet = update_balance(profit)
            message = f"💎 {symbol}\n\nTP3 HIT ✅\n\nPrice: {price}\nROI: {roi}%\nProfit: {profit}$\nWallet: {wallet}$"
            send_message(message)
            mark_tp3(trade_id)
            close_trade(trade_id, "TP3", roi, profit)
            logger.info(f"✅ TP3 HIT: {symbol} - Profit: {profit}$")

        # Stop Loss
        elif price >= stop and stop_hit == 0:
            roi, profit = calculate_profit(entry, price, margin, leverage, "SELL")
            wallet = update_balance(profit)
            message = f"🛑 {symbol}\n\nSTOP LOSS ❌\n\nPrice: {price}\nROI: {roi}%\nLoss: {profit}$\nWallet: {wallet}$"
            send_message(message)
            mark_stop(trade_id)
            close_trade(trade_id, "STOP", roi, profit)
            logger.warning(f"❌ STOP HIT: {symbol} - Loss: {profit}$")

    except Exception as e:
        logger.error(f"❌ Error in check_sell_signal: {e}")
