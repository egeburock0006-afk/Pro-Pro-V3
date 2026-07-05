"""
Trade View Engine

Trade card'ını oluşturur.
"""

import logging
from services.binance_service import get_price
from core.progress_bar import build_progress

logger = logging.getLogger(__name__)


def build_trade_card(trade):
    """
    Trade kart mesajını oluşturur.
    
    Args:
        trade (tuple): Trade verisi
    
    Returns:
        str: Trade kart mesajı ya da None
    """
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

        # Güncel fiyat al
        current = get_price(symbol)
        
        if current is None:
            current = entry

        # Progress bar oluştur
        bar = build_progress(
            signal,
            entry,
            tp3,
            current
        )

        direction = "LONG" if signal == "BUY" else "SHORT"
        emoji = "🟢" if signal == "BUY" else "🔴"

        text = f"""
{emoji} {symbol}    {direction}

{bar}

"""
        return text
    
    except Exception as e:
        logger.error(f"❌ Error building trade card: {e}")
        return None
