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
        },
        "f": 7,
        "g": {
            "ts": "9w",
            "j2": 8,
        },
        "w": {
            "s": {
                "ge": 89,
                "00": "ej",
            },
            "r": {
                "le": 33,
                "03": "ef",
            }
        },
        "sk": {
            "a": "23",
            "b": {
                "s": 9,
                "g": 0,
                "p": 4,
            },
            "c": {
                "s": 8,
                "t": "w",
                "j": "23",
            }
        },
    }
    d2 = {
        "a": 12,
        "b": ["4", "s"],
        "c.l": 0,
        "c.j.se": "we",
        "c.j.t": 5,
        "g": {
            "ts": "9w",
            "j2": 8,
        },
        "w.s": {
            "ge": 89,
            "00": "ej",
        },
        "w.r.le": 33,
        "w.r.03": "ef",
        "sk.a": "23",
        "sk.b": {
            "s": 9,
            "g": 0,
            "p": 4,
        },
        "sk.c": {
            "s": 8,
            "t": "w",
            "j": "23",
        }
    }

    d3 = feilian.flatten_dict(d1, frozen={"g", "w.s", "sk."}, exclude="f")

    assert d2 == d3
