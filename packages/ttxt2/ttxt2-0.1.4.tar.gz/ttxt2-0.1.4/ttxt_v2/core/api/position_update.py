from dataclasses import dataclass
from typing import List

from .enums import ESide
from .trading_pair import TradingPair


@dataclass
class Position:
    symbol: TradingPair
    side: ESide
    size: int
    position_value: float
    entry_price: float
    position_im: float
    position_mm: float
    tp_price: float
    sl_price: float
    unrealised_pnl: float
    cur_pnl: float
    create_time: int
    update_time: int


@dataclass
class PositionUpdate:
    positions: List[Position]
    timestamp: int
