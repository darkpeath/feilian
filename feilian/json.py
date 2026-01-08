# -*- coding: utf-8 -*-

from typing import Dict, List, Union, Any
from pathlib import Path
import os
import abc
import json
from decimal import Decimal
from .io import ensure_parent_dir_exist
from .txt import get_file_encoding
try:
    import ijson
except ImportError as e:
    ijson = None

def _read_json(filepath: Union[str, os.PathLike], jsonl: bool, encoding='utf-8', **kwargs):
    """
    The actual read function.
    """
    encoding = get_file_encoding(filepath, encoding=encoding)
    with open(filepath, encoding=encoding) as f:
        if jsonl:
            return [json.loads(x, **kwargs) for x in f]
        else:
            return json.load(f, **kwargs)

def _is_jsonl(filepath: Union[str, os.PathLike], jsonl: bool = None) -> bool:
    if jsonl is None:
        filepath = Path(filepath)
        jsonl = filepath.suffix.lower() == '.jsonl'
    return jsonl

def read_json(
    filepath: Union[str, os.PathLike],
    jsonl: bool = None,
    encoding: str = 'auto',
    **kwargs
) -> Union[Dict[str, Any], List[Any]]:
    """
    An agent for `json.load()` with some default value.
    """
    jsonl = _is_jsonl(filepath, jsonl)
    try:
        return _read_json(filepath, jsonl=jsonl, encoding=encoding, **kwargs)
    except Exception as e:
        # if failed, try again with different arg `jsonl`
        try:
            return _read_json(filepath, jsonl=not jsonl, encoding=encoding, **kwargs)
        except Exception:
            raise e

def save_json(
    filepath: Union[str, os.PathLike],
    data: Union[Dict[str, Any], List[Any]],
    jsonl: bool = None,
    encoding: str = 'utf-8',
    newline: str = '\n',
    indent: int = 2,
    ensure_ascii: bool = False,
    **kwargs
):
    """
    An agent for `json.dump()` with some default value.
    """
    jsonl = _is_jsonl(filepath, jsonl)
    if jsonl and not isinstance(data, list):
        # data should be a list
        raise ValueError("data should be a list when save as jsonl format")
    ensure_parent_dir_exist(filepath)
    with open(filepath, 'w', encoding=encoding, newline=newline) as f:
        if jsonl:
            for x in data:
                f.write(json.dumps(x, ensure_ascii=ensure_ascii, **kwargs))
                f.write(newline)
        else:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, **kwargs)

def write_json(
    filepath: Union[str, os.PathLike],
    data: Union[Dict[str, Any], List[Any]],
    jsonl: bool = None,
    encoding: str = 'utf-8',
    newline: str = '\n',
    indent: int = 2,
    ensure_ascii: bool = False,
    **kwargs
):
    save_json(
        filepath=filepath,
        data=data,
        jsonl=jsonl,
        encoding=encoding,
        newline=newline,
        indent=indent,
        ensure_ascii=ensure_ascii,
        **kwargs
    )


class _JsonNode:
    def __init__(self, type: str = '', parent: '_JsonNode' = None):
        self._type = ''
        self._value = None
        self._parent = parent
        if type:
            self.type = type

    def clear(self):
        if self._type == 'map':
            self._value.clear()
        elif self._type == 'array':
            self._value.clear()

    @property
    def parent(self):
        return self._parent

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if self._type:
            raise ValueError('type is already set')
        self._type = value
        if value == 'map':
            self._value = {}
        elif value == 'array':
            self._value = []

    @property
    def value(self):
        if not self._type:
            raise ValueError('type is not set')
        if self._type == 'dummy':
            assert isinstance(self._value, _JsonNode)
            return self._value.value
        if self._type == 'map':
            assert isinstance(self._value, dict)
            return {k: v.value for k, v in self._value.items()}
        if self._type == 'array':
            assert isinstance(self._value, list)
            return [v.value for v in self._value]
        return self._value

    @value.setter
    def value(self, value):
        if not self._type:
            raise ValueError('type is not set')
        if self._type in ['dummy', 'map', 'array']:
            raise RuntimeError('cannot set value for dummy, map, array')
        self._value = value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

class StreamJsonReader(abc.ABC):
    """
    Iterate over a json file.
    """
    def __init__(self, filepath: Union[str, os.PathLike], encoding: str = None, limit: int = float('inf')):
        self.filepath = filepath
        self.encoding = encoding
        self.limit = limit
        self._data_type = ''  # dict or list

    @property
    def data_type(self):
        return self._data_type

    def __iter__(self):
        raise NotImplementedError

class BigJsonReader(StreamJsonReader):
    def __iter__(self):
        with open(self.filepath, 'rb') as f:
            parser = ijson.parse(f)
            dummy = node = _JsonNode('')
            cnt = 0
            for prefix, event, value in parser:
                if event == 'start_map':
                    if node.type == 'array':
                        child = _JsonNode(type='map', parent=node)
                        node._value.append(child)
                        node = child
                    else:
                        node.type = 'map'
                elif event == 'end_map':
                    node = node.parent
                elif event == 'start_array':
                    node.type = 'array'
                elif event == 'end_array':
                    node = node.parent
                elif event == 'map_key':
                    assert node.type == 'map', f"{event} {value} {prefix}"
                    child = _JsonNode(parent=node)
                    node._value[value] = child
                    node = child
                else:
                    assert event in ['null', 'boolean', 'integer', 'double', 'number', 'string']
                    if isinstance(value, Decimal):
                        value = float(value)
                    if node.type == 'array':
                        child = _JsonNode(type=event, parent=node)
                        child.value = value
                        node._value.append(child)
                    else:
                        assert not node.type
                        node.type = event
                        node.value = value
                        node = node.parent
                if node == dummy and event not in ['start_map', 'start_array']:
                    assert node.type in ['map', 'array']
                    if node.type == 'map':
                        value = node.value
                        assert isinstance(value, dict)
                        assert len(value) == 1
                        k, v = list(value.items())[0]
                        self._data_type = 'dict'
                        yield k, v
                        node.clear()
                    elif node.type == 'array':
                        value = node.value
                        assert isinstance(value, list)
                        assert len(value) == 1
                        self._data_type = 'list'
                        yield value[0]
                        node.clear()
                    cnt += 1
                    if cnt >= self.limit:
                        break

class JsonlReader(StreamJsonReader):
    @property
    def data_type(self):
        return 'list'

    def __iter__(self):
        with open(self.filepath, encoding=self.encoding) as f:
            for i, line in enumerate(f, 1):
                yield json.loads(line)
                if i >= self.limit:
                    break

def read_big_json(
    filepath: Union[str, os.PathLike],
    jsonl: bool = None,
    encoding: str = 'auto',
) -> StreamJsonReader:
    jsonl = _is_jsonl(filepath, jsonl)
    encoding = get_file_encoding(filepath, encoding=encoding)
    if jsonl:
        return JsonlReader(filepath, encoding=encoding)
    else:
        if ijson is None:
            raise ImportError('ijson is not installed')
        return BigJsonReader(filepath)

