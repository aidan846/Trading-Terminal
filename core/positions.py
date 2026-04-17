from ..market.api import *

import json

def get_portfolio_data():
    with open("data/positions.json", "r") as f:
        data = json.load(f)
    return data["portfolio"]

def get_cash():
    return get_portfolio_data()["uninvested_cash"]

def get_positions():
    return get_portfolio_data()["positions"]

def get_tickers():
    return [position["ticker"] for position in get_positions()]


def update_positions():
    portfolio_data = get_portfolio_data()

    new_data = download_portfolio_data()

    for position in portfolio_data["positions"]:
        ticker = position["ticker"]
        shares = position["shares"]
        avg_price = position["avg_price"]
        current_price = position["current_price"]
        daily_pl = position["daily_pl"]
        open_pl = position["open_pl"]


        new_current_price = new_data["Close"][ticker][-1]
        prev_close = new_data["Close"][ticker][-2]

        new_daily_pl = (new_current_price - prev_close) * shares
        new_open_pl = (new_current_price - avg_price) * shares

        position["current_price"] = round(float(new_current_price), 2)
        position["daily_pl"] = round(float(new_daily_pl), 2)
        position["open_pl"] = round(float(new_open_pl), 2)

    with open('data/portfolio.json', 'w') as f:
        json.dump(portfolio_data, f, indent=4)
    
    return portfolio_data