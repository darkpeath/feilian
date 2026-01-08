from typing import Union, Literal
import os
import chardet

def detect_text_encoding(raw: bytes, should_rename_legacy=True) -> str:
    return chardet.detect(raw, should_rename_legacy=should_rename_legacy).get('encoding')

def detect_file_encoding(path: Union[str, os.PathLike], size=10000, should_rename_legacy=True) -> str:
    with open(path, 'rb') as f:
        raw = f.read(size)
    return detect_text_encoding(raw, should_rename_legacy=should_rename_legacy)

def get_file_encoding(path: Union[str, os.PathLike], encoding: Union[None, Literal['auto'], str] = None) -> str:
    if encoding == 'auto':
        encoding = detect_file_encoding(path)
    return encoding

def read_txt(path: Union[str, os.PathLike], encoding: Union[None, Literal['auto'], str] = None) -> str:
    if encoding == 'auto':
        with open(path, 'rb') as f:
            raw = f.read()
        encoding = detect_text_encoding(raw)
        return raw.decode(encoding)
    with open(path, 'r', encoding=encoding) as f:
        return f.read()

def save_txt(path: Union[str, os.PathLike], content: str, encoding: str = 'utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        f.write(content)

def write_txt(path: Union[str, os.PathLike], content: str, encoding: str = 'utf-8'):
    save_txt(path=path, content=content, encoding=encoding)
