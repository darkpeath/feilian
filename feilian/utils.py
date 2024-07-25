#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Any, Union, Collection, List

def flatten_dict(data: Dict[str, Any], prefix="", joiner=".",
                 exclude: Union[None, str, Collection[str]] = None,
                 frozen: Union[None, str, Collection[str]] = None,
                 empty_as_default=False, empty_value=None,
                 res: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    flatten dict as a flat one layer dict
    :param data:      origin dict
    :param prefix:    prefix for key in the dict
    :param joiner:    join symbol for different layer key
    :param exclude:   prefix to be excluded from result
    :param frozen:    keys not to be flattened
    :param empty_as_default:  should set a default value if value is an empty dict
    :param empty_value:       if `empty_as_default` is `True`, used as the default value for empty dict
    :param res:       the result flat layer dict, create a new one if not given.
    """
    if res is None:
        res = {}
    if isinstance(exclude, str):
        exclude = {exclude}
    if isinstance(frozen, str):
        frozen = {frozen}

    # all keys are start with the prefix, ignore data
    if exclude and prefix in exclude:
        return res

    # all keys in data should be frozen
    if frozen and prefix in frozen:
        for k, v in data.items():
            res[prefix+k] = v
        return res

    for k, v in data.items():
        k = prefix + k

        if exclude and k in exclude:
            # only the key should be excluded
            continue

        if frozen and k in frozen:
            # frozen key, keep it as original value
            res[k] = v
            continue

        if isinstance(v, dict):
            if len(v) == 0:
                # empty dict, set as default value if set
                if empty_as_default:
                    res[k] = empty_value
            else:
                # value is a dict, flatten recursively
                flatten_dict(v, prefix=k+joiner, joiner=joiner, exclude=exclude, frozen=frozen, res=res)
        else:
            # normal value, keep it as original value
            res[k] = v

    return res


def flatten_list(data: List[Any], res: List[Any] = None) -> List[Any]:
    """
    Flatten nested list as a flat on layer list.
    :param data:    a nested list
    :param res:     the result flat layer list, create a new one if not given.
    """
    if res is None:
        res = []

    for x in data:
        if isinstance(x, list):
            # flatten recursively
            flatten_list(x, res)
        else:
            res.append(x)

    return res
