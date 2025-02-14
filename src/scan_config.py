from enum import Enum

from src.stock_data import Trend


class Strategy(Enum):
    MIN_PRICE = "min_price"
    MIN_VOLUME = "min_volume"
    TREND = "trend"
    DIFF_150_AVG = "diff_150_avg"
    MAX_RSI = "max_rsi"


class ScanConfig:
    def __init__(self, min_price=10, diff_150_avg=3, trend=Trend.UP, max_rsi=30, min_avg_volume=1_000_000, strategies=None):
        self.min_price = min_price
        self.diff_150_avg = diff_150_avg
        self.trend = trend
        self.max_rsi = max_rsi
        self.min_avg_volume = min_avg_volume
        if strategies is None:
            strategies = [Strategy.MIN_PRICE, Strategy.MIN_VOLUME, Strategy.TREND, Strategy.DIFF_150_AVG,
                          Strategy.MAX_RSI]
        self.strategies = strategies
