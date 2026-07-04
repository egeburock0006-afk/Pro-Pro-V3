import pandas as pd


def calculate_score(df, signal):

    score = 0

    last = df.iloc[-1]

    # -------------------------
    # 1) Yeni AlphaTrend sinyali
    # -------------------------

    if signal in ("BUY", "SELL"):
        score += 40

    # -------------------------
    # 2) ATR yüksek mi?
    # -------------------------

    atr = last["ATR"]

    atr_mean = df["ATR"].tail(20).mean()

    if atr > atr_mean:
        score += 20

    # -------------------------
    # 3) Hacim
    # -------------------------

    volume_mean = df["volume"].tail(20).mean()

    if last["volume"] > volume_mean:
        score += 20

    # -------------------------
    # 4) Mum yönü
    # -------------------------

    if signal == "BUY":

        if last["close"] > last["open"]:
            score += 10

    else:

        if last["close"] < last["open"]:
            score += 10

    # -------------------------
    # 5) Büyük fitilli mum olmasın
    # -------------------------

    candle = abs(last["close"] - last["open"])

    full = last["high"] - last["low"]

    if full > 0:

        body_ratio = candle / full

        if body_ratio > 0.5:
            score += 10

    return round(score, 2)