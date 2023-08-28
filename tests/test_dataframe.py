# -*- coding: utf-8 -*-

import feilian

def test_read():
    input_file = 'a.csv'
    df = feilian.read_dataframe(input_file)
    print(df)
