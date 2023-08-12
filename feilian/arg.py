# -*- coding: utf-8 -*-

from typing import Union, List, Any, Iterable, Callable, Set, Optional

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

