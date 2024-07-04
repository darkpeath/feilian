import abc
import tqdm
import pandas as pd
from typing import Any, Dict, Hashable
from .dataframe import read_dataframe, save_dataframe

class BaseProcessor(abc.ABC):
    """
    Base class for processing data.
    """

    @abc.abstractmethod
    def read_data(self, filepath: str) -> Any:
        """
        Read data from input file.
        """

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

    def run(self, input_path: str, output_path: str = None, write_output=True):
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
    def __init__(self, input_dtype=None, progress=False):
        self.input_dtype = input_dtype
        self.progress = progress

    def read_data(self, filepath: str) -> pd.DataFrame:
        return read_dataframe(filepath, dtype=self.input_dtype)

    def save_result(self, filepath: str, result: pd.DataFrame):
        save_dataframe(filepath, result)

    @abc.abstractmethod
    def process_row(self, i: Hashable, row: pd.Series) -> Dict[str, Any]:
        """
        Process a single row of data.
        """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        bar = data.iterrows()
        if self.progress:
            desc = "process" if self.progress is True else self.progress
            bar = tqdm.tqdm(bar, total=len(data), desc=desc)
        res = [self.process_row(i, row) for i, row in bar]
        return pd.DataFrame(res)

