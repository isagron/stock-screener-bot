import yfinance as yf
import numpy as np
from enum import Enum


class Trend(Enum):
    UP = "up"
    DOWN = "down"


class StockData:
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.last_close = None
        self.last_volume = None
        self.avg_volume_150 = None
        self.last_150_days = []
        self.avg_150_today = None
        self.avg_150_yesterday = None
        self.trend = None
        self.rsi = None

        self._fetch_stock_data()

    def _fetch_stock_data(self):
        """
        Fetch stock data for the last 150 days and compute required fields.
        """
        try:
            stock = yf.Ticker(self.symbol)
            history = stock.history(period="151d")  # Fetch 151 days to get yesterday’s avg

            if len(history) < 150:
                raise ValueError("Not enough historical data available.")

            self.last_close = history["Close"].iloc[-1]
            self.last_volume = history["Volume"].iloc[-1]
            self.last_150_days = list(history["Close"].iloc[-150:])  # Last 150 closing prices

            self.avg_150_today = np.mean(self.last_150_days)
            self.avg_150_yesterday = np.mean(history["Close"].iloc[-151:-1])  # Previous 150 days

            self.avg_volume_150 = np.mean(history["Volume"].iloc[-150:])  # Compute average volume

            self.trend = Trend.UP if self.avg_150_today > self.avg_150_yesterday else Trend.DOWN

            rsi = self._calculate_rsi()

            if rsi is not None:
                self.rsi = float(rsi.iloc[0])

        except Exception as e:
            print(f"Error fetching data for {self.symbol}: {e}")

    def _calculate_rsi(self, period=14):
        """
        Fetches historical stock data and calculates the RSI for the given stock symbol.

        :param symbol: Stock ticker symbol (e.g., "AAPL" for Apple)
        :param period: Number of days to calculate RSI (default is 14)
        :return: The latest RSI value (float) or None if calculation fails
        """
        try:
            # Fetch last 150 days of stock data
            stock_data = yf.download(self.symbol, period="150d", interval="1d")

            if stock_data.empty or "Close" not in stock_data.columns:
                print(f"⚠️ No data found for {self.symbol}")
                return None

            # Calculate daily price changes
            delta = stock_data["Close"].diff()

            # Separate gains and losses
            gains = delta.where(delta > 0, 0)
            losses = -delta.where(delta < 0, 0)

            # Calculate average gain and average loss over the period
            avg_gain = gains.rolling(window=period, min_periods=1).mean()
            avg_loss = losses.rolling(window=period, min_periods=1).mean()

            # Compute Relative Strength (RS) and RSI
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            # Return the most recent RSI value
            return round(rsi.iloc[-1], 2)

        except Exception as e:
            print(f"⚠️ Error calculating RSI for {self.symbol}: {e}")
            return None

    def __repr__(self):
        return (f"StockData(symbol={self.symbol}, last_close={self.last_close}, "
                f"avg_150_today={self.avg_150_today}, avg_150_yesterday={self.avg_150_yesterday}, "
                f"avg_volume={self.avg_volume_150}, trend={self.trend}, rsi={self.rsi})")
