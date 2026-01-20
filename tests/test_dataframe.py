# -*- coding: utf-8 -*-

from pathlib import Path
import io
import feilian

def test_read():
    input_file = Path(__file__).parent.joinpath('a.csv')
    df = feilian.read_dataframe(input_file)
    print(df)

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
