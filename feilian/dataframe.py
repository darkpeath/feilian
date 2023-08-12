# -*- coding: utf-8 -*-

"""
Encapsulate methods for pandas `DataFrame`.
"""

from typing import Union, Iterable, Dict, Literal, List, Any, Sequence, Callable, Tuple, Hashable
import os
import pandas as pd
import random
import collections
from .io import ensure_parent_dir_exist

# Compatible with different pandas versions
PD_PARAM_NEWLINE = 'lineterminator'
pd_version = [int(x) for x in pd.__version__.split('.')]
if pd_version[0] < 1 or (pd_version[0] == 1 and pd_version[1] < 5):
    PD_PARAM_NEWLINE = 'line_terminator'

def read_dataframe(file: str, *args, sheet_name=0,
                   file_format: Literal['csv', 'tsv', 'json', 'xlsx'] = None,
                   line_delimited_json_format=False, **kwargs) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    read file as pandas `DataFrame`
    """
    # decide the file format
    if not file_format:
        if not isinstance(file, str):
            raise ValueError("Format should given!")
        file_format = os.path.splitext(file)[1].lower()[1:]

    if 'lines' in kwargs and kwargs.pop('lines'):
        line_delimited_json_format = True

    # if the file format is tsv, actually same as csv
    if file_format == 'tsv':
        file_format = 'csv'
        if 'sep' in kwargs:
            kwargs.pop('sep')
        kwargs['delimiter'] = '\t'

    if file_format == 'csv':
        return pd.read_csv(file, *args, **kwargs)
    elif file_format == 'xlsx':
        return pd.read_excel(file, *args, sheet_name=sheet_name, **kwargs)
    elif file_format == 'json':
        return pd.read_json(file, *args, lines=line_delimited_json_format, **kwargs)
    else:
        raise IOError(f"Unknown file format: {file}")

def save_dataframe(file: Union[str, 'pd.WriteBuffer[bytes]',  'pd.WriteBuffer[str]'],
                   df: Union[pd.DataFrame, Iterable[Union[pd.Series, Dict[str, Any]]]],
                   *args,
                   file_format: Literal['csv', 'tsv', 'json', 'xlsx'] = None,
                   index=False, index_label=None,
                   encoding='utf-8', newline='\n',
                   force_ascii=False,
                   orient='records', line_delimited_json_format=True,
                   column_mapper: Union[Dict[str, str], Sequence[str]] = None,
                   include_columns: Sequence[str] = None,
                   exclude_columns: Sequence[str] = None,
                   **kwargs):
    """
    save data into file
    :param file:                        where to save the data to
    :param df:                          the data
    :param args:                        extra args for df.to_xx()
    :param file_format:                 file format：csv, json, xlsx
    :param index:                       save index or not, see docs in df.to_csv()
    :param index_label:                 header for the index when `index` is `True`
    :param encoding:                    text file encoding
    :param newline:                     text file newline
    :param force_ascii:                 `force_ascii` for json format
    :param orient:                      `orient` for json format
    :param line_delimited_json_format:  jsonl format or not
    :param column_mapper:               rename columns; if set, columns not list here will be ignored
    :param include_columns:             if set, columns not list here will be ignored
    :param exclude_columns:             if set, columns list here will be ignored
    :param kwargs:                      extra kwargs for df.to_xx()
    """
    # decide file format
    if not file_format:
        if isinstance(file, str):
            file_format = os.path.splitext(file)[1].lower()[1:]
        elif isinstance(file, pd.ExcelWriter):
            file_format = 'xlsx'
        else:
            raise ValueError("Format should given!")

    # convert data to be a dataframe
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    # deal with columns
    if column_mapper:
        df = df.rename(columns=column_mapper)
    if exclude_columns:
        df = df.drop(exclude_columns, axis=1)
    if include_columns:
        df = df.reindex(include_columns, axis=1)

    # ensure parent dir exists
    if isinstance(file, (str, os.PathLike)):
        ensure_parent_dir_exist(file)

    # tsv is actually a csv
    if file_format == 'tsv':
        file_format = 'csv'
        kwargs['sep'] = '\t'

    # save to file for different format
    if file_format == 'csv':
        kwargs[PD_PARAM_NEWLINE] = newline
        df.to_csv(file, *args, index=index, index_label=index_label, encoding=encoding, **kwargs)
    elif file_format == 'xlsx':
        df.to_excel(file, *args, index=index, index_label=index_label, **kwargs)
    elif file_format == 'json':
        if line_delimited_json_format:
            orient = 'records'
            index = True
        df.to_json(file, *args, index=index, force_ascii=force_ascii,
                   orient=orient, lines=line_delimited_json_format,
                   **kwargs)
    else:
        raise IOError(f"Unknown file format: {file}")

def iter_dataframe(data: pd.DataFrame, progress_bar=False) -> Iterable[Tuple[Hashable, pd.Series]]:
    """
    iter dataframe rows, may show a progress bar
    :param data:            dataframe
    :param progress_bar:    show a progress bar or not
                            if set a non-empty string, the string will be set as the progress bar description
    """
    rows = data.iterrows()
    if progress_bar:
        import tqdm
        rows = tqdm.tqdm(rows, total=len(data), desc=progress_bar if isinstance(progress_bar, str) else None)
    return rows

def extract_dataframe_sample(data: pd.DataFrame,
                             filter_func: Callable[[pd.Series], bool],
                             size=0, shuffle=False,
                             return_format: Literal['df', 'dataframe', 'list'] = 'dataframe',
                             progress_bar=False) -> Union[pd.DataFrame, List[pd.Series]]:
    """
    extract sample from a dataframe
    :param data:            original data
    :param filter_func:     bool function, `True` means to reserve the row
    :param size:            max size for the result
    :param shuffle:         shuffle result or not
    :param progress_bar:    passed to `iter_dataframe()`
    :param return_format:   one of {'dataframe', 'list'}
    """
    result = [row for _, row in iter_dataframe(data, progress_bar=progress_bar) if filter_func(row)]
    if shuffle:
        random.shuffle(result)
    if 0 < size < len(result):
        result = result[:size]
    if return_format == 'df' or return_format == 'dataframe':
        try:
            return pd.DataFrame(result)
        except pd.errors.InvalidIndexError:
            return pd.DataFrame([{k: v for k, v in x.items()} for x in result])
    elif return_format == 'list':
        return result
    raise ValueError("Param 'return_format' should be one of {'dataframe', 'list'}.")

def is_empty_text(s: str) -> bool:
    return pd.isna(s) or not s

def is_nonempty_text(s: str) -> bool:
    return pd.notna(s) and isinstance(s, str) and s

def is_blank_text(s: str) -> bool:
    return pd.isna(s) or isinstance(s, str) and not s.strip()

def is_non_blank_text(s: str) -> bool:
    return pd.notna(s) and isinstance(s, str) and s.strip()

def join_values(values: Sequence[Any], sep=None) -> str:
    if not values:
        return ''
    if len(values) == 1:
        return str(values[0])
    return sep.join(map(str, values)) if sep else values

def merge_dataframe_rows(data: pd.DataFrame, col_id='ID', na=None, join_sep=None, progress_bar=False) -> pd.DataFrame:
    """
    merge rows of same id to one row, similar to group by in sql
    :param data:            original data
    :param col_id:          column name for the id col
    :param na:              values to be treated as na
    :param join_sep:        seperator to join multi values
    :param progress_bar:    passed to `iter_dataframe()`
    """
    if na is None:
        na = set()
    elif isinstance(na, str):
        na = {na}
    else:
        na = set(na)
    counts = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    rows = iter_dataframe(data, progress_bar=progress_bar)
    for i, row in rows:
        eid = row[col_id]
        for k, v in row.items():
            if pd.notna(v) and v not in na:
                counts[eid][k][v] += 1
    result = []
    for x in counts.values():
        item = {col: join_values(list(values.keys()), sep=join_sep) for col, values in x.items()}
        result.append(item)
    return pd.DataFrame(result)
