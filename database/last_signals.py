"""
Last Signals Model

Son sinyalleri saklar ve yönetir.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base:
    """Base model class"""
    pass


class LastSignal(Base):
    """
    Son yapılan sinyalleri saklar.
    
    Attributes:
        symbol (str): Sembol adı (örn: BTCUSDT) - Primary Key
        signal (str): Sinyal türü ("BUY" ya da "SELL")
    """

    __tablename__ = "last_signals"

    symbol: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        nullable=False,
        doc="Sembol adı"
    )

    signal: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        doc="BUY ya da SELL"
    )

    def __repr__(self) -> str:
        return f"<LastSignal(symbol={self.symbol}, signal={self.signal})>"
