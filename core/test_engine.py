"""
Test Engine

Backtest/test modunda wallet ve trade'leri yönetir.
"""

import logging

logger = logging.getLogger(__name__)

# Global test variables
_wallet = 100.0
_trade_count = 0
_max_trades = 100
_win_count = 0
_loss_count = 0


def get_wallet():
    """
    Güncel wallet değerini döndürür.
    
    Returns:
        float: Wallet miktarı
    """
    return round(_wallet, 2)


def update_balance(profit):
    """
    Wallet'e kar/zarar ekler.
    
    Args:
        profit (float): Kar/zarar miktarı
    
    Returns:
        float: Yeni wallet miktarı
    """
    global _wallet
    _wallet += profit
    logger.info(f"Balance updated: {round(_wallet, 2)}$ (profit: {profit}$)")
    return round(_wallet, 2)


def get_position_size():
    """
    Wallet'in %10'unu position size olarak döndürür.
    
    Returns:
        float: Position size
    """
    return round(_wallet * 0.10, 2)


def add_trade(win=False):
    """
    Trade sayacını artırır.
    
    Args:
        win (bool): Trade kazanıldı mı?
    """
    global _trade_count, _win_count, _loss_count
    
    _trade_count += 1
    if win:
        _win_count += 1
    else:
        _loss_count += 1
    
    logger.info(f"Trade added: {_trade_count}/{_max_trades} (W: {_win_count}, L: {_loss_count})")


def get_trade_count():
    """
    Toplam trade sayısını döndürür.
    
    Returns:
        int: Trade sayısı
    """
    return _trade_count


def get_remaining():
    """
    Kalan trade sayısını döndürür.
    
    Returns:
        int: Kalan trade sayısı
    """
    return _max_trades - _trade_count


def finished():
    """
    Test bitti mi?
    
    Returns:
        bool: True/False
    """
    return _trade_count >= _max_trades


def get_winrate():
    """
    Win rate'i hesaplar.
    
    Returns:
        float: Win rate yüzdesi
    """
    if _trade_count == 0:
        return 0
    return round((_win_count / _trade_count) * 100, 2)


def get_stats():
    """
    Test istatistiklerini döndürür.
    
    Returns:
        dict: Test stats
    """
    return {
        "wallet": round(_wallet, 2),
        "trade": _trade_count,
        "remaining": _max_trades - _trade_count,
        "wins": _win_count,
        "losses": _loss_count,
        "winrate": get_winrate(),
        "position": round(_wallet * 0.10, 2)
    }


def get_balance():
    """
    Wallet alias.
    
    Returns:
        float: Wallet miktarı
    """
    return get_wallet()
