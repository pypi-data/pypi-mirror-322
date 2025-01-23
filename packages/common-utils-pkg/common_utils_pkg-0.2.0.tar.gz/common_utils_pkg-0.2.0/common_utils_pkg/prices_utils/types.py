from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class MarketTypeEnum(str, Enum):
    SPOT = "spot"
    FUTURES = "futures"


class SymbolInfo(BaseModel):
    symbol: str
    first_data_date: datetime | None
    last_loaded_data_date: datetime | None
    is_spot_finished: bool

    first_futures_data_date: datetime | None
    last_loaded_futures_data_date: datetime | None
    is_futures_finished: bool


class SkippedDay(BaseModel):
    symbol: str
    type: MarketTypeEnum
    date: datetime


class TickTrade(BaseModel):
    time: datetime
    symbol: str
    price: float
    quantity: float


class Kline(BaseModel):
    symbol: str
    date: float
    open: float
    high: float
    low: float
    close: float
    volume: float


class Funding(BaseModel):
    symbol: str
    time: datetime
    funding: float
    mark_price: float | None


class PremiumIndexKline(BaseModel):
    symbol: str
    time: datetime
    open: float
    high: float
    low: float
    close: float


class SymbolVolatility(BaseModel):
    symbol: str
    date: datetime
    long_trades: int
    short_trades: int
    last_level_price: float | None
