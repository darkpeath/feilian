# -*- coding: utf-8 -*-

from typing import Union
import pandas as pd

def format_time(time: Union[str, int, float, feilian.datetime] = None, fmt='%Y-%m-%d %H:%M:%S') -> str:
    if time is None:
        time = feilian.datetime.now()
    elif isinstance(time, (int, float)):
        time = feilian.datetime.fromtimestamp(time)
    elif isinstance(time, str):
        time = pd.to_datetime(time)
    else:
        if not isinstance(time, feilian.datetime):
            raise ValueError(f"Unexpected type: {type(time)}")
    return time.strftime(fmt)

def format_date(date: Union[str, int, float, feilian.datetime] = None, sep='-') -> str:
    return format_time(date, fmt=sep.join(['%Y', '%m', '%d']))
