import os
import pandas as pd
import configparser
from datetime import datetime, timedelta
from yahoo_fin.stock_info import get_data

from pgdb import PGDatabase

config = configparser.ConfigParser()
config.read("config.ini")


company_all = eval(config["Companies"]["company_all"])
sales_path = config["Files"]["sl"]
DATABASE_CR = config['Database']

sl_df = pd.DataFrame()
if os.path.exists(sales_path):
    sl_df = pd.read_csv(sales_path)
    os.remove(sales_path)

history_d = {}

for comp in company_all:
    history_d[comp] = get_data(
        comp,
        start_date=(datetime.today() - timedelta(days=1)).strftime("%m/%d/%Y"),
        end_date=datetime.today().strftime("%m/%d/%Y"),
    ).reset_index()

database = PGDatabase(
    host=DATABASE_CR['HOST'],
    database=DATABASE_CR['DATABASE'],
    user=DATABASE_CR['USER'],
    password=DATABASE_CR['PASSWORD'],
)

for i, row in sl_df.iterrows():
    query = f"insert into sales values ('{row['date']}', '{row['company']}', '{row['trans_type']}', {row['amount']})"
    database.post(query)


for comp, data in history_d.items():
    for i, row in data.iterrows():
        query = f"insert into stock values ('{row['index']}', '{row['ticker']}', {row['open']}, {row['close']})"
        database.post(query)