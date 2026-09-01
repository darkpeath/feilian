# -*- coding: utf-8 -*-

from feilian import ArgValueParser

def test_split_strs_to_list():
    assert ArgValueParser.split_strs_to_list("a,b,c") == ["a", "b", "c"]
    assert ArgValueParser.split_strs_to_list(["a,b", "c"]) == ["a", "b", "c"]
    assert ArgValueParser.split_strs_to_list(" a , b ") == ["a", "b"]
    assert ArgValueParser.split_strs_to_list(" a , b ", do_trim=False) == [" a ", " b "]
    assert ArgValueParser.split_strs_to_list("a,,b") == ["a", "b"]
    assert ArgValueParser.split_strs_to_list("a;b", sep=";") == ["a", "b"]
    assert ArgValueParser.split_strs_to_list(None) == []
    assert ArgValueParser.split_strs_to_list("") == []

def test_split_strs_with_parse_func():
    assert ArgValueParser.split_strs_to_list("1,2,3", func=int) == [1, 2, 3]

def test_split_strs_to_set():
    assert ArgValueParser.split_strs_to_set("a,b,a") == {"a", "b"}
    assert ArgValueParser.split_strs_to_set(None) == set()

def test_bound_if_singleton():
    assert ArgValueParser.bound_list_if_singleton("x", elem_type=str) == ["x"]
    assert ArgValueParser.bound_list_if_singleton(["x"]) == ["x"]
    assert ArgValueParser.bound_tuple_if_singleton("x", elem_type=str) == ("x",)
    assert ArgValueParser.bound_tuple_if_singleton(("x",)) == ("x",)
    assert ArgValueParser.bound_set_if_singleton("x", elem_type=str) == {"x"}
    assert ArgValueParser.bound_set_if_singleton({"x"}) == {"x"}
    # value not matching elem_type is returned unchanged
    assert ArgValueParser.bound_list_if_singleton(5, elem_type=str) == 5
    # collections of allowed_type are returned unchanged
    assert ArgValueParser.bound_list_if_singleton((1, 2)) == (1, 2)

def test_ensure_list():
    assert ArgValueParser.ensure_list([1, 2]) == [1, 2]
    assert ArgValueParser.ensure_list((1, 2)) == [1, 2]
    assert ArgValueParser.ensure_list({1}) == [1]
    assert ArgValueParser.ensure_list("x") == ["x"]
    assert ArgValueParser.ensure_list(5) == [5]
    # default na handling: None kept as is
    assert ArgValueParser.ensure_list(None) is None

def test_ensure_tuple():
    assert ArgValueParser.ensure_tuple([1, 2]) == (1, 2)
    assert ArgValueParser.ensure_tuple("x") == ("x",)
    assert ArgValueParser.ensure_tuple(None) is None

def test_ensure_set():
    assert ArgValueParser.ensure_set([1, 2, 2]) == {1, 2}
    assert ArgValueParser.ensure_set("x") == {"x"}
    assert ArgValueParser.ensure_set(None) is None

def test_ensure_collection_na_handling():
    # na_converter built-ins
    assert ArgValueParser.ensure_list(None, na_converter='none') is None
    assert ArgValueParser.ensure_list(None, na_converter='empty') == []
    assert ArgValueParser.ensure_list(None, na_converter='single') == [None]
    # na_checker built-ins
    assert ArgValueParser.ensure_list(5, na_checker='always_na') == 5
    assert ArgValueParser.ensure_list(None, na_checker='never_na') == [None]
    # custom callables
    assert ArgValueParser.ensure_list('', na_checker=lambda x: x == '', na_converter=lambda x: ['na']) == ['na']

def test_ensure_collection_invalid_builtin_name():
    import pytest
    with pytest.raises(ValueError, match="Unknown built-in name"):
        ArgValueParser.ensure_list(None, na_checker='no_such_checker')
    with pytest.raises(ValueError, match="Unknown built-in name"):
        ArgValueParser.ensure_list(None, na_converter='no_such_converter')
