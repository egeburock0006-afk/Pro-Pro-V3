"""
Trade Engine

Trade hesaplamalarını yapar (ROI, profit, vb).
"""

import logging
from database.wallet_db import get_wallet, update_wallet

logger = logging.getLogger(__name__)


def calculate_roi(entry, exit_price, signal, leverage):
    """
    ROI (Return on Investment) hesaplar.
    
    Args:
        entry (float): Entry fiyatı
        exit_price (float): Exit fiyatı
        signal (str): "BUY" ya da "SELL"
        leverage (float): Kaldıraç
    
    Returns:
        float: ROI yüzdesi
    """
    try:
        if entry == 0:
            return 0
        
        if signal == "BUY":
            roi = ((exit_price - entry) / entry) * leverage * 100
        else:  # SELL
            roi = ((entry - exit_price) / entry) * leverage * 100
        
        return round(roi, 2)
    
    except Exception as e:
        logger.error(f"❌ Error calculating ROI: {e}")
        return 0


def calculate_profit(entry, exit_price, margin, leverage, signal):
    """
    Kar/zarar miktarını hesaplar (USDT).
    
    Args:
        entry (float): Entry fiyatı
        exit_price (float): Exit fiyatı
        margin (float): Margin miktarı
        leverage (float): Kaldıraç
        signal (str): "BUY" ya da "SELL"
    
    Returns:
        float: Kar/zarar miktarı
    """
    try:
        roi = calculate_roi(entry, exit_price, signal, leverage)
        profit = margin * (roi / 100)
        return round(profit, 2)
    
    except Exception as e:
        logger.error(f"❌ Error calculating profit: {e}")
        return 0


def update_wallet_profit(profit):
    """
    Wallet'e kar/zarar ekler.
    
    Args:
        profit (float): Kar/zarar miktarı
    
    Returns:
        float: Yeni wallet miktarı
    """
    try:
        wallet = get_wallet()
        wallet += profit
        update_wallet(wallet)
        logger.info(f"Wallet updated: +{profit}$ -> {wallet}$")
        return wallet
    
    except Exception as e:
        logger.error(f"❌ Error updating wallet: {e}")
        return 0
