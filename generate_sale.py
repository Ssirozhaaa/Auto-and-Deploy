from datetime import datetime, timedelta
from random import randint
import configparser

import pandas as pd

config = configparser.ConfigParser()
config.read("config.ini")

company_all = eval(config["Companies"]["company_all"])

today = datetime.today()
yestreday = today - timedelta(days=1)

# if 1 <= today.weekday() <= 5:
d = {
    "date": [yestreday.strftime("%d-%m-%Y")] * len(company_all) * 2,
    "company": company_all * 2,
    "trans_type": ["buy"] * len(company_all) + ["sell"] * len(company_all),
    "amount": [randint(0, 1000) for _ in range(len(company_all) * 2)],
}

df = pd.DataFrame(d)
df.to_csv("sales-data.csv", index=False)

