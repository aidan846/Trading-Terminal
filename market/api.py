from ..core.positions import *
import yfinance as yf

def download_portfolio_data():
    tickers = get_tickers()
    
    data = yf.download(tickers, period="1d", interval="1m")

    return data