# -*- coding: utf-8 -*-

import pandas as pd
import feilian

def _df(cols):
    return pd.DataFrame({c: [1, 2, 3] for c in cols})

def test_save_excel_single_dataframe(tmp_path):
    path = tmp_path / "a.xlsx"
    df = _df(["a", "b"])
    feilian.save_excel(path, df)
    df2 = feilian.read_dataframe(path)
    assert df2.equals(df)

def test_save_excel_list_of_dataframes(tmp_path):
    path = tmp_path / "a.xlsx"
    dfs = [_df(["a"]), _df(["b"])]
    feilian.save_excel(path, dfs)
    sheets = feilian.read_dataframe(path, sheet_name=None)
    assert set(sheets.keys()) == {"Sheet1", "Sheet2"}
    assert sheets["Sheet1"].equals(dfs[0])
    assert sheets["Sheet2"].equals(dfs[1])

def test_save_excel_dict_of_dataframes(tmp_path):
    path = tmp_path / "a.xlsx"
    dfs = {"x": _df(["a"]), "y": _df(["b"])}
    feilian.save_excel(path, dfs)
    sheets = feilian.read_dataframe(path, sheet_name=None)
    assert set(sheets.keys()) == {"x", "y"}
    assert sheets["x"].equals(dfs["x"])
    assert sheets["y"].equals(dfs["y"])

def test_save_excel_sheet_name(tmp_path):
    path = tmp_path / "a.xlsx"
    df = _df(["a"])
    feilian.save_excel(path, df, sheet_name="data")
    sheets = feilian.read_dataframe(path, sheet_name=None)
    assert list(sheets.keys()) == ["data"]

def test_write_excel_alias(tmp_path):
    path = tmp_path / "a.xlsx"
    df = _df(["a", "b"])
    feilian.write_excel(path, df)
    assert feilian.read_dataframe(path).equals(df)
