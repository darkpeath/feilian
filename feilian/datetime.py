# -*- coding: utf-8 -*-

from typing import Union
import pandas as pd
import datetime

def format_time(time: Union[str, int, float, datetime.datetime] = None, fmt='%Y-%m-%d %H:%M:%S') -> str:
    if time is None:
        time = datetime.datetime.now()
    elif isinstance(time, (int, float)):
        time = datetime.datetime.fromtimestamp(time)
    elif isinstance(time, str):
        time = pd.to_datetime(time)
    else:
        if not isinstance(time, datetime.datetime):
            raise ValueError(f"Unexpected type: {type(time)}")
    return time.strftime(fmt)

# when format a date, no sep is used more
def format_date(date: Union[str, int, float, datetime.datetime] = None, sep='') -> str:
    return format_time(date, fmt=sep.join(['%Y', '%m', '%d']))
