import threading
import threading

from colorama import init
from database.wallet_db import create_wallet
from database.schema import create_database
from bot_ui.bot import application
from bot_ui.handlers import register_handlers
from core.dashboard import build_dashboard
from services.telegram_service import send_dashboard
from bot_ui.menus.dashboard import dashboard_text, dashboard_keyboard
from core.trade_monitor import start_trade_monitor
from database.trade_db import save_trade
from core.test_engine import get_wallet
from core.test_engine import (
    get_wallet,
    update_balance,
    get_stats,
    get_position_size,
)



from core.scanner import start_scan
from services.binance_service import get_klines
from strategies.alphatrend import AlphaTrend

alpha = AlphaTrend()
df = get_klines(
    symbol="BTCUSDT",
    interval="5m",
    limit=200,
)

alpha = AlphaTrend()
result = alpha.last_signal(df)
print("===================================")
print("AlphaTrend Sonucu")
print("===================================")

print(f"Signal      : {result['signal']}")
print(f"Direction   : {result['direction']}")
print(f"Close       : {result['price']}")
print(f"AlphaTrend  : {result['alphatrend']}")
print(f"ATR         : {result['atr']}")
print(f"MFI         : {result['mfi']}")
data = alpha.calculate(df)

signals = data[
    (data["buy"] == True) |
    (data["sell"] == True)
]

print(signals[
    [
        "close",
        "AlphaTrend",
        "Trigger",
        "buy",
        "sell",
        "direction"
    ]
].tail(20))

print()

print("BUY SAYISI :", data["buy"].sum())
print("SELL SAYISI:", data["sell"].sum())






init()

print("=" * 60)
print("🤖 FollowLine Pro AI V3")
print("=" * 60)
print("Telegram başlatılıyor...")

register_handlers(application)

print("✅ Handlerlar yüklendi")
print("🚀 Bot çalışıyor...")

print("📦 Database hazırlanıyor...")
create_database()
create_wallet()
print("=" * 50)
print("🧪 TEST ENGINE")
print(f"Wallet : {get_wallet()} USDT")
print(f"Position Size : {get_position_size()} USDT")
print("=" * 50)




    # Trades tablosunu oluştur
try:
        save_trade(
            
            "BUY",
            0,
            0,
            0,
            0,
            0
        )
except:
        pass
    
from database.trade_db import close_trade
try:
    close_trade(1, "INIT", 0, 0)
except:
    pass              
            
            
            

print("✅ Database hazır")
klines = get_klines("BTCUSDT")

print(f"📊 BTCUSDT Mum Sayısı : {len(klines)}")

scan_thread = threading.Thread(
    target=start_scan,
    daemon=True
)

monitor_thread = threading.Thread(
    target=start_trade_monitor,
    daemon=True
)

monitor_thread.start()

scan_thread.start()



print("📲 Dashboard Telegram'a gönderiliyor...")

send_dashboard(

    dashboard_text(),

    dashboard_keyboard()

)

print("✅ Dashboard gönderildi")

application.run_polling()