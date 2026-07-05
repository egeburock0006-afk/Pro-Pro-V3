"""
Telegram Bot - Dashboard Live Menüsü

Anlık dashboard bilgilerini gösterir.
"""

import logging
from core.dashboard import build_dashboard
from bot_ui.keyboards import back_keyboard

logger = logging.getLogger(__name__)


def dashboard_live():
    """
    Live dashboard'ı gösterir.
    
    Returns:
        tuple: (text, keyboard)
    """
    try:
        dashboard_text = build_dashboard()
        
        # Dashboard metin kontrolü
        if not dashboard_text:
            logger.warning("⚠️ Dashboard metni boş döndü")
            dashboard_text = "📊 Dashboard yüklenemedi."
        
        return dashboard_text, back_keyboard()
    
    except Exception as e:
        logger.error(f"❌ Error in dashboard_live: {e}")
        error_text = "❌ Dashboard yüklenemedi. Lütfen tekrar deneyin."
        return error_text, back_keyboard()
