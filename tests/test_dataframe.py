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

def test_save_dataframe_column_options(tmp_path):
    df = pd.DataFrame(dict(a=[1], b=[2], c=[3]))
    file = tmp_path / "data.csv"

    feilian.save_dataframe(file, df, column_mapper={"a": "x"})
    assert list(feilian.read_dataframe(file).columns) == ["x", "b", "c"]

    feilian.save_dataframe(file, df, include_columns=["a", "b"])
    assert list(feilian.read_dataframe(file).columns) == ["a", "b"]

    feilian.save_dataframe(file, df, exclude_columns=["b"])
    assert list(feilian.read_dataframe(file).columns) == ["a", "c"]

def test_save_dataframe_from_records(tmp_path):
    # df may be an iterable of dicts instead of a DataFrame
    file = tmp_path / "data.csv"
    feilian.save_dataframe(file, [{"a": 1}, {"a": 2}])
    assert feilian.read_dataframe(file)["a"].tolist() == [1, 2]

def test_save_dataframe_index_as_str(tmp_path):
    # passing a str as `index` should save the index with that header
    df = pd.DataFrame(dict(a=[10, 20]))
    file = tmp_path / "data.csv"
    feilian.save_dataframe(file, df, index="rowid")
    df2 = feilian.read_dataframe(file)
    assert list(df2.columns) == ["rowid", "a"]
    assert df2["rowid"].tolist() == [0, 1]

def test_read_dataframe_drop_na(tmp_path):
    file = tmp_path / "data.csv"
    file.write_text("a,b,c\n1,,\n2,,x\n,,\n")
    df = feilian.read_dataframe(file, drop_na_columns=True, drop_na_rows=True)
    assert list(df.columns) == ["a", "c"]
    assert len(df) == 2

def test_read_dataframe_tsv(tmp_path):
    file = tmp_path / "data.tsv"
    file.write_text("a\tb\n1\t2\n")
    df = feilian.read_dataframe(file)
    assert df["a"].tolist() == [1]
    assert df["b"].tolist() == [2]

def test_read_dataframe_json_lines_fallback(tmp_path):
    # a .json file that actually contains jsonl should still be readable
    file = tmp_path / "data.json"
    file.write_text('{"a":1}\n{"a":2}\n')
    df = feilian.read_dataframe(file)
    assert df["a"].tolist() == [1, 2]

def test_read_dataframe_unknown_format(tmp_path):
    import pytest
    file = tmp_path / "data.unknown"
    file.write_text("x")
    with pytest.raises(IOError, match="unknown"):
        feilian.read_dataframe(file)

def test_read_dataframe_parquet(tmp_path):
    import pytest
    pytest.importorskip("pyarrow")
    df = pd.DataFrame(dict(a=[1, 2], b=["x", "y"]))
    file = tmp_path / "data.parquet"
    feilian.save_dataframe(file, df)
    assert feilian.read_dataframe(file).equals(df)

def test_iter_dataframe():
    df = pd.DataFrame(dict(a=[1, 2, 3]))
    rows = list(feilian.iter_dataframe(df))
    assert [i for i, _ in rows] == [0, 1, 2]
    assert [row['a'] for _, row in rows] == [1, 2, 3]

def test_iter_dataframe_progress_bar():
    df = pd.DataFrame(dict(a=[1, 2, 3]))
    rows = list(feilian.iter_dataframe(df, progress_bar=True))
    assert len(rows) == 3
    rows = list(feilian.iter_dataframe(df, progress_bar="desc"))
    assert len(rows) == 3

def test_extract_dataframe_sample():
    df = pd.DataFrame(dict(a=[1, 2, 3, 4], b=['w', 'x', 'y', 'z']))
    res = feilian.extract_dataframe_sample(df, filter_func=lambda row: row['a'] > 1)
    assert isinstance(res, pd.DataFrame)
    assert res['a'].tolist() == [2, 3, 4]

    res = feilian.extract_dataframe_sample(df, filter_func=lambda row: row['a'] > 1, size=2)
    assert len(res) == 2

    res = feilian.extract_dataframe_sample(df, filter_func=lambda row: row['a'] > 1, return_format='list')
    assert isinstance(res, list)
    assert len(res) == 3

    res = feilian.extract_dataframe_sample(df, filter_func=lambda row: row['a'] > 1, shuffle=True)
    assert sorted(res['a'].tolist()) == [2, 3, 4]

def test_extract_dataframe_sample_invalid_format():
    import pytest
    df = pd.DataFrame(dict(a=[1]))
    with pytest.raises(ValueError):
        feilian.extract_dataframe_sample(df, filter_func=lambda row: True, return_format='bad')

def test_text_checkers_return_bool():
    for func in [feilian.is_empty_text, feilian.is_nonempty_text,
                 feilian.is_blank_text, feilian.is_non_blank_text]:
        for value in ['', ' ', 'x', None, float('nan')]:
            assert isinstance(func(value), bool), (func.__name__, value)
    assert feilian.is_empty_text('')
    assert feilian.is_nonempty_text('x')
    assert feilian.is_blank_text(' ')
    assert feilian.is_non_blank_text(' x ')
