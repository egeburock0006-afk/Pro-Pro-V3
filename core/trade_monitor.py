"""
Trade Monitor

Backtest/test modunda açık işlemleri izler.
"""

import time
import logging

from helpers.test_formatter import test_dashboard
from services.telegram_service import send_message
from core.test_engine import (
    update_balance,
    add_trade,
    finished,
)
from database.trade_db import (
    get_open_trades,
    mark_tp1,
    mark_tp2,
    mark_tp3,
    mark_stop,
    close_trade,
)
from services.binance_service import get_price
from core.trade_engine import calculate_profit

logger = logging.getLogger(__name__)


def start_trade_monitor():
    """
    Test modunda işlemleri izler ve TP/SL kontrolü yapar.
    """
    logger.info("🛡 Trade Monitor Başlatıldı")

    while True:
        try:
            trades = get_open_trades()
            
            if not trades:
                logger.debug("No open trades")
                time.sleep(5)
                continue
            
            logger.info(f"📊 Monitoring {len(trades)} open trades...")

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

                    logger.debug(f"Checking {symbol}...")
                    
                    # Fiyat al
                    price = get_price(symbol)
                    if price is None:
                        logger.warning(f"⚠️ No price for {symbol}")
                        continue

                    if signal == "BUY":
                        check_buy_trade(
                            trade_id, symbol, entry, tp1, tp2, tp3, stop,
                            margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit, price
                        )
                    else:  # SELL
                        check_sell_trade(
                            trade_id, symbol, entry, tp1, tp2, tp3, stop,
                            margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit, price
                        )

                except ValueError as e:
                    logger.error(f"❌ Trade unpacking error: {e}")
                    continue
                except Exception as e:
                    logger.error(f"❌ Error checking trade {symbol}: {e}")
                    continue

            time.sleep(5)

        except Exception as e:
            logger.error(f"❌ Critical error in trade_monitor: {e}")
            time.sleep(5)


def check_buy_trade(trade_id, symbol, entry, tp1, tp2, tp3, stop, margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit, price):
    """
    BUY işlemi için TP/SL kontrolü.
    """
    try:
        # TP1
        if not tp1_hit and price >= tp1:
            logger.info(f"🎯 TP1 HIT -> {symbol}")
            mark_tp1(trade_id)

        # TP2
        elif tp1_hit and not tp2_hit and price >= tp2:
            logger.info(f"🚀 TP2 HIT -> {symbol}")
            mark_tp2(trade_id)

        # TP3
        elif tp2_hit and not tp3_hit and price >= tp3:
            logger.info(f"🏆 TP3 HIT -> {symbol}")
            roi, profit = calculate_profit(
                entry, price, margin, leverage, "BUY"
            )
            wallet = update_balance(profit)
            add_trade(win=True)
            
            logger.info(f"Wallet: {wallet:.2f}$")
            logger.info(f"ROI: {roi}%")
            logger.info(f"Profit: {profit}$")
            
            mark_tp3(trade_id)
            close_trade(trade_id, "TP3", roi, profit)
            
            if finished():
                logger.info("=" * 50)
                logger.info("🧪 TEST TAMAMLANDI")
                logger.info("=" * 50)
                try:
                    send_message("✅ 100 İşlem Testi Tamamlandı\n\n" + test_dashboard())
                except Exception as e:
                    logger.error(f"❌ Error sending test result: {e}")

        # Stop Loss
        elif not stop_hit and price <= stop:
            logger.info(f"🛑 STOP HIT -> {symbol}")
            roi, profit = calculate_profit(
                entry, price, margin, leverage, "BUY"
            )
            wallet = update_balance(profit)
            add_trade(win=False)
            
            logger.info(f"Wallet: {wallet:.2f}$")
            logger.info(f"ROI: {roi}%")
            logger.info(f"Profit: {profit}$")
            
            mark_stop(trade_id)
            close_trade(trade_id, "STOP", roi, profit)
            
            if finished():
                logger.info("=" * 50)
                logger.info("🧪 TEST TAMAMLANDI")
                logger.info("=" * 50)
                try:
                    send_message("✅ 100 İşlem Testi Tamamlandı\n\n" + test_dashboard())
                except Exception as e:
                    logger.error(f"❌ Error sending test result: {e}")

    except Exception as e:
        logger.error(f"❌ Error in check_buy_trade: {e}")


def check_sell_trade(trade_id, symbol, entry, tp1, tp2, tp3, stop, margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit, price):
    """
    SELL işlemi için TP/SL kontrolü.
    """
    try:
        # TP1
        if not tp1_hit and price <= tp1:
            logger.info(f"🎯 TP1 HIT -> {symbol}")
            mark_tp1(trade_id)

        # TP2
        elif tp1_hit and not tp2_hit and price <= tp2:
            logger.info(f"🚀 TP2 HIT -> {symbol}")
            mark_tp2(trade_id)

        # TP3
        elif tp2_hit and not tp3_hit and price <= tp3:
            logger.info(f"🏆 TP3 HIT -> {symbol}")
            roi, profit = calculate_profit(
                entry, price, margin, leverage, "SELL"
            )
            wallet = update_balance(profit)
            add_trade(win=True)
            
            logger.info(f"Wallet: {wallet:.2f}$")
            logger.info(f"ROI: {roi}%")
            logger.info(f"Profit: {profit}$")
            
            mark_tp3(trade_id)
            close_trade(trade_id, "TP3", roi, profit)
            
            if finished():
                logger.info("=" * 50)
                logger.info("🧪 TEST TAMAMLANDI")
                logger.info("=" * 50)
                try:
                    send_message("✅ 100 İşlem Testi Tamamlandı\n\n" + test_dashboard())
                except Exception as e:
                    logger.error(f"❌ Error sending test result: {e}")

        # Stop Loss
        elif not stop_hit and price >= stop:
            logger.info(f"🛑 STOP HIT -> {symbol}")
            roi, profit = calculate_profit(
                entry, price, margin, leverage, "SELL"
            )
            wallet = update_balance(profit)
            add_trade(win=False)
            
            logger.info(f"Wallet: {wallet:.2f}$")
            logger.info(f"ROI: {roi}%")
            logger.info(f"Profit: {profit}$")
            
            mark_stop(trade_id)
            close_trade(trade_id, "STOP", roi, profit)
            
            if finished():
                logger.info("=" * 50)
                logger.info("🧪 TEST TAMAMLANDI")
                logger.info("=" * 50)
                try:
                    send_message("✅ 100 İşlem Testi Tamamlandı\n\n" + test_dashboard())
                except Exception as e:
                    logger.error(f"❌ Error sending test result: {e}")

    except Exception as e:
        logger.error(f"❌ Error in check_sell_trade: {e}")
