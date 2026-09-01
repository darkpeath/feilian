# -*- coding: utf-8 -*-

import os
from ._typing import Union

def ensure_parent_dir_exist(filepath: Union[str, os.PathLike]):
    # non-path values (e.g. buffers) are ignored
    if isinstance(filepath, (str, os.PathLike)):
        parent_path = os.path.abspath(os.path.dirname(os.fspath(filepath)))
        os.makedirs(parent_path, exist_ok=True)
