"""
Telegram Bot - Açık İşlemler Menüsü

Aktif işlemleri gösterir.
"""

import logging
from bot_ui.keyboards import back_keyboard, trades_keyboard
from database.trade_db import get_open_trades
from services.binance_service import get_price
from core.progress_bar import build_progress

logger = logging.getLogger(__name__)

# Geçerli Binance sembollerinin listesi
VALID_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'SOLUSDT', 'DOGEUSDT']


def is_valid_symbol(symbol):
    """Sembolün geçerli olup olmadığını kontrol et"""
    if not symbol or symbol == "INIT" or not isinstance(symbol, str):
        return False
    return True


def trades_menu():
    """
    Açık işlemleri menü formatında gösterir.
    
    Returns:
        tuple: (text, keyboard)
    """
    try:
        # Tüm açık işlemleri bir kez al
        all_trades = get_open_trades()
        
        if not all_trades:
            text = """
📈 OPEN TRADES

━━━━━━━━━━━━━━━━━━

Şu anda açık işlem yok.

━━━━━━━━━━━━━━━━━━
"""
            return text, back_keyboard()

        # Son 10 işlemi göster
        trades = all_trades[-10:]
        total_trades = len(all_trades)

        text = "📈 OPEN TRADES\n\n━━━━━━━━━━━━━━━━━━\n\n"
        valid_trades = []

        for trade in trades:
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

                # Geçersiz sembolü kontrol et
                if not is_valid_symbol(symbol):
                    logger.warning(f"⚠️ Geçersiz sembol atlanıyor: {symbol}")
                    continue

                # Sıfır değerleri kontrol et
                if entry == 0.0 or tp3 == 0.0:
                    logger.warning(f"⚠️ {symbol} için sıfır değerler, atlanıyor (entry: {entry}, tp3: {tp3})")
                    continue

                # Güncel fiyat al
                try:
                    current_price = float(get_price(symbol))
                except (ValueError, TypeError, Exception) as price_error:
                    logger.warning(f"⚠️ {symbol} fiyatı alınamadı: {price_error}")
                    current_price = entry

                # Progress bar oluştur
                try:
                    bar = build_progress(
                        signal,
                        entry,
                        tp3,
                        current_price
                    )
                except Exception as bar_error:
                    logger.warning(f"⚠️ Progress bar hatası {symbol}: {bar_error}")
                    bar = "⚠️ Progress Bar Hatası"

                emoji = "🟢" if signal == "BUY" else "🔴"
                direction = "LONG" if signal == "BUY" else "SHORT"

                text += (
                    f"{emoji} {symbol}    {direction}\n"
                    f"Entry: {entry:.4f} | TP3: {tp3:.4f} | Current: {current_price}\n\n"
                    f"{bar}\n\n"
                    "━━━━━━━━━━━━━━━━━━\n\n"
                )
                
                # Geçerli trade'i listele
                valid_trades.append(trade)

            except ValueError as ve:
                logger.error(f"❌ Trade parse hatası: {ve}")
                continue
            except Exception as e:
                logger.error(f"❌ Trade işleme hatası: {e}")
                continue

        # Hiç geçerli trade yoksa
        if not valid_trades:
            text = """
📈 OPEN TRADES

━━━━━━━━━━━━━━━━━━

⚠️ Geçerli açık işlem yok.

━━━━━━━━━━━━━━━━━━
"""
            return text, back_keyboard()

        if total_trades > 10:
            text += f"\n📌 Toplam Açık İşlem: {total_trades}"

        return text, trades_keyboard(valid_trades)

    except Exception as e:
        logger.error(f"❌ Error in trades_menu: {e}")
        error_text = "❌ İşlemler yüklenemedi. Lütfen tekrar deneyin."
        return error_text, back_keyboard()
