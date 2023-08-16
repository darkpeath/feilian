# -*- coding: utf-8 -*-

from typing import Union, List, Any, Iterable, Callable, Set, Optional, Tuple, Literal, Dict, Hashable

_build_in_na_checkers = {
    'always_na': lambda x: True,
    'never_na': lambda x: False,
    'is_none': lambda x: x is None,
}
_NA_CHECKER_TYPES = Union[Callable[[Any], bool], Literal['always_na', 'never_na', 'is_none']]

_build_in_na_converters = {
    'none': lambda x: None,
    'self': lambda x: x,
    'empty': lambda x: [],
    'single': lambda x: [x],
}
_NA_CONVERTER_TYPES = Union[Callable[[Any], Any], Literal['none', 'self', 'empty', 'single']]

def _get_or_default(value: Any, mapping: Dict[Hashable, Any], default_key: Any) -> Any:
    if value is None:
        return mapping[default_key]
    return mapping.get(value, value)

class ArgValueParser(object):
    @classmethod
    def split_and_parse_strs(cls, strings: Union[List[str], str, None],
                             func: Callable[[str], Any] = None,
                             sep=',', do_trim=True, ignore_blank=True) -> Iterable[Any]:
        """
        split and parse multi string values
        :param strings:  list of strings
        :param func:     function to parse single string value
        :param sep:      seperator to split single string
        :param do_trim:  trim every word or not
        :param ignore_blank:    ignore blank or not; in some case, this must be `True`
        """
        if isinstance(strings, str):
            strings = [strings]
        if strings:
            for value in strings:
                for x in value.split(sep):
                    if do_trim:
                        x = x.strip()
                    if not x and ignore_blank:
                        continue
                    yield func(x) if func else x

    @classmethod
    def split_strs_to_set(cls, values: Union[List[str], str, None],
                          func: Callable[[str], Any] = None,
                          sep=',', do_trim=True, ignore_blank=True) -> Optional[Set[Any]]:
        """
        split multi string values as words to a set
        """
        return set(cls.split_and_parse_strs(values, func, sep, do_trim, ignore_blank))

    @classmethod
    def split_strs_to_list(cls, values: Union[List[str], str, None],
                           func: Callable[[str], Any] = None,
                           sep=',', do_trim=True, ignore_blank=True) -> Optional[List[Any]]:
        """
        split multi string values as words to a list
        """
        return list(cls.split_and_parse_strs(values, func, sep, do_trim, ignore_blank))

    @staticmethod
    def bound_collection_if_singleton(value: Any, collection_type: type,
                                      elem_type: Union[type, Tuple[type]] = (),
                                      allowed_type=(list, tuple, set)) -> Any:
        """
        if `value` is a singleton element, bound it with a collection type.
        :param value:       the input value may be bounded
        :param collection_type:     may be `list`, `tuple` or `set`
        :param elem_type:       if `value` is instance of `elem_type` but not instance of `allowed_type`, bound  it.
        :param allowed_type:    if `value` is instance of `allowed_type`, return the `value` unchanged.
        """
        if isinstance(value, allowed_type):
            return value
        if isinstance(value, elem_type):
            return collection_type([value])
        return value

    @classmethod
    def bound_list_if_singleton(cls, value: Any, elem_type: Union[type, Tuple[type]] = (),
                                allowed_type=(list, tuple, set)) -> Any:
        """
        If `value` is a singleton element, bound it to be a `list`.
        See more arg docs in `bound_collection_if_singleton()`.
        """
        return cls.bound_collection_if_singleton(value, collection_type=list,
                                                 elem_type=elem_type, allowed_type=allowed_type)

    @classmethod
    def bound_tuple_if_singleton(cls, value: Any, elem_type: Union[type, Tuple[type]] = (),
                                 allowed_type=(list, tuple, set)) -> Any:
        """
        If `value` is a singleton element, bound it to be a `tuple`.
        See more arg docs in `bound_collection_if_singleton()`.
        """
        return cls.bound_collection_if_singleton(value, collection_type=tuple,
                                                 elem_type=elem_type, allowed_type=allowed_type)

    @classmethod
    def bound_set_if_singleton(cls, value: Any, elem_type: Union[type, Tuple[type]] = (),
                               allowed_type=(list, tuple, set)) -> Any:
        """
        If `value` is a singleton element, bound it to be a `set`.
        See more arg docs in `bound_collection_if_singleton()`.
        """
        return cls.bound_collection_if_singleton(value, collection_type=set,
                                                 elem_type=elem_type, allowed_type=allowed_type)

    @staticmethod
    def ensure_collection(value: Any, expected_type: type, collection_type: Union[type, Tuple[type, ...]],
                          na_checker: _NA_CHECKER_TYPES = None, na_converter: _NA_CONVERTER_TYPES = None) -> Any:
        """
        Ensure the value to be a list, tuple or set.
        :param value:   any type value
        :param expected_type:       expected return type, can be list, tuple or set
        :param collection_type:     other collection type to be convert
        :param na_checker:      check if `value` is na, default is 'is_none'
                                str value means some built-in functions:
                                    always_na:  always treat the value as na
                                    never_na:   never treat the value as na
                                    is_none:    test if the value is `None`
        :param na_converter:    if `value` is na, return output of this function, default is 'self'
                                str value means some built-in functions:
                                    none:   `None`
                                    self:   the value no changed
                                    empty:  an empty list
                                    single: a single value list: `[value]`
        :return:    expected to be an instance of `expected_type`, or be `None` for some condition
        """
        na_checker = _get_or_default(na_checker, _build_in_na_checkers, 'is_none')
        if na_checker(value):
            na_converter = _get_or_default(na_converter, _build_in_na_converters, 'self')
            return na_converter(value)
        if isinstance(value, expected_type):
            return value
        if isinstance(value, collection_type):
            return expected_type(value)
        return expected_type([value])

    @classmethod
    def ensure_list(cls, value: Any, na_checker: _NA_CHECKER_TYPES = None,
                    na_converter: _NA_CONVERTER_TYPES = None) -> Optional[List[Any]]:
        """
        Ensure the value to be a list.
        See more arg docs in `ensure_collection()`.
        """
        return cls.ensure_collection(value, expected_type=list, collection_type=(tuple, set),
                                     na_checker=na_checker, na_converter=na_converter)

    @classmethod
    def ensure_tuple(cls, value: Any, na_checker: _NA_CHECKER_TYPES = None,
                     na_converter: _NA_CONVERTER_TYPES = None) -> Optional[Tuple[Any]]:
        """
        Ensure the value to be a tuple.
        See more arg docs in `ensure_collection()`.
        """
        return cls.ensure_collection(value, expected_type=tuple, collection_type=(list, set),
                                     na_checker=na_checker, na_converter=na_converter)

    @classmethod
    def ensure_set(cls, value: Any, na_checker: _NA_CHECKER_TYPES = None,
                   na_converter: _NA_CONVERTER_TYPES = None) -> Optional[Set[Any]]:
        """
        Ensure the value to be a set.
        See more arg docs in `ensure_collection()`.
        """
        return cls.ensure_collection(value, expected_type=set, collection_type=(list, tuple),
                                     na_checker=na_checker, na_converter=na_converter)

