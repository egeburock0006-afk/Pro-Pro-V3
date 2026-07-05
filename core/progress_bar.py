"""
Progress Bar Engine

Progress bar oluşturur ve hesaplar.
"""

import logging

logger = logging.getLogger(__name__)


def build_progress_bar(progress):
    """
    0-100 arasında progress bar oluşturur.
    
    Args:
        progress (float): Progress değeri (0-100)
    
    Returns:
        str: Progress bar stringi
    """
    try:
        progress = max(0, min(progress, 100))
        filled = int(progress / 10)
        
        chars = []
        for i in range(10):
            if i < filled:
                chars.append("█")
            else:
                chars.append("░")
        
        return "".join(chars)
    
    except Exception as e:
        logger.error(f"❌ Error building progress bar: {e}")
        return "░░░░░░░░░░"


def calculate_progress(signal, entry, tp3, current_price):
    """
    Entry'den TP3'e kadar olan progress'i hesaplar.
    
    Args:
        signal (str): "BUY" ya da "SELL"
        entry (float): Entry fiyatı
        tp3 (float): TP3 fiyatı
        current_price (float): Güncel fiyat
    
    Returns:
        float: Progress yüzdesi (0-100)
    """
    try:
        if signal == "BUY":
            total = tp3 - entry
            current = current_price - entry
        else:  # SELL
            total = entry - tp3
            current = entry - current_price

        if total <= 0:
            return 0

        progress = (current / total) * 100
        progress = max(0, min(progress, 100))
        
        return progress
    
    except Exception as e:
        logger.error(f"❌ Error calculating progress: {e}")
        return 0


def build_progress(signal, entry, tp3, current_price):
    """
    Progress bar'ı oluşturur.
    
    Args:
        signal (str): "BUY" ya da "SELL"
        entry (float): Entry fiyatı
        tp3 (float): TP3 fiyatı
        current_price (float/str): Güncel fiyat
    
    Returns:
        str: Progress bar stringi
    """
    try:
        # current_price None olabilir
        if current_price is None:
            current_price = entry
        
        progress = calculate_progress(
            signal,
            entry,
            tp3,
            float(current_price)
        )
        
        return build_progress_bar(progress)
    
    except Exception as e:
        logger.error(f"❌ Error in build_progress: {e}")
        return "░░░░░░░░░░"
