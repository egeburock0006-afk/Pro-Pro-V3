"""
Telegram Bot - Cüzdan Menüsü

Kullanıcı bakiyesini gösterir.
"""

import logging
from bot_ui.keyboards import back_keyboard
from database.wallet_db import get_wallet
from core.stats_engine import get_stats

logger = logging.getLogger(__name__)


def wallet_menu():
    """
    Cüzdan bilgilerini gösterir.
    
    Returns:
        tuple: (text, keyboard)
    """
    try:
        wallet = get_wallet()
        stats = get_stats()
        
        # Wallet güvenli dönüşümü
        try:
            balance = float(wallet) if wallet else 0.0
        except (ValueError, TypeError):
            balance = 0.0
            logger.warning("⚠️ Wallet değeri dönüştürülemedi, 0.0 kullanılıyor")
        
        # Stats bilgilerini al
        profit = stats.get("profit", 0.0)
        roi = stats.get("roi", 0.0)
        win_rate = stats.get("win_rate", 0.0)
        
        text = f"""
💰 WALLET

━━━━━━━━━━━━━━━━━━

💵 Balance

{balance:.2f}$

━━━━━━━━━━━━━━━━━━

📈 Profit

{profit:.2f}$

📊 ROI

{roi:.2f}%

🏆 Win Rate

{win_rate:.2f}%

━━━━━━━━━━━━━━━━━━
"""

        return text, back_keyboard()

    except Exception as e:
        logger.error(f"❌ Error in wallet_menu: {e}")
        error_text = "❌ Cüzdan bilgisi yüklenemedi. Lütfen tekrar deneyin."
        return error_text, back_keyboard()
