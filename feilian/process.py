import abc
import tqdm
import pandas as pd
from typing import (
    Any, Dict, Hashable, List,
    Tuple, Union, Iterable, Optional,
)
from .dataframe import (
    read_dataframe,
    save_dataframe,
)

class BaseProcessor(abc.ABC):
    """
    Base class for processing data.
    """

    @abc.abstractmethod
    def read_single_file(self, filepath: str) -> Any:
        """
        Actual method to read data from a single file.
        """

    def merge_input_data(self, data: Iterable[Any]) -> Any:
        """
        Merge data read from multi files.
        """
        return data

    def read_data(self, filepath: Union[str, List[str], Tuple[str]]) -> Any:
        """
        Read data from input file.
        """
        if isinstance(filepath, (list, tuple)):
            return self.merge_input_data(self.read_single_file(x) for x in filepath)
        else:
            return self.read_single_file(filepath)

    @abc.abstractmethod
    def save_result(self, filepath: str, result: Any):
        """
        Save result to output file.
        """

    @abc.abstractmethod
    def process(self, data: Any) -> Any:
        """
        Process data and return result.
        """

    def run(self, input_path: Union[str, List[str], Tuple[str]], output_path: str = None, write_output=True):
        """
        Read from a file, and save result to another file.
        :param input_path:      file with the data
        :param output_path:     where to save the result, if not given, use input_path
        :param write_output:    whether to write the result to the output_file
        """
        data = self.read_data(input_path)
        result = self.process(data)
        if write_output:
            self.save_result(output_path or input_path, result)

class DataframeProcessor(BaseProcessor, abc.ABC):
    def __init__(self, input_dtype=None, progress=False, read_args: Dict[str, Any] = None,
                 write_args: Dict[str, Any] = None):
        self.progress = progress
        self.read_args = read_args or {}
        if input_dtype is not None:
            self.read_args['dtype'] = input_dtype
        self.write_args = write_args or {}

    def read_single_file(self, filepath: str) -> pd.DataFrame:
        return read_dataframe(filepath, **self.read_args)

    def merge_input_data(self, data: Iterable[pd.DataFrame]) -> pd.DataFrame:
        return pd.concat(data)

    def read_data(self, filepath: Union[str, List[str], Tuple[str]]) -> pd.DataFrame:
        return super().read_data(filepath)

    def save_result(self, filepath: str, result: pd.DataFrame):
        save_dataframe(filepath, result, **self.write_args)

    @abc.abstractmethod
    def process_row(self, i: Hashable, row: pd.Series) -> Optional[Dict[str, Any]]:
        """
        Process a single row of data.
        :return:    if `None`, ignore this row
        """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        bar = data.iterrows()
        if self.progress:
            desc = "process" if self.progress is True else self.progress
            bar = tqdm.tqdm(bar, total=len(data), desc=desc)
        res = (self.process_row(i, row) for i, row in bar)
        res = (x for x in res if x is not None)
        return pd.DataFrame(res)

