#!/usr/bin/env python
# coding: utf-8

import feilian

def test_flatten_dict():
    d1 = {
        "a": 12,
        "b": ["4", "s"],
        "c": {
            "l": 0,
            "j": {
                "se": "we",
                "t": 5,
            }
        }
    }
    d2 = {
        "a": 12,
        "b": ["4", "s"],
        "c.l": 0,
        "c.j.se": "we",
        "c.j.t": 5,
    }

    d3 = feilian.flatten_dict(d1)

    assert d2 == d3
