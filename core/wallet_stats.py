"""
Wallet Stats Engine

Wallet ve trade istatistiklerini hesaplar.
"""

import logging
from database.wallet_db import get_wallet
from database.trade_db import get_trades_by_status

logger = logging.getLogger(__name__)


def get_wallet_stats():
    """
    Wallet ve trade istatistiklerini döndürür.
    
    Returns:
        dict: {
            "wallet": float,
            "profit": float,
            "wins": int,
            "losses": int,
            "win_rate": float,
            "total": int
        }
    """
    try:
        wallet = get_wallet()
        closed = get_trades_by_status("CLOSED")

        wins = 0
        losses = 0
        total_profit = 0

        for trade in closed:
            try:
                profit = trade[15] if len(trade) > 15 and trade[15] else 0
                total_profit += profit

                if profit > 0:
                    wins += 1
                elif profit < 0:
                    losses += 1
            except (IndexError, TypeError) as e:
                logger.warning(f"⚠️ Invalid trade data: {e}")
                continue

        total = wins + losses

        if total == 0:
            win_rate = 0
        else:
            win_rate = round((wins / total) * 100, 2)

        stats = {
            "wallet": wallet,
            "profit": total_profit,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "total": total
        }
        
        logger.debug(f"Wallet stats: {stats}")
        return stats
    
    except Exception as e:
        logger.error(f"❌ Error getting wallet stats: {e}")
        return {
            "wallet": 0,
            "profit": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "total": 0
        }
