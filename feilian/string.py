# -*- coding: utf-8 -*-

from typing import Any, Callable

def join_values(*values: Any, sep='', func: Callable[[Any], str] = str, do_trim=False, ignore_empty=False):
    def f():
        for x in values:
            s = func(x)
            if do_trim:
                s = s.strip()
            if s or not ignore_empty:
                yield s
    return sep.join(f())
