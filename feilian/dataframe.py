# -*- coding: utf-8 -*-

"""
Encapsulate methods for pandas `DataFrame`.
"""

from typing import Union, Iterable, Dict, List, Any, Sequence, Callable, Tuple, Hashable
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import os
import pathlib
import pandas as pd
import random
import collections
from .io import ensure_parent_dir_exist
from .txt import get_file_encoding

# Compatible with different pandas versions
PD_PARAM_NEWLINE = 'lineterminator'
pd_version = [int(x) for x in pd.__version__.split('.')]
if pd_version[0] < 1 or (pd_version[0] == 1 and pd_version[1] < 5):
    PD_PARAM_NEWLINE = 'line_terminator'

FILE_FORMAT = Literal['csv', 'tsv', 'json', 'xlsx', 'parquet']
COMPRESSION_FORMAT = Literal[None, 'infer', 'snappy', 'gzip', 'brotli', 'bz2', 'zip', 'xz']

def _drop_na_values(data: Union[pd.DataFrame, Dict[str, pd.DataFrame]], axis: Literal['columns', 'rows']):
    if isinstance(data, pd.DataFrame):
        data.dropna(axis=axis, how='all', inplace=True)
    else:
        assert isinstance(data, dict)
        for df in data.values():
            df.dropna(axis=axis, how='all', inplace=True)

def _infer_file_format(file) -> str:
    if isinstance(file, str):
        return os.path.splitext(file)[1].lower()[1:]
    elif isinstance(file, pathlib.PurePath):
        suf = file.suffix
        return suf[1:] if suf.startswith('.') else suf
    elif isinstance(file, os.PathLike):
        return os.path.splitext(str(file))[1].lower()[1:]
    elif isinstance(file, pd.ExcelWriter):
        return 'xlsx'
    else:
        raise ValueError(f"Cannot infer format for type: {type(file)}")

