from typing import Union, Literal
import os
import chardet

def read_txt(path: Union[str, os.PathLike], encoding: Union[None, Literal['auto'], str] = None) -> str:
    if encoding == 'auto':
        with open(path, 'rb') as f:
            raw = f.read()
        encoding = chardet.detect(raw)['encoding']
        return raw.decode(encoding)
    with open(path, 'r', encoding=encoding) as f:
        return f.read()

def save_txt(path: Union[str, os.PathLike], content: str, encoding: str = 'utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        f.write(content)

def write_txt(path: Union[str, os.PathLike], content: str, encoding: str = 'utf-8'):
    save_txt(path=path, content=content, encoding=encoding)
