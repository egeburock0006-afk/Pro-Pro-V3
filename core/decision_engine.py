"""
Decision Engine

En iyi sinyali seçer.
"""

import logging

logger = logging.getLogger(__name__)


def choose_best_signal(signals):
    """
    Sinyallerden en iyi olanını seçer.
    
    Args:
        signals (list): Signal objelerinin listesi [{"score": X, ...}]
    
    Returns:
        dict: En iyi sinyal ya da None
    """
    if not signals:
        logger.warning("No signals provided")
        return None

    try:
        # Score'u 85+ olan adayları filtrele
        candidates = [
            s for s in signals
            if s.get("score", 0) >= 85
        ]

        if not candidates:
            logger.info("No candidates with score >= 85")
            return None

        # En yüksek score'u seç
        best = max(
            candidates,
            key=lambda x: x.get("score", 0)
        )

        logger.info(f"✅ Best signal selected: {best.get('symbol')} - Score: {best.get('score')}")
        return best
    
    except Exception as e:
        logger.error(f"❌ Error in choose_best_signal: {e}")
        return None
