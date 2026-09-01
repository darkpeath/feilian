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

def test_flatten_dict_simple():
    assert feilian.flatten_dict({"a": {"b": {"c": 1}}, "d": 2}) == {"a.b.c": 1, "d": 2}
    assert feilian.flatten_dict({}) == {}

def test_flatten_dict_joiner():
    assert feilian.flatten_dict({"a": {"b": 1}}, joiner="/") == {"a/b": 1}

def test_flatten_dict_empty_value():
    # empty dict is dropped by default
    assert feilian.flatten_dict({"a": {}}) == {}
    # keep it as a default value when requested
    assert feilian.flatten_dict({"a": {}}, empty_as_default=True) == {"a": None}
    assert feilian.flatten_dict({"a": {}}, empty_as_default=True, empty_value=0) == {"a": 0}

def test_flatten_dict_exclude_nested():
    data = {"a": {"b": 1, "c": 2}, "d": 3}
    assert feilian.flatten_dict(data, exclude="a.b") == {"a.c": 2, "d": 3}

def test_flatten_list():
    assert feilian.flatten_list([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
    assert feilian.flatten_list([]) == []
    assert feilian.flatten_list([[], [1]]) == [1]

def test_ensure_parent_dir_exist(tmp_path):
    path = tmp_path / "x" / "y" / "z.txt"
    feilian.ensure_parent_dir_exist(str(path))
    assert path.parent.is_dir()
    # calling again on an existing dir is a no-op
    feilian.ensure_parent_dir_exist(str(path))

def test_string_join_values():
    from feilian.string import join_values
    assert join_values("a", "b", "c") == "abc"
    assert join_values("a", "b", sep="-") == "a-b"
    assert join_values(1, 2, sep=",") == "1,2"
    assert join_values(" a ", "b", sep=",", do_trim=True) == "a,b"
    assert join_values("a", "", "b", sep=",", ignore_empty=True) == "a,b"
    assert join_values("a", "", "b", sep=",") == "a,,b"
    assert join_values() == ""
