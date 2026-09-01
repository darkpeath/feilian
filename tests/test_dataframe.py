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
    # the sample must be long enough for the encoding detection to be reliable
    rows = ''.join(f'中文内容示例第{i}行,这是用于编码检测的较长文本\n' for i in range(20))
    buf = io.BytesIO(f'a,b\n{rows}'.encode('gb18030'))
    df = feilian.read_dataframe(buf, file_format='csv', encoding='auto')
    assert len(df) == 20
    assert df['a'].tolist()[0] == '中文内容示例第0行'

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

def test_parse_pandas_version():
    from feilian.dataframe import _parse_version
    assert _parse_version('1.3.5') == [1, 3]
    assert _parse_version('2.1.0rc0') == [2, 1]
    assert _parse_version('3.0.0.dev0+2098.gc9d764f') == [3, 0]
    # always contains at least [major, minor]
    assert _parse_version('2') == [2, 0]

def test_infer_format_unsupported_type():
    import pytest
    with pytest.raises(ValueError):
        feilian.read_dataframe(12345)

def test_read_dataframe_lines_kwarg(tmp_path):
    # 'lines' and 'line_delimited_json_format' are aliases of jsonl=True
    file = tmp_path / "data.json"
    file.write_text('{"a":1}\n{"a":2}\n')
    df = feilian.read_dataframe(file, lines=True)
    assert df["a"].tolist() == [1, 2]
    df = feilian.read_dataframe(file, line_delimited_json_format=True)
    assert df["a"].tolist() == [1, 2]

def test_save_dataframe_lines_kwarg(tmp_path):
    df = pd.DataFrame(dict(a=[1, 2]))
    file = tmp_path / "data.json"
    feilian.save_dataframe(file, df, jsonl=False, lines=True)
    assert file.read_text().count('\n') >= 2  # one object per line
    assert feilian.read_dataframe(file)["a"].tolist() == [1, 2]

def test_save_dataframe_compression(tmp_path):
    df = pd.DataFrame(dict(a=[1, 2, 3]))
    file = tmp_path / "data.csv.gz"
    feilian.save_dataframe(file, df, file_format='csv', compression='gzip')
    df2 = feilian.read_dataframe(file, file_format='csv')
    assert df2["a"].tolist() == [1, 2, 3]

def test_compressed_suffix_inference(tmp_path):
    # format and compression are inferred from suffixes like '.csv.gz'
    df = pd.DataFrame(dict(a=[1, 2, 3]))
    import gzip
    for name in ["data.csv.gz", "data.jsonl.gz"]:
        file = tmp_path / name
        feilian.save_dataframe(file, df)
        with gzip.open(file) as f:  # should actually be gzip compressed
            assert f.read()
        assert feilian.read_dataframe(file)["a"].tolist() == [1, 2, 3], name

def test_read_compressed_with_auto_encoding(tmp_path):
    # encoding detection cannot work on compressed bytes and should be skipped
    df = pd.DataFrame(dict(a=['中文', '数据'], b=[1, 2]))
    file = tmp_path / "data.csv.gz"
    feilian.save_dataframe(file, df)
    df2 = feilian.read_dataframe(file, encoding='auto')
    assert df2['a'].tolist() == ['中文', '数据']

def test_save_dataframe_json_indent(tmp_path):
    df = pd.DataFrame(dict(a=[1], b=["中文"]))
    file = tmp_path / "data.json"
    feilian.save_dataframe(file, df, jsonl=False, indent=2)
    content = file.read_text()
    assert '中文' in content  # force_ascii defaults to False
    assert feilian.read_dataframe(file, jsonl=False)["a"].tolist() == [1]

def test_merge_dataframe_rows_na_values():
    df = pd.DataFrame([
        {"a": "1", "b": "-"},
        {"a": "1", "b": "x"},
    ])
    res = feilian.merge_dataframe_rows(df, col_id="a", na="-", join_sep=",")
    assert res["b"].tolist() == ["x"]

def test_merge_dataframe_rows_na_id_skipped():
    df = pd.DataFrame([
        {"a": "1", "b": "x"},
        {"a": None, "b": "y"},
        {"a": float("nan"), "b": "z"},
    ])
    res = feilian.merge_dataframe_rows(df, col_id="a")
    assert len(res) == 1
    assert res["b"].tolist() == ["x"]
    # ids matching the `na` values are skipped as well
    res = feilian.merge_dataframe_rows(df, col_id="a", na="1")
    assert len(res) == 0

def test_iter_dataframe_with_tqdm_instance():
    from tqdm import tqdm
    df = pd.DataFrame(dict(a=[1, 2, 3]))
    bar = tqdm(total=len(df), disable=True)
    rows = list(feilian.iter_dataframe(df, progress_bar=bar))
    assert len(rows) == 3

def test_iter_dataframe_with_callable():
    df = pd.DataFrame(dict(a=[1, 2]))
    called = []
    def wrapper(it):
        called.append(True)
        return it
    rows = list(feilian.iter_dataframe(df, progress_bar=wrapper))
    assert len(rows) == 2
    assert called == [True]

def test_text_checkers_return_bool():
    for func in [feilian.is_empty_text, feilian.is_nonempty_text,
                 feilian.is_blank_text, feilian.is_non_blank_text]:
        for value in ['', ' ', 'x', None, float('nan')]:
            assert isinstance(func(value), bool), (func.__name__, value)
    assert feilian.is_empty_text('')
    assert feilian.is_nonempty_text('x')
    assert feilian.is_blank_text(' ')
    assert feilian.is_non_blank_text(' x ')

def test_json_io():
    input_file = Path(__file__).parent.joinpath('a.jsonl')
    with open(input_file, 'rb') as f:
        buf1 = io.BytesIO(f.read())
    buf2 = io.BytesIO()
    s1 = buf1.getvalue().decode('utf-8')
    buf1.seek(0)
    d1 = feilian.read_dataframe(buf1, file_format='jsonl')
    feilian.save_dataframe(buf2, d1, file_format='jsonl', escape_forward_slashes=False)
    s2 = buf2.getvalue().decode('utf-8')
    assert s1 == s2
    buf2.seek(0)
    d2 = feilian.read_dataframe(buf2, file_format='jsonl')
    assert d1.equals(d2)
