# -*- coding: utf-8 -*-

from typing import Union, List, Any, Iterable, Callable, Set, Optional, Tuple

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
    def ensure_list(value: Any, allow_none=True) -> Optional[List[Any]]:
        """
        Ensure the value to be a list.
        If value is `None`, return `None` if `allow_none` is `True`, else return `[None]`.
        """
        if value is None and allow_none:
            if allow_none:
                return value
            return [value]
        if isinstance(value, list):
            return value
        if isinstance(value, (set, tuple)):
            return list(value)
        return [value]

    @staticmethod
    def ensure_tuple(value: Any, allow_none=True) -> Optional[Tuple[Any]]:
        """
        Ensure the value to be a tuple.
        If value is `None`, return `None` if `allow_none` is `True`, else return `(None, )`.
        """
        if value is None and allow_none:
            if allow_none:
                return value
            return (value,)
        if isinstance(value, tuple):
            return value
        if isinstance(value, (set, list)):
            return tuple(value)
        return (value,)

    @staticmethod
    def ensure_set(value: Any, allow_none=True) -> Optional[Set[Any]]:
        """
        Ensure the value to be a set.
        If value is `None`, return `None` if `allow_none` is `True`, else return `{None}`.
        """
        if value is None and allow_none:
            if allow_none:
                return value
            return {value}
        if isinstance(value, set):
            return value
        if isinstance(value, (tuple, list)):
            return set(value)
        return {value}
