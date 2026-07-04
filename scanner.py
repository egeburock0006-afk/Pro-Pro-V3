"""
FollowLine Pro AI V3

Scanner Engine
"""
from multiprocessing.resource_sharer import stop
import time
from helpers.telegram_formatter import format_new_signal
from unittest import result
from indicators.macd import macd
from database.tables import signals
from utils.mfi import mfi
from services.binance_service import get_klines
from services.binance_service import get_futures_symbols
from strategies.alphatrend import AlphaTrend
from utils.indicators import ema
from utils.indicators import atr
from services.telegram_service import send_message
from database.signal_db import get_last_signal, save_signal
from database.trade_db import save_trade
from ai.score import calculate_ai_score
from indicators.adx import adx
from config import BINANCE_API_KEY, BINANCE_API_SECRET
from config import INTERVAL, TRADE_MARGIN, LEVERAGE
from datetime import datetime
from core.dashboard import build_dashboard
from services.telegram_service import update_dashboard
from database.trade_db import has_open_trade
from bot_ui.menus.dashboard import dashboard_keyboard
from core.score_engine import calculate_score
from core.decision_engine import choose_best_signal
from helpers.telegram_formatter import format_trade_card





def scan_symbol(symbol):

    print(f"🔍 Taranıyor : {symbol}")

    
    if has_open_trade(symbol):
         print(f"{symbol} -> OPEN TRADE VAR")
         return
    
    
    
    
    df = get_klines(
        symbol=symbol,
        interval=INTERVAL
        )



    if df is None:
        return {
            "signal": None
        }

    df["EMA200"] = ema(df["close"], 200)

    df["ATR14"] = atr(df, 14)
    
    df["MFI"] = mfi(df)
    macd_line, signal_line, histogram = macd(df["close"])
    df["MACD"] = macd_line
    df["MACD_SIGNAL"] = signal_line
    df["MACD_HIST"] = histogram
    df["ADX"] = adx(df)
    alpha = AlphaTrend()

    result = alpha.last_signal(df)
    if result is None:
        return None
    price = result["price"]
    ema200 = df["EMA200"].iloc[-1]
    mfi_value = df["MFI"].iloc[-1]
    adx_value = df["ADX"].iloc[-1]
    macd_value = df["MACD"].iloc[-1]
    macd_signal = df["MACD_SIGNAL"].iloc[-1]
    trend_ok = False
    if result["signal"] == "BUY":
        trend_ok = price > ema200
    elif result["signal"] == "SELL":
        trend_ok = price < ema200
    adx_ok = adx_value >= 25
    macd_ok = False
    if result["signal"] == "BUY":
        macd_ok = macd_value > macd_signal
    else:
        macd_ok = macd_value < macd_signal
    mfi_ok = False
    if result["signal"] == "BUY":
        mfi_ok = 55 <= mfi_value <= 75
    else:
        mfi_ok = 25 <= mfi_value <= 45
    if not trend_ok:
        return {"signal": None}
    if not adx_ok:
        return {"signal": None}
    if not macd_ok:
        return {"signal": None}
    if not mfi_ok:
        return {"signal": None}
    
    quality = 0

    if trend_ok:
        quality += 25
        
    if adx_ok:
        quality += 20   
    if macd_ok:
        quality += 20
    if mfi_ok:
        quality += 15   
    if result["strength"] >= 70:
        quality += 20 
    elif result["strength"] >= 50:
        quality += 15
    elif result["strength"] >= 30:
        quality += 10
    print(f"⭐ Trade Quality : {quality}/100")




    ai_score = calculate_ai_score(
        result,
        df["EMA200"].iloc[-1],
        result["price"],
        df["MFI"].iloc[-1],
        df["MACD"].iloc[-1],
        df["ADX"].iloc[-1]
    )

    print("\n==============================")
    print("AlphaTrend")
    print("==============================")
    print(result)
    print(f"🤖 AI Score : {ai_score}/100")
    print(f"MACD : {df['MACD'].iloc[-1]:.4f}")
    if result["signal"]:

        last_signal = get_last_signal(symbol)

        if last_signal != result["signal"]:
            entry = result["price"]

            if result["signal"] == "BUY":

                tp1 = entry + result["atr"] * 2
                tp2 = entry + result["atr"] * 4
                tp3 = entry + result["atr"] * 6
                stop = entry - result["atr"] * 2

            else:

                tp1 = entry - result["atr"] * 2
                tp2 = entry - result["atr"] * 4
                tp3 = entry - result["atr"] * 6
                stop = entry + result["atr"] * 2



            if has_open_trade(symbol):
                print(f"{symbol} -> OPEN TRADE VAR")
                return {"signal": None}

            
            
            
            
            
            
            
            
            
            
            
            print(f"🟢 Yeni Sinyal : {symbol} -> {result['signal']}")
            price = result["price"]
            atr_value = result["atr"]
            if result["signal"] == "BUY":

                sl = round(price - atr_value * 2, 5)
                tp1 = round(price + atr_value * 2, 5)

                tp2 = round(price + atr_value * 4, 5)

                tp3 = round(price + atr_value * 6, 5)

            else:

                sl = round(price + atr_value * 2, 5)

                tp1 = round(price - atr_value * 2, 5)

                tp2 = round(price - atr_value * 4, 5)

                tp3 = round(price - atr_value * 6, 5)
            
            
            emoji = "🟢" if result["signal"] == "BUY" else "🔴"

            signal_time = datetime.now().strftime("%H:%M:%S")

            send_message(
                format_trade_card(best_signal)
            )

            
               
    

    print(f"📊 Mum Sayısı : {len(df)}")

    print(f"İlk Close : {df['close'].iloc[0]}")

    print(f"Son Close : {df['close'].iloc[-1]}")

    print(f"📈 EMA200 : {df['EMA200'].iloc[-1]:.2f}")

    print(f"📊 ATR14 : {df['ATR14'].iloc[-1]:.4f}")

    print(f"MFI : {df['MFI'].iloc[-1]:.2f}")
    
    return {
        "signal": result["signal"],
        "strength": result["strength"],
        "entry": entry,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "stop": stop,
        "price": result["price"],
        "atr": result["atr"]
    }
    
    
    
    
    
    
    