def read_dataframe(file: str | os.PathLike, *args, sheet_name=0,
                   file_format: FILE_FORMAT = None, encoding='auto',
                   jsonl=False, dtype: type = None,
                   drop_na_columns=False, drop_na_rows=False,
                   **kwargs) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    read file as pandas `DataFrame`
    :param file:        the file to be read
    :param args:        extra args for `pd.read_xx()`
    :param sheet_name:      `sheet_name` for `pd.read_excel()`
    :param file_format:     csv, tsv, json ,xlsx, parquet
    :param encoding:    text file encoding
    :param jsonl:       jsonl format or not, only used in json format
    :param dtype:       `dtype` for `pd.read_xx()`
    :param drop_na_columns:     drop column if all values of the column is na
    :param drop_na_rows:        drop row if all values of the row is na
    :param kwargs:      extra kwargs for `pd.read_xx()`
    """
    # decide the file format
    if not file_format:
        file_format = _infer_file_format(file)

    for key in ['lines', 'line_delimited_json_format']:
        if key in kwargs and kwargs.pop(key):
            jsonl = True

    # handle special formats
    if file_format == 'tsv':
        # if the file format is tsv, actually same as csv
        file_format = 'csv'
        if 'sep' in kwargs:
            kwargs.pop('sep')
        kwargs['delimiter'] = '\t'
    elif file_format == 'jsonl':
        file_format = 'json'
        jsonl = True

    if encoding == 'auto' and file_format in ['csv', 'json']:
        if isinstance(file, (str, os.PathLike)):
            encoding = get_file_encoding(file, encoding=encoding)
        else:
            encoding = None

    if file_format == 'csv':
        df = pd.read_csv(file, *args, encoding=encoding, dtype=dtype, **kwargs)
    elif file_format == 'xlsx':
        df = pd.read_excel(file, *args, sheet_name=sheet_name, dtype=dtype, **kwargs)
    elif file_format == 'json':
        try:
            df = pd.read_json(file, *args, encoding=encoding, lines=jsonl, dtype=dtype, **kwargs)
        except Exception as e:
            # if failed, try again with different arg `lines`
            try:
                df = pd.read_json(file, *args, lines=not jsonl, dtype=dtype, **kwargs)
            except Exception:
                raise e
    elif file_format == 'parquet':
        df = pd.read_parquet(file, *args, **kwargs)
    else:
        raise IOError(f"Unknown file format: {file}")

    if drop_na_columns:
        _drop_na_values(df, axis='columns')
    if drop_na_rows:
        _drop_na_values(df, axis='rows')

    return df

def save_dataframe(file: Union[str | os.PathLike, 'pd.WriteBuffer[bytes]',  'pd.WriteBuffer[str]'],
                   df: Union[pd.DataFrame, Iterable[Union[pd.Series, Dict[str, Any]]]],
                   *args, sheet_name='Sheet1',
                   file_format: FILE_FORMAT = None,
                   compression: COMPRESSION_FORMAT = None,
                   index=False, index_label=None,
                   encoding='utf-8', newline='\n',
                   force_ascii=False,
                   orient='records', jsonl=True, indent=None,
                   column_mapper: Union[Dict[str, str], Sequence[str]] = None,
                   include_columns: Sequence[str] = None,
                   exclude_columns: Sequence[str] = None,
                   **kwargs):
    """
    save data into file
    :param file:                where to save the data to
    :param df:                  the data
    :param args:                extra args for df.to_xx()
    :param sheet_name:          `sheet_name` for excel format
    :param file_format:         csv, tsv, json, xlsx, parquet
    :param compression:         name of the compression to use.
                                use `None` for no compression.
    :param index:               save index or not, see docs in df.to_csv();
                                if set as str and `index_label` not set, `index_label` will be set as this
    :param index_label:         header for the index when `index` is `True`
    :param encoding:            text file encoding
    :param newline:             text file newline
    :param force_ascii:         `force_ascii` for json format
    :param orient:              `orient` for json format
    :param jsonl:               jsonl format or not
    :param indent:              indent for json format
    :param column_mapper:       rename columns; if set, columns not list here will be ignored
    :param include_columns:     if set, columns not list here will be ignored
    :param exclude_columns:     if set, columns list here will be ignored
    :param kwargs:              extra kwargs for df.to_xx()
    """
    # decide file format
    if not file_format:
        file_format = _infer_file_format(file)

    # convert data to be a dataframe
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    for key in ['lines', 'line_delimited_json_format']:
        if key in kwargs and kwargs.pop(key):
            jsonl = True

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

    # compatible for set index just use arg `index`
    if index_label is None and isinstance(index, str):
        index, index_label = True, index

    # handle special formats
    if file_format == 'tsv':
        # tsv is actually a csv
        file_format = 'csv'
        kwargs['sep'] = '\t'
    elif file_format == 'jsonl':
        file_format = 'json'
        jsonl = True

    # save to file for different format
    if file_format == 'csv':
        kwargs[PD_PARAM_NEWLINE] = newline
        df.to_csv(file, *args, compression=compression, index=index, index_label=index_label,
                  encoding=encoding, **kwargs)
    elif file_format == 'xlsx':
        df.to_excel(file, *args, index=index, index_label=index_label, sheet_name=sheet_name, **kwargs)
    elif file_format == 'json':
        if jsonl:
            orient = 'records'
            indent = None
        if orient not in ['split', 'table']:
            index = True
        df.to_json(file, *args, compression=compression, index=index,
                   force_ascii=force_ascii, orient=orient, lines=jsonl,
                   indent=indent, **kwargs)
    elif file_format == 'parquet':
        df.to_parquet(file, *args, compression=compression, index=index, **kwargs)
    else:
        raise IOError(f"Unknown file format: {file}")

def iter_dataframe(data: pd.DataFrame,
                   progress_bar: Union[bool, str, 'tqdm', Callable[[Iterable[Any]], 'tqdm']] = False
                   ) -> Iterable[Tuple[Hashable, pd.Series]]:
    """
    iter dataframe rows, may show a progress bar
    :param data:            dataframe
    :param progress_bar:    show a progress bar or not
                            if set a non-empty string, the string will be set as the progress bar description
    """
    rows = data.iterrows()
    if progress_bar:
        from tqdm import tqdm
        if isinstance(progress_bar, tqdm):
            progress_bar.iterable = rows
            rows = progress_bar
        elif isinstance(progress_bar, str):
            rows = tqdm(rows, total=len(data), desc=progress_bar)
        elif callable(progress_bar):
            rows = progress_bar(rows)
        else:
            rows = tqdm(rows, total=len(data))
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
