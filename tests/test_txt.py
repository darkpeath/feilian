# -*- coding: utf-8 -*-

import io
import feilian

def test_save_and_read_txt(tmp_path):
    path = tmp_path / "a.txt"
    content = "hello\nworld\n"
    feilian.save_txt(path, content)
    assert feilian.read_txt(path, encoding="utf-8") == content

def test_write_txt_alias(tmp_path):
    path = tmp_path / "a.txt"
    feilian.write_txt(path, "abc")
    assert feilian.read_txt(path) == "abc"

def test_read_txt_auto_encoding_utf8(tmp_path):
    path = tmp_path / "a.txt"
    content = "中文内容 mixed with ascii\n"
    feilian.save_txt(path, content, encoding="utf-8")
    assert feilian.read_txt(path, encoding="auto") == content

def test_read_txt_auto_encoding_gb18030(tmp_path):
    path = tmp_path / "a.txt"
    content = "这是一段比较长的中文文本，用来帮助编码检测器正确识别编码。\n" * 5
    path.write_bytes(content.encode("gb18030"))
    assert feilian.read_txt(path, encoding="auto") == content

def test_read_txt_auto_encoding_empty_file(tmp_path):
    # detection returns None for empty input, should fallback instead of crashing
    path = tmp_path / "a.txt"
    path.write_bytes(b"")
    assert feilian.read_txt(path, encoding="auto") == ""

def test_detect_file_encoding(tmp_path):
    path = tmp_path / "a.txt"
    path.write_bytes("plain ascii text".encode("utf-8"))
    encoding = feilian.detect_file_encoding(path)
    assert encoding is not None

def test_detect_text_encoding():
    raw = "编码检测样例文本，检测器需要足够多的字节。".encode("utf-8")
    encoding = feilian.detect_text_encoding(raw)
    assert encoding.lower().replace("-", "") == "utf8"

def test_detect_stream_encoding():
    raw = "编码检测样例文本，检测器需要足够多的字节。".encode("utf-8")
    encoding = feilian.detect_stream_encoding(io.BytesIO(raw))
    assert encoding.lower().replace("-", "") == "utf8"

def test_get_file_encoding(tmp_path):
    path = tmp_path / "a.txt"
    path.write_bytes(b"abc")
    # non-auto values are passed through unchanged
    assert feilian.get_file_encoding(path, encoding="gbk") == "gbk"
    assert feilian.get_file_encoding(path, encoding=None) is None
    # auto triggers detection
    assert feilian.get_file_encoding(path, encoding="auto") != "auto"
