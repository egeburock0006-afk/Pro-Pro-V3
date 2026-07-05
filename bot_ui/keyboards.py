"""
Telegram Bot Keyboard Layouts

Bu modül bot için inline keyboard'ları tanımlar.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Callback data sabitleri
CALLBACK_DASHBOARD = "dashboard"
CALLBACK_WALLET = "wallet"
CALLBACK_TRADES = "trades"
CALLBACK_WATCHLIST = "watchlist"
CALLBACK_RANKING = "ranking"
CALLBACK_SIGNALS = "signals"
CALLBACK_SETTINGS = "settings"
CALLBACK_HOME = "home"


def dashboard_keyboard():
    """
    Ana dashboard menüsü keyboard'ını döndürür.
    
    Returns:
        InlineKeyboardMarkup: Dashboard menüsü
    """
    keyboard = [
        [InlineKeyboardButton("📊 Dashboard", callback_data=CALLBACK_DASHBOARD)],
        [InlineKeyboardButton("💰 Wallet", callback_data=CALLBACK_WALLET)],
        [InlineKeyboardButton("📈 Açık İşlemler", callback_data=CALLBACK_TRADES)],
        [InlineKeyboardButton("👀 Watchlist", callback_data=CALLBACK_WATCHLIST)],
        [InlineKeyboardButton("🏆 AI Ranking", callback_data=CALLBACK_RANKING)],
        [InlineKeyboardButton("📋 Son Sinyaller", callback_data=CALLBACK_SIGNALS)],
        [InlineKeyboardButton("⚙️ Ayarlar", callback_data=CALLBACK_SETTINGS)],
    ]

    return InlineKeyboardMarkup(keyboard)


def back_keyboard():
    """
    Geri dön (Ana Menü) butonunu döndürür.
    
    Returns:
        InlineKeyboardMarkup: Geri dön butonu
    """
    keyboard = [
        [InlineKeyboardButton("⬅️ Ana Menü", callback_data=CALLBACK_HOME)]
    ]

    return InlineKeyboardMarkup(keyboard)


def settings_keyboard():
    """
    Ayarlar menüsü keyboard'ını döndürür.
    
    Returns:
        InlineKeyboardMarkup: Ayarlar menüsü
    """
    keyboard = [
        [InlineKeyboardButton("🔔 Bildirimler", callback_data="settings_notifications")],
        [InlineKeyboardButton("📱 Profil", callback_data="settings_profile")],
        [InlineKeyboardButton("🔐 Güvenlik", callback_data="settings_security")],
        [InlineKeyboardButton("⬅️ Geri", callback_data=CALLBACK_HOME)],
    ]

    return InlineKeyboardMarkup(keyboard)


def confirm_keyboard(action_data):
    """
    Onay/İptal keyboard'ını döndürür.
    
    Args:
        action_data (str): Onaylanacak işlemin callback verisi
    
    Returns:
        InlineKeyboardMarkup: Evet/Hayır seçeneği
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Evet", callback_data=f"confirm_{action_data}"),
            InlineKeyboardButton("❌ İptal", callback_data=CALLBACK_HOME),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def trades_keyboard(trades):
    """
    Trades menüsü için inline keyboard
    
    Args:
        trades (list): İşlemler listesi. Her trade tuple formatında:
                      (trade_id, symbol, signal, entry, tp1, tp2, tp3, stop, ...)
    
    Returns:
        InlineKeyboardMarkup: Trades keyboard'ı
    """
    keyboard = []
    
    # Her trade için buton ekle (maksimum 10 trade göster)
    if trades:
        for trade in trades:
            try:
                trade_id = trade[0]  # trade_id
                symbol = trade[1]    # symbol (örn: BTCUSDT)
                signal = trade[2]    # BUY veya SHORT
                
                # Emoji ve yön
                emoji = "🟢" if signal == "BUY" else "🔴"
                direction = "LONG" if signal == "BUY" else "SHORT"
                
                # Buton metni ve callback
                button_text = f"{emoji} {symbol} {direction}"
                callback = f"trade_detail_{trade_id}"
                
                keyboard.append([InlineKeyboardButton(button_text, callback_data=callback)])
            
            except (IndexError, TypeError):
                # Geçersiz trade formatı, atla
                continue
    
    # Geri butonu
    keyboard.append([InlineKeyboardButton("⬅️ Ana Menü", callback_data=CALLBACK_HOME)])
    
    return InlineKeyboardMarkup(keyboard)


def trade_detail_keyboard(trade_id):
    """
    Tek trade detayı için keyboard
    
    Args:
        trade_id (int): Trade ID
    
    Returns:
        InlineKeyboardMarkup: Trade detay keyboard'ı
    """
    keyboard = [
        [InlineKeyboardButton("📊 Grafik", callback_data=f"trade_chart_{trade_id}")],
        [InlineKeyboardButton("❌ Kapat", callback_data=f"trade_close_{trade_id}")],
        [InlineKeyboardButton("⬅️ Geri", callback_data=CALLBACK_TRADES)],
    ]
    
    return InlineKeyboardMarkup(keyboard)
