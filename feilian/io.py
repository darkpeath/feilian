# -*- coding: utf-8 -*-

import os

def ensure_parent_dir_exist(filepath: str | os.PathLike):
    if isinstance(filepath, str):
        parent_path = os.path.abspath(os.path.dirname(filepath))
    elif isinstance(filepath, os.PathLike):
        parent_path = os.path.abspath(os.path.dirname(filepath.__fspath__()))
    else:
        return
    os.makedirs(parent_path, exist_ok=True)
