# -*- coding: utf-8 -*-

from typing import Dict, List, Union, Any
import json
from .io import ensure_parent_dir_exist

def read_json(filepath: str, encoding='utf-8', **kwargs):
    """
    An agent for `json.load()` with some default value.
    """
    with open(filepath, encoding=encoding) as f:
        return json.load(f, **kwargs)

def save_json(filepath: str, data: Union[Dict[str, Any], List[Any]],
              encoding='utf-8', newline='\n', indent=2, ensure_ascii=False, **kwargs):
    """
    An agent for `json.dump()` with some default value.
    """
    ensure_parent_dir_exist(filepath)
    with open(filepath, 'w', encoding=encoding, newline=newline) as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, **kwargs)
