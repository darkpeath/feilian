# -*- coding: utf-8 -*-

from pathlib import Path
import feilian

def test_read():
    input_file = Path(__file__).parent.joinpath('a.csv')
    df = feilian.read_dataframe(input_file)
    print(df)
