from datetime import datetime
from database.wallet_db import get_wallet
from core.stats_engine import get_stats

def build_dashboard():

    stats = get_stats()

    now = datetime.now().strftime("%H:%M:%S")

    text = f"""
🤖 FOLLOWLINE PRO AI V4

━━━━━━━━━━━━━━━━━━

🟢 Status : ONLINE

💰 Wallet : {stats['wallet']:.2f}$

📈 Open Trades : {stats['open_trades']}

🎯 TP1 : {stats['tp1']}
🚀 TP2 : {stats['tp2']}
🏆 TP3 : {stats['tp3']}
🛑 STOP : {stats['stop']}

📊 Win Rate : {stats['win_rate']}%

👀 Watching : ...

⏱ Interval : 5M

🕒 Updated : {now}
"""

    return text