from src.scan_config import ScanConfig, Strategy
from src.stock_data import StockData
from src.stock_list import sp500, russell2000, custom

sp_index_name = "S&P"
russel_index_name = "Russell"
custom_index_name = "Custom"


stock_dict = {
    sp_index_name: sp500,
    russel_index_name: russell2000,
    custom_index_name: custom
}




def is_price_higher_then(ticker_data: StockData, scan_config: ScanConfig):
    return ticker_data.last_close is not None and ticker_data.last_close > scan_config.min_price


def is_volume_higher_then(ticker_data: StockData, scan_config: ScanConfig):
    return ticker_data.avg_volume_150 > scan_config.min_avg_volume


def is_trend(ticker_data: StockData, scan_config: ScanConfig):
    return ticker_data.trend == scan_config.trend


def is_diff_from_150avg_less(ticker_data: StockData, scan_config: ScanConfig):
    diff_percentage = ((
                               ticker_data.last_close - ticker_data.avg_150_today) / ticker_data.avg_150_today) * 100
    return diff_percentage <= scan_config.diff_150_avg


def is_rsi_less_than(ticker_data: StockData, scan_config: ScanConfig):
    return ticker_data.rsi <= scan_config.max_rsi

STRATEGY_FUNCTIONS = {
    Strategy.MIN_PRICE: is_price_higher_then,
    Strategy.MIN_VOLUME: is_volume_higher_then,
    Strategy.TREND: is_trend,
    Strategy.DIFF_150_AVG: is_diff_from_150avg_less,
    Strategy.MAX_RSI: is_rsi_less_than,
}

def evaluate_stock(stock_data: StockData, scan_config: ScanConfig = None):
    return all(STRATEGY_FUNCTIONS[strategy](stock_data, scan_config) for strategy in scan_config.strategies if
               strategy in STRATEGY_FUNCTIONS)

def find_stocks(stock_index=None, scan_config: ScanConfig = None):
    if scan_config is None:
        scan_config = ScanConfig()
    if stock_index is None:
        stock_index = [sp_index_name]
    tickers = []
    for i in stock_index:
        tickers.extend(stock_dict.get(i))

    results = []
    retry_delay = 1
    for ticker in tickers:
        ticker_data = StockData(ticker)
        print(f"Checking stock: {ticker}")
        try:
            if evaluate_stock(ticker_data, scan_config):
                print(f"Add: {ticker} to the list")
                results.append(ticker_data)



        except Exception as e:
            print(f"⚠️ Error processing {ticker}: {e}")
            time.sleep(retry_delay)
            retry_delay *= 2

    return results