# -*- coding: utf-8 -*-

from typing import Dict, List, Union, Any
import json
from .io import ensure_parent_dir_exist

def _is_jsonl(filepath: str, jsonl=None) -> bool:
    if jsonl is None:
        jsonl = filepath.lower().endswith('.jsonl')
    return jsonl

def read_json(filepath: str, jsonl=None, encoding='utf-8', **kwargs):
    """
    An agent for `json.load()` with some default value.
    """
    jsonl = _is_jsonl(filepath, jsonl)
    with open(filepath, encoding=encoding) as f:
        if jsonl:
            return [json.loads(x) for x in f]
        else:
            return json.load(f, **kwargs)

def save_json(filepath: str, data: Union[Dict[str, Any], List[Any]], jsonl=False,
              encoding='utf-8', newline='\n', indent=2, ensure_ascii=False, **kwargs):
    """
    An agent for `json.dump()` with some default value.
    """
    jsonl = _is_jsonl(filepath, jsonl)
    if jsonl and not isinstance(data, list):
        # data should be a list
        raise ValueError("data should be a list when save as jsonl format")
    ensure_parent_dir_exist(filepath)
    with open(filepath, 'w', encoding=encoding, newline=newline) as f:
        if jsonl:
            for x in data:
                f.write(json.dumps(x, ensure_ascii=ensure_ascii, **kwargs))
                f.write(newline)
        else:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, **kwargs)
