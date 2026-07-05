"""
Stats Engine

Bot istatistiklerini hesaplar.
"""

import logging
from database.wallet_db import get_wallet
from database.trade_db import (
    get_open_trades,
    get_tp1_count,
    get_tp2_count,
    get_tp3_count,
    get_stop_count,
)

logger = logging.getLogger(__name__)


def get_stats():
    """
    Bot istatistiklerini döndürür.
    
    Returns:
        dict: {
            "wallet": float,
            "open_trades": int,
            "tp1": int,
            "tp2": int,
            "tp3": int,
            "stop": int,
            "win_rate": float
        }
    """
    try:
        wallet = get_wallet()
        open_trades = len(get_open_trades())
        tp1 = get_tp1_count()
        tp2 = get_tp2_count()
        tp3 = get_tp3_count()
        stop = get_stop_count()

        total_finished = tp3 + stop

        if total_finished == 0:
            win_rate = 0
        else:
            win_rate = round((tp3 / total_finished) * 100, 2)

        stats = {
            "wallet": wallet,
            "open_trades": open_trades,
            "tp1": tp1,
            "tp2": tp2,
            "tp3": tp3,
            "stop": stop,
            "win_rate": win_rate
        }
        
        logger.debug(f"Stats: {stats}")
        return stats
    
    except Exception as e:
        logger.error(f"❌ Error getting stats: {e}")
        return {
            "wallet": 0,
            "open_trades": 0,
            "tp1": 0,
            "tp2": 0,
            "tp3": 0,
            "stop": 0,
            "win_rate": 0
        }
