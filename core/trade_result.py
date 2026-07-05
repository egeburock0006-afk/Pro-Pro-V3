"""
Trade Result Engine

Trade sonuçlarını işler.
"""

import logging
from database.wallet_db import get_wallet, update_wallet

logger = logging.getLogger(__name__)


def process_trade_result(profit):
    """
    Trade sonucunu işler ve wallet'i günceller.
    
    Args:
        profit (float): Kar/zarar miktarı
    
    Returns:
        float: Yeni wallet miktarı ya da None (hata durumunda)
    """
    try:
        wallet = get_wallet()
        wallet += profit
        update_wallet(wallet)
        
        logger.info(f"✅ Trade result processed: profit={profit}$, wallet={wallet}$")
        return wallet
    
    except Exception as e:
        logger.error(f"❌ Error processing trade result: {e}")
        return None
