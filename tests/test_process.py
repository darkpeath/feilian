# -*- coding: utf-8 -*-

import pandas as pd
import feilian

class _DoubleProcessor(feilian.DataframeProcessor):
    """Double the value of column 'a' and drop rows where 'a' is even."""

    def process_row(self, i, row):
        if row["a"] % 2 == 0:
            return None
        return {"a": row["a"] * 2, "b": row["b"]}

def _write_input(path, values):
    df = pd.DataFrame({"a": values, "b": [f"v{x}" for x in values]})
    feilian.save_dataframe(path, df)
    return df

def test_processor_run(tmp_path):
    input_file = tmp_path / "in.csv"
    output_file = tmp_path / "out.csv"
    _write_input(input_file, [1, 2, 3])
    _DoubleProcessor().run(str(input_file), str(output_file))
    res = feilian.read_dataframe(output_file)
    assert res["a"].tolist() == [2, 6]
    assert res["b"].tolist() == ["v1", "v3"]

def test_processor_multi_input(tmp_path):
    f1 = tmp_path / "in1.csv"
    f2 = tmp_path / "in2.csv"
    output_file = tmp_path / "out.csv"
    _write_input(f1, [1, 2])
    _write_input(f2, [3, 4])
    _DoubleProcessor().run([str(f1), str(f2)], str(output_file))
    res = feilian.read_dataframe(output_file)
    assert res["a"].tolist() == [2, 6]

def test_processor_no_output(tmp_path):
    input_file = tmp_path / "in.csv"
    _write_input(input_file, [1, 2, 3])
    _DoubleProcessor().run(str(input_file), write_output=False)
    # input file is unchanged when write_output is False
    res = feilian.read_dataframe(input_file)
    assert res["a"].tolist() == [1, 2, 3]

def test_processor_read_args(tmp_path):
    input_file = tmp_path / "in.csv"
    output_file = tmp_path / "out.csv"
    _write_input(input_file, [1, 3])
    processor = _DoubleProcessor(input_dtype=str)
    df = processor.read_data(str(input_file))
    assert df["a"].tolist() == ["1", "3"]
