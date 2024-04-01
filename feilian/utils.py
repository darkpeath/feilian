#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Any

def flatten_dict(data: Dict[str, Any], prefix="", joiner=".", exclude_prefixes=None,
                 res: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    flatten dict as a flat one layer dict
    :param data:      origin dict
    :param prefix:    prefix for key in the dict
    :param joiner:    join symbol for different layer key
    :param exclude_prefixes:  keys exclude from result
    :param res:       the result flat layer dict, create a new one if not given.
    """
    if res is None:
        res = {}
    if exclude_prefixes and prefix in exclude_prefixes:
        return res
    for k, v in data.items():
        k = prefix + k
        if isinstance(v, dict) and k not in exclude_prefixes:
            flatten_dict(v, prefix=k + joiner, joiner=joiner, exclude_prefixes=exclude_prefixes, res=res)
        else:
            res[k] = v
    return res

