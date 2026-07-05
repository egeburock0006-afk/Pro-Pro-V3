"""
Score Engine

Sinyal puanını hesaplar.
"""

import logging

logger = logging.getLogger(__name__)


def calculate_score(result):
    """
    AlphaTrend sonucuna göre score hesaplar.
    
    Args:
        result (dict): AlphaTrend sonucu {"signal": "BUY/SELL", "strength": X, ...}
    
    Returns:
        float: Hesaplanan score değeri
    """
    try:
        if not result:
            return 0
        
        score = 0
        signal = result.get("signal")
        strength = result.get("strength", 0)
        
        # AlphaTrend sinyali
        if signal in ("BUY", "SELL"):
            score += 40
        
        # Strength değerine göre
        if strength >= 70:
            score += 30
        elif strength >= 50:
            score += 20
        elif strength >= 30:
            score += 10
        
        logger.debug(f"Score calculated: {score} (strength: {strength})")
        return round(score, 2)
    
    except Exception as e:
        logger.error(f"❌ Error calculating score: {e}")
        return 0
