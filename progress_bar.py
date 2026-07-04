def build_progress_bar(progress):

    progress = max(0, min(progress, 100))

    filled = int(progress / 10)

    chars = []

    for i in range(10):

        if i < filled:
            chars.append("█")
        else:
            chars.append("░")

    chars[2] = "1"
    chars[5] = "2"
    chars[8] = "3"

    return "".join(chars)


def calculate_progress(signal, entry, tp3, current_price):

    if signal == "BUY":

        total = tp3 - entry
        current = current_price - entry

    else:

        total = entry - tp3
        current = entry - current_price

    if total <= 0:
        return 0

    progress = (current / total) * 100

    progress = max(0, min(progress, 100))

    return progress


def build_progress(signal, entry, tp3, current_price):

    progress = calculate_progress(
        signal,
        entry,
        tp3,
        current_price
    )

    return build_progress_bar(progress)