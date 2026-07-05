"""
Settings Model

Bot ayarlarını saklar ve yönetir.
"""

from sqlalchemy import Boolean, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base:
    """Base model class"""
    pass


class Settings(Base):
    """
    Bot ayarlarını saklar.
    
    Attributes:
        id (int): Primary Key - Ayarlar ID
        ai_threshold (int): AI skor eşiği (0-100)
        watchlist_threshold (int): Watchlist eşiği (0-100)
        scan_interval (int): Tarama aralığı (saniye)
        notification (bool): Bildirimleri aç/kapat
        triple_confirmation (bool): Üçlü doğrulama aç/kapat
    """

    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        doc="Settings ID"
    )

    ai_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=85,
        doc="AI skor minimum eşiği (0-100)"
    )

    watchlist_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=70,
        doc="Watchlist eşiği (0-100)"
    )

    scan_interval: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=60,
        doc="Tarama aralığı (saniye)"
    )

    notification: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Bildirimleri aç/kapat"
    )

    triple_confirmation: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Üçlü doğrulama aç/kapat"
    )

    def __repr__(self) -> str:
        return (
            f"<Settings("
            f"ai_threshold={self.ai_threshold}, "
            f"watchlist_threshold={self.watchlist_threshold}, "
            f"scan_interval={self.scan_interval}, "
            f"notification={self.notification}, "
            f"triple_confirmation={self.triple_confirmation}"
            f")>"
        )

    def to_dict(self) -> dict:
        """Ayarları sözlüğe çevir"""
        return {
            "id": self.id,
            "ai_threshold": self.ai_threshold,
            "watchlist_threshold": self.watchlist_threshold,
            "scan_interval": self.scan_interval,
            "notification": self.notification,
            "triple_confirmation": self.triple_confirmation,
        }
