from ._typing import Union, Literal
import os
import io
import inspect
import chardet

_DEFAULT_CHUNK_SIZE = 1024

if 'should_rename_legacy' in inspect.signature(chardet.UniversalDetector).parameters:
    def _create_detector(should_rename_legacy: bool):
        return chardet.UniversalDetector(should_rename_legacy=should_rename_legacy)
else:
    def _create_detector(should_rename_legacy: bool):
        return chardet.UniversalDetector()

def detect_stream_encoding(stream: io.IOBase, chunk_size=_DEFAULT_CHUNK_SIZE, should_rename_legacy=True) -> str:
    detector = _create_detector(should_rename_legacy=should_rename_legacy)
    while True:
        raw = stream.read(chunk_size)
        if not raw:
            break
        detector.feed(raw)
        if detector.done:
            break
    detector.close()
    return detector.result.get('encoding')

def detect_text_encoding(raw: bytes, chunk_size=_DEFAULT_CHUNK_SIZE, should_rename_legacy=True) -> str:
    return detect_stream_encoding(io.BytesIO(raw), chunk_size=chunk_size, should_rename_legacy=should_rename_legacy)

def detect_file_encoding(path: Union[str, os.PathLike], chunk_size=_DEFAULT_CHUNK_SIZE, should_rename_legacy=True) -> str:
    with open(path, 'rb') as f:
        return detect_stream_encoding(f, chunk_size=chunk_size, should_rename_legacy=should_rename_legacy)

def get_file_encoding(path: Union[str, os.PathLike], encoding: Union[None, Literal['auto'], str] = None) -> str:
    if encoding == 'auto':
        encoding = detect_file_encoding(path)
    return encoding

def read_txt(path: Union[str, os.PathLike], encoding: Union[None, Literal['auto'], str] = None) -> str:
    if encoding == 'auto':
        with open(path, 'rb') as f:
            raw = f.read()
        encoding = detect_stream_encoding(io.BytesIO(raw))
        return raw.decode(encoding)
    with open(path, 'r', encoding=encoding) as f:
        return f.read()

def save_txt(path: Union[str, os.PathLike, io.IOBase], content: str, encoding: str = 'utf-8'):
    if isinstance(path, (str, os.PathLike)):
        f = open(path, 'w', encoding=encoding)
        should_close = True
    else:
        if isinstance(path, io.BytesIO):
            content = content.encode(encoding)
        f = path
        should_close = False
    try:
        f.write(content)
    finally:
        if should_close:
            f.close()

def write_txt(path: Union[str, os.PathLike], content: str, encoding: str = 'utf-8'):
    save_txt(path=path, content=content, encoding=encoding)
