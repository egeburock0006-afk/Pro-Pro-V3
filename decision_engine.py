def choose_best_signal(signals):

    if len(signals) == 0:
        return None

    # En düşük puanlıları ele
    candidates = [
        s for s in signals
        if s["score"] >= 85
    ]

    if len(candidates) == 0:
        return None

    # En yüksek skoru seç
    best = max(
        candidates,
        key=lambda x: x["score"]
    )

    return best