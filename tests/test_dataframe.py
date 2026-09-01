# -*- coding: utf-8 -*-

import io
from pathlib import Path
import pandas as pd
import feilian

def test_read():
    input_file = Path(__file__).parent.joinpath('a.csv')
    df = feilian.read_dataframe(input_file)
    assert list(df.columns) == ['a', 'b', 'c']
    assert len(df) == 4
    assert df['b'].tolist() == ['k1', 'k2', 'k3', 'k4']

def test_read_auto_encoding_from_file():
    input_file = Path(__file__).parent.joinpath('a.csv')
    df = feilian.read_dataframe(input_file, encoding='auto')
    assert len(df) == 4

def test_read_auto_encoding_from_text_stream():
    buf = io.StringIO('a,b\n1,2\n3,4\n')
    df = feilian.read_dataframe(buf, file_format='csv', encoding='auto')
    assert list(df.columns) == ['a', 'b']
    assert len(df) == 2

def test_read_auto_encoding_from_bytes_stream():
    buf = io.BytesIO('a,b\n中文,2\n'.encode('gb18030'))
    df = feilian.read_dataframe(buf, file_format='csv', encoding='auto')
    assert df['a'].tolist() == ['中文']

def test_save_and_read(tmp_path):
    df = pd.DataFrame(dict(a=[1, 2, 3], b=['x', 'y', 'z']))
    for suffix in ['csv', 'tsv', 'json', 'jsonl', 'xlsx']:
        file = tmp_path / f"data.{suffix}"
        feilian.save_dataframe(file, df)
        df2 = feilian.read_dataframe(file)
        assert df2['a'].tolist() == [1, 2, 3], suffix
        assert df2['b'].tolist() == ['x', 'y', 'z'], suffix

def test_merge_dataframe_rows():
    df = pd.DataFrame([
        {"a": "1", "b": "2", "c": "5"},
        {"a": "2", "b": "6", "c": "8"},
        {"a": "1", "b": "8", "c": "9"},
    ])
    res = feilian.merge_dataframe_rows(df, col_id="a", join_sep=",")
    res = res.sort_values("a").reset_index(drop=True)
    assert res["b"].tolist() == ["2,8", "6"]
    # without join_sep, multi values are kept as a list
    res2 = feilian.merge_dataframe_rows(df, col_id="a")
    res2 = res2.sort_values("a").reset_index(drop=True)
    assert res2["b"].tolist() == [["2", "8"], "6"]

def test_join_values_empty_sep():
    from feilian.dataframe import join_values
    assert join_values(['x', 'y'], sep='') == 'xy'
    assert join_values(['x', 'y'], sep='-') == 'x-y'
    assert join_values(['x', 'y']) == ['x', 'y']
    assert join_values(['x']) == 'x'
    assert join_values([]) == ''

def test_text_checkers_return_bool():
    for func in [feilian.is_empty_text, feilian.is_nonempty_text,
                 feilian.is_blank_text, feilian.is_non_blank_text]:
        for value in ['', ' ', 'x', None, float('nan')]:
            assert isinstance(func(value), bool), (func.__name__, value)
    assert feilian.is_empty_text('')
    assert feilian.is_nonempty_text('x')
    assert feilian.is_blank_text(' ')
    assert feilian.is_non_blank_text(' x ')
