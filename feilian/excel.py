import pandas as pd
from typing import Union, Iterable, Dict, Sequence, Any, List, Tuple
from .dataframe import save_dataframe

def _save_excel(file, df, *args, **kwargs):
    # if df is a list of dataframe, then save each dataframe into a sheet
    if isinstance(df, (list, tuple)) and df and all(isinstance(x, pd.DataFrame) for x in df):
        if 'sheet_name' in kwargs:
            kwargs.pop('sheet_name')
        with pd.ExcelWriter(file) as writer:
            for i, x in enumerate(df, 1):
                save_dataframe(writer, x, *args, sheet_name=f"Sheet{i}", **kwargs)
    elif isinstance(df, dict) and df and all(isinstance(x, pd.DataFrame) for x in df.values()):
        if 'sheet_name' in kwargs:
            kwargs.pop('sheet_name')
        with pd.ExcelWriter(file) as writer:
            for name, x in df.items():
                save_dataframe(writer, x, *args, sheet_name=name, **kwargs)
    else:
        return save_dataframe(file, df, *args, **kwargs)

_FILE_TYPES = Union[str, 'pd.WriteBuffer[bytes]', 'pd.WriteBuffer[str]']
_DATA_TYPES = Union[
    pd.DataFrame, Iterable[Union[pd.Series, Dict[str, Any]]],
    List[pd.DataFrame], Tuple[pd.DataFrame], Dict[str, pd.DataFrame]
]

def save_excel(file: _FILE_TYPES, df: _DATA_TYPES,
               *args, sheet_name='Sheet1',
               header: Union[Sequence[str], bool] = True,
               index=False, index_label=None,
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
    :param header:              `header` for excel format
    :param index:               save index or not, see docs in df.to_csv();
                                if set as str and `index_label` not set, `index_label` will be set as this
    :param index_label:         header for the index when `index` is `True`
    :param column_mapper:       rename columns; if set, columns not list here will be ignored
    :param include_columns:     if set, columns not list here will be ignored
    :param exclude_columns:     if set, columns list here will be ignored
    :param kwargs:              extra kwargs for df.to_xx()
    """
    _save_excel(
        file, df, *args,
        sheet_name=sheet_name,
        header=header,
        index=index,
        index_label=index_label,
        column_mapper=column_mapper,
        include_columns=include_columns,
        exclude_columns=exclude_columns,
        **kwargs
    )

def write_excel(
    file: _FILE_TYPES, df: _DATA_TYPES,
    *args, sheet_name='Sheet1',
    header: Union[Sequence[str], bool] = True,
    index=False, index_label=None,
    column_mapper: Union[Dict[str, str], Sequence[str]] = None,
    include_columns: Sequence[str] = None,
    exclude_columns: Sequence[str] = None,
    **kwargs
):
    save_excel(
        file, df, *args,
        sheet_name=sheet_name,
        header=header,
        index=index,
        index_label=index_label,
        column_mapper=column_mapper,
        include_columns=include_columns,
        exclude_columns=exclude_columns,
        **kwargs
    )
