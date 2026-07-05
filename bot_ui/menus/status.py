"""
Telegram Bot - Bot Durum Menüsü

Bot ve servislerin durumunu gösterir.
"""

import logging
from bot_ui.keyboards import back_keyboard
from services.status_service import get_status

logger = logging.getLogger(__name__)


def status_menu():
    """
    Bot durumunu gösterir.
    
    Returns:
        tuple: (text, keyboard)
    """
    try:
        status = get_status()
        
        # Status bilgilerini kontrol et
        telegram = "🟢 Online" if status.get("telegram", False) else "🔴 Offline"
        binance = "🟢 Hazır" if status.get("binance", False) else "🔴 Bağlı Değil"
        scanner = "🟢 Çalışıyor" if status.get("scanner", False) else "🟡 Bekliyor"
        database = "🟢 Hazır" if status.get("database", False) else "🔴 Hata"
        
        # System bilgilerini al
        cpu = status.get("cpu", "N/A")
        ram = status.get("ram", "N/A")
        uptime = status.get("uptime", "N/A")
        
        text = f"""
📊 BOT DURUMU

━━━━━━━━━━━━━━━━━━

🤖 Telegram : {telegram}

📡 Binance : {binance}

📊 Scanner : {scanner}

💾 Database : {database}

━━━━━━━━━━━━━━━━━━

💻 CPU : {cpu}

🧠 RAM : {ram}

⏱ Uptime : {uptime}

━━━━━━━━━━━━━━━━━━
"""

        return text, back_keyboard()

    except Exception as e:
        logger.error(f"❌ Error in status_menu: {e}")
        error_text = "❌ Durum bilgisi yüklenemedi. Lütfen tekrar deneyin."
        return error_text, back_keyboard()
