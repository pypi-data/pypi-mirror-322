import pandas as pd
import datetime
import fleet
import os

CALENDAR_DIR = os.path.join(os.path.dirname(__file__), "calendar/China")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SNOWBALL_CSV_PATH = os.path.join(DATA_DIR, "snowball.csv")

CALENDAR = fleet.Calendar(CALENDAR_DIR)

#需要的函数（生成观察日/敲出障碍/票息3个序列）

_PERIOD_MAP = {
    'month': fleet.TimeUnit.MONTH,
    'week': fleet.TimeUnit.WEEK,
    'day': fleet.TimeUnit.DAY,
    'year': fleet.TimeUnit.YEAR
}
    
def _to_fleet_date(date: datetime.date):
    return fleet.Date(date.year, date.month, date.day)


def _to_py_date(date: fleet.Date):
    return datetime.date(date.Year(), date.Month(), date.Day())

def schedule_dates(start_date: datetime.date, tenor:int, period: int, period_unit: str, skip: int):
    start =_to_fleet_date(start_date)
    end = fleet.Date(start.Year()+ int(tenor/12) , start.Month(), start.Day())
    if not CALENDAR.IsBusinessDay(end):
        end = CALENDAR.NextBusinessDay(end)
    fleet_output = CALENDAR.Schedule(
        start, 
        end,
        fleet.Period(period, _PERIOD_MAP[period_unit]),
        skip,
        fleet.BusinessDayConvention.FOLLOWING,
        fleet.Direction.FORWARD
    )
    dates = list(map(_to_py_date, fleet_output))
    dates_str = ' '.join([d.strftime('%Y-%m-%d') for d in dates])
    return dates_str

def ko_levels_output(
    subclass, 
    tenor: int, 
    skip: int,
    ko_level:float,
    step_down: float = 0):
    substring ="stepdown"
    n = tenor - skip + 1
    if substring in subclass:
        sequence = [ko_level - step_down * i for i in range(n)]
        ko_levels =' '.join([str(num) for num in sequence])
    else:
        ko_levels =  ' '.join([str(ko_level)] * n)
    return ko_levels  

def coupons_output(
    subclass, 
    tenor: int, 
    skip: int,
    ko_coupon: float,
    secondary_coupon: float,
    bonus_period: int = 1):
    substring ="bonus"
    n = tenor - skip + 1
    m = bonus_period * 12
    if substring in subclass:
        sequence = [ko_coupon] * (n - m) + [secondary_coupon] * m
        ko_coupons = ' '.join([str(num) for num in sequence])
    else:
        ko_coupons =  ' '.join([str(ko_coupon)] * n)
    return ko_coupons 


def generate_contracts(contract,trade_dates,underlying_prices,trade_book):
    
    #读取contract 要素
    subclass = contract['structure']
    underlying = contract['underlying']
    principal = contract['principal']
    tenor = int(contract['tenor'][:-1])
    skip = int(contract['lock_period'][:-1])
    ki_level = contract['knock in barrier']
    ko_level = contract['knock out barrier']
    ko_coupon = contract['coupon']
    step_down =  contract.get('stepdown', 0)
    secondary_coupon = contract.get('secondary coupon', 0)
    bonus_period = int(contract.get('bonus_period', "1Y")[:-1])
    maturity_coupon = contract.get('maturity coupon', contract.get('secondary coupon', contract['coupon']))
    
    # 生成序列及必要入参
    ko_levels = ko_levels_output(subclass, tenor,skip,ko_level,step_down)
    ko_coupons = coupons_output(subclass, tenor,skip,ko_coupon,secondary_coupon,bonus_period)
    substring ="limitedloss"
    if substring in subclass:
        margin = max_loss = round((1.0 - ki_level),4)
    else:
        margin = max_loss = 1.0
    
    #获取雪球的columns并填入结构要素
    snowball_df = pd.read_csv(SNOWBALL_CSV_PATH)
    columns = snowball_df.columns.tolist()  
    df = pd.DataFrame(columns=columns)
    input_data = [('TRADE STATUS','ACTIVE'),('TRADE BOOK','SIMULATION'),('TRADE TYPE','OPT'),('TRADE DIRECTION','BUY'),
              ('UNDERLYING CODE', underlying),('NOTIONAL PRINCIPAL', principal),('KNOCK IN STATUS','FALSE'),('KNOCK IN LEVEL',ki_level),
              ('KNOCK IN STRIKE LEVEL', 1.0),('KNOCK IN PARTICIPATION',1.0),('DAILY KNOCK IN','TRUE'),('KNOCK OUT LEVELS',ko_levels),
              ('KNOCK OUT COUPONS',ko_coupons),('MATURITY COUPON',maturity_coupon),('MARGIN RATIO',margin),('MAX LOSS',max_loss)]
    data_dict = {key: value for key, value in input_data}
    df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
    structure_row = df.iloc[0]
    rows = [structure_row for _ in range(len(trade_dates))]
    df = pd.DataFrame(rows, columns=columns)
    df.index=range(len(df.index))
    for i in range(len(trade_dates)):
        df.loc[i,'INITIAL PRICE'] = underlying_prices.iloc[i]
        df.loc[i,'START DATE'] = trade_dates.iloc[i]
        date_str = df.loc[i,'START DATE'].strftime('%Y%m%d')
        df.loc[i,'TRADE CODE'] = f"SIMULATION-OPT-{date_str}-01"
        df.loc[i,'KNOCK OUT DATES'] = schedule_dates(trade_dates.iloc[i], tenor, 1,  "month", skip)
        dates = df.loc[i,'KNOCK OUT DATES'].split()
        df.loc[i,'END DATE'] = dates[-1]
    df.to_csv(trade_book, mode='a', header=False, index=False)