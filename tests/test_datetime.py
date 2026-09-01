# -*- coding: utf-8 -*-

import datetime
import pytest
import feilian

_DT = datetime.datetime(2026, 9, 1, 15, 30, 45)

def test_format_time_datetime():
    assert feilian.format_time(_DT) == "2026-09-01 15:30:45"
    assert feilian.format_time(_DT, fmt="%H:%M:%S") == "15:30:45"

def test_format_time_str():
    assert feilian.format_time("2026-09-01 15:30:45") == "2026-09-01 15:30:45"
    assert feilian.format_time("2026/09/01", fmt="%Y%m%d") == "20260901"

def test_format_time_timestamp():
    ts = _DT.timestamp()
    assert feilian.format_time(ts) == "2026-09-01 15:30:45"
    assert feilian.format_time(int(ts)) == "2026-09-01 15:30:45"

def test_format_time_now():
    # just check the shape of the output
    s = feilian.format_time()
    datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def test_format_time_invalid_type():
    with pytest.raises(ValueError):
        feilian.format_time(object())

def test_format_date():
    assert feilian.format_date(_DT) == "20260901"
    assert feilian.format_date(_DT, sep="-") == "2026-09-01"

def test_format_date_with_date_object():
    d = datetime.date(2026, 9, 1)
    assert feilian.format_date(d) == "20260901"
    assert feilian.format_time(d, fmt="%Y/%m/%d") == "2026/09/01"
