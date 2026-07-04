from helpers.pnl_calculator import calculate_profit
from core.trade_result import process_trade_result
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
from helpers.telegram_formatter import (
    format_tp1,
    format_tp2,
    format_tp3,
)


def calculate_pnl(entry, current, margin, leverage, signal):
    """Calculate P&L in percentage and USDT"""
    if signal == "BUY":
        percent = ((current - entry) / entry) * 100
    else:
        percent = ((entry - current) / entry) * 100

    position = margin * leverage
    pnl = position * (percent / 100)

    return round(percent, 2), round(pnl, 2)


def profit_percent(entry, current, signal):
    """Calculate profit percentage"""
    if signal == "BUY":
        return ((current - entry) / entry) * 100

    return ((entry - current) / entry) * 100


def check_trades():
    """Monitor open trades and check for TP/SL hits"""
    trades = get_open_trades()

    for trade in trades:
        trade_id, symbol, signal, entry, tp1, tp2, tp3, stop, margin, leverage, tp1_hit, tp2_hit, tp3_hit, stop_hit = trade
        df = get_klines(symbol)

        if df is None:
            continue

        price = float(df["close"].iloc[-1])

        if signal == "BUY":
            # Check TP1
            if price >= tp1 and tp1_hit == 0:
                profit_percent_val, profit_usdt = calculate_pnl(
                    entry,
                    price,
                    margin,
                    leverage,
                    signal
                )
                send_message(
                    format_tp1(
                        symbol,
                        entry,
                        price,
                        profit_percent_val,
                        profit_usdt,
                        margin,
                        leverage
                    )
                )
                mark_tp1(trade_id)

            # Check TP2
            elif price >= tp2 and tp2_hit == 0:
                profit_percent_val, profit_usdt = calculate_pnl(
                    entry,
                    price,
                    margin,
                    leverage,
                    signal
                )
                send_message(
                    format_tp2(
                        symbol,
                        entry,
                        price,
                        profit_percent_val,
                        profit_usdt,
                        margin,
                        leverage
                    )
                )
                mark_tp2(trade_id)

            # Check TP3
            elif price >= tp3 and tp3_hit == 0:
                roi, profit = calculate_profit(
                    entry,
                    price,
                    margin,
                    leverage,
                    signal
                )
                wallet = update_balance(profit)
                print(f"Wallet : {wallet}$")
                print(f"ROI : {roi}%")
                print(f"Profit : {profit}$")
                send_message(
                    f"💎 {symbol}\n\nTP3 HIT ✅\n\nPrice : {price}"
                )
                mark_tp3(trade_id)
                close_trade(
                    trade_id,
                    "TP3",
                    roi,
                    profit
                )

            # Check Stop Loss
            elif price <= stop and stop_hit == 0:
                roi, profit = calculate_profit(
                    entry,
                    price,
                    margin,
                    leverage,
                    signal
                )
                wallet = update_balance(profit)
                print(f"Wallet : {wallet}$")
                send_message(
                    f"🛑 {symbol}\n\nSTOP LOSS ❌\n\nPrice : {price}"
                )
                mark_stop(trade_id)
                print(f"ROI    : {roi}%")
                print(f"Profit : {profit}$")
                close_trade(
                    trade_id,
                    "STOP",
                    roi,
                    profit
                )

        else:  # SELL signal
            # Check TP1
            if price <= tp1 and tp1_hit == 0:
                send_message(
                    f"🎯 {symbol}\n\nTP1 HIT ✅\n\nPrice : {price}"
                )
                mark_tp1(trade_id)

            # Check TP2
            elif price <= tp2 and tp2_hit == 0:
                send_message(
                    f"🚀 {symbol}\n\nTP2 HIT ✅\n\nPrice : {price}"
                )
                mark_tp2(trade_id)

            # Check TP3
            elif price <= tp3 and tp3_hit == 0:
                send_message(
                    f"🏆 {symbol}\n\nTP3 HIT ✅\n\nPrice : {price}"
                )
                roi, profit = calculate_profit(
                    entry,
                    price,
                    margin,
                    leverage,
                    signal
                )
                wallet = update_balance(profit)
                close_trade(
                    trade_id,
                    "TP3",
                    roi,
                    profit
                )

            # Check Stop Loss
            elif price >= stop and stop_hit == 0:
                send_message(
                    f"🛑 {symbol}\n\nSTOP LOSS ❌\n\nPrice : {price}"
                )
                roi, profit = calculate_profit(
                    entry,
                    price,
                    margin,
                    leverage,
                    signal
                )
                close_trade(
                    trade_id,
                    "STOP",
                    roi,
                    profit
                )
