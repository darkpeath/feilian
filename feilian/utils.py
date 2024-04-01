#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Any

def flatten_dict(data: Dict[str, Any], prefix="", joiner=".", exclude_keys=None,
                 res: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    flatten dict as a flat one layer dict
    :param data:      origin dict
    :param prefix:    prefix for key in the dict
    :param joiner:    join symbol for different layer key
    :param exclude_keys:  keys exclude from result
    :param res:       the result flat layer dict, create a new one if not given.
    """
    if res is None:
        res = {}
    if exclude_keys is None:
        exclude_keys = set()
    for k, v in data.items():
        k = prefix + k
        if isinstance(v, dict) and k not in exclude_keys:
            flatten_dict(v, prefix=k + joiner, joiner=joiner, exclude_keys=exclude_keys, res=res)
        else:
            res[k] = v
    return res

