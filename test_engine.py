wallet = 100.0

trade_count = 0

max_trades = 100

win_count = 0

loss_count = 0


def get_wallet():
    return round(wallet, 2)


def update_balance(profit):

    global wallet

    wallet += profit

    return round(wallet, 2)


def get_position_size():

    return round(wallet * 0.10, 2)


def add_trade(win=False):

    global trade_count
    global win_count
    global loss_count

    trade_count += 1

    if win:
        win_count += 1
    else:
        loss_count += 1


def get_trade_count():
    return trade_count


def get_remaining():
    return max_trades - trade_count


def finished():

    return trade_count >= max_trades


def get_winrate():

    if trade_count == 0:
        return 0

    return round((win_count / trade_count) * 100, 2)


def get_stats():

    return {

        "wallet": round(wallet, 2),

        "trade": trade_count,

        "remaining": max_trades - trade_count,

        "wins": win_count,

        "losses": loss_count,

        "winrate": get_winrate(),

        "position": round(wallet * 0.10, 2)

    }
    
def get_balance():
    return get_wallet()
