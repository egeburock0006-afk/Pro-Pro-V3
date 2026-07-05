"""
Dashboard Engine

Dashboard mesajını oluşturur.
"""

from datetime import datetime
from database.wallet_db import get_wallet
from core.stats_engine import get_stats


def build_dashboard():
    """
    Bot dashboard mesajını oluşturur.
    
    Returns:
        str: Formatted dashboard mesajı
    """
    try:
        stats = get_stats()
        now = datetime.now().strftime("%H:%M:%S")

        text = f"""
🤖 FOLLOWLINE PRO AI V4

━━━━━━━━━━━━━━━━━━

🟢 Status : ONLINE

💰 Wallet : {stats.get('wallet', 0):.2f}$

📈 Open Trades : {stats.get('open_trades', 0)}

🎯 TP1 : {stats.get('tp1', 0)}
🚀 TP2 : {stats.get('tp2', 0)}
🏆 TP3 : {stats.get('tp3', 0)}
🛑 STOP : {stats.get('stop', 0)}

📊 Win Rate : {stats.get('win_rate', 0)}%

👀 Watching : {len([])} symbols

⏱ Interval : 5M

🕒 Updated : {now}
"""
        return text
    
    except Exception as e:
        print(f"❌ Error building dashboard: {e}")
        return "❌ Dashboard oluşturulamadı"
