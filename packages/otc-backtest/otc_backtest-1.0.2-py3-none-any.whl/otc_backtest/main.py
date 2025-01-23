from .utils import generate_contracts
import pandas as pd
import datetime

contract = {
    'structure' : "bonus_snowball", 
    'underlying':"000852.SH",
    'principal' : 10000000,
    'tenor' : "24M",
    'lock_period' : "3M",
    'knock out barrier': 1.0,
    'knock in barrier': 0.7,
    'coupon' : 0.25,
    'stepdown': 0.005, #非必须，默认0
    'maturity coupon': 0.2, #非必须，默认 = coupon
    'bonus period': "1Y", #非必须
    'secondary coupon': 0.05, #非必须
}

trade_dates = pd.Series([datetime.date(2024, 1, 9)])
underlying_prices = pd.Series(6000)
trade_book = 'simulation.csv'

generate_contracts(contract,trade_dates,underlying_prices,trade_book)