def start_scan():

    print("🚀 FollowLine Pro AI V3 Başlatıldı")

    while True:
        from database.trade_db import get_open_trades
        if len(get_open_trades()) > 0:
            print("🟡 Açık işlem var. Yeni sinyal aranmayacak.")
            time.sleep(30)
            continue
        update_dashboard(
            build_dashboard(),
            dashboard_keyboard()
            )
        
        
        
        
        
        
        
        
        
        
        

        
        
        update_dashboard(

        build_dashboard(),

        dashboard_keyboard()

        )

        print("\n🔍 Yeni Tarama Başladı...\n")

        symbols = get_futures_symbols()

        print(f"📈 Toplam Coin : {len(symbols)}")

        signals = []

        for symbol in symbols:

            result = scan_symbol(symbol)

            if result is None:
                continue
            if result["signal"] is None:
                continue
            score = calculate_score(result)
            result["symbol"] = symbol
            result["score"] = score
            
            signals.append(result)
                
            score = calculate_score(result)            
                
            
                   
              
                
                
        best_signal = choose_best_signal(signals)
        if best_signal is None:
            print("❌ Uygun işlem bulunamadı.")
        else:
            print("\n🏆 EN İYİ İŞLEM")
            print(best_signal)
        
        if not has_open_trade(best_signal["symbol"]):
            save_trade(                
                best_signal["symbol"],
                best_signal["signal"],
                best_signal["entry"],
                best_signal["tp1"],
                best_signal["tp2"],
                best_signal["tp3"],
                best_signal["stop"]
            )
            
               

        print(f"✅ TRADE OPENED -> {best_signal['symbol']}")
        save_signal(

    best_signal["symbol"],
    best_signal["signal"]

)
        
        
        
        
        
        
        
        
                
                                                            
        if not has_open_trade(best_signal["symbol"]):                                                                  
                
            
            
            
         
            print("\n" + "=" * 50)
        print("✅ Tarama Tamamlandı")
        print(f"📊 Bulunan Sinyal : {len(signals)}")
        print("=" * 50)

        print("\n⏳ 30 saniye bekleniyor...\n")

        time.sleep(60)
        
        
        
        
        
        

        
        
        
        
        
        

    
        
    print()
    print("=" * 50)
    print("BULUNAN SİNYALLER")
    print("=" * 50)
    
    for s in signals:
        print(
            f"{s['symbol']} | "
            f"{s['signal']} | "
            f"Strength: {s['strength']}"
        )
        
    print()
    print(f"Toplam Sinyal : {len(signals)}")


        
        