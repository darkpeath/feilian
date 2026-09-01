import json
from pathlib import Path
import feilian

a = [
  {"a": 1, "b": "k1", "c": 0.2},
  {"a": 2, "b": "k2", "c": 5.3},
  {"a": 3, "b": "k3", "c": 4.7},
  {"a": 4, "b": "k4", "c": 22.0},
]

b = {
    "a1": {
        "s1": "ail",
        "i2": 5
    },
    "a2": {
        "s2": "ttj",
        "i2": 8
    },
    "a3": {
        "s3": "jjl",
        "i3": 6,
        "t": "908"
    }
}

def test_read_jsonl():
    path = Path(__file__).parent.joinpath("a.jsonl")
    d = feilian.read_json(path)
    assert d == a

def test_read_json():
    path = Path(__file__).parent.joinpath("b.json")
    d = feilian.read_json(path)
    assert d == b

def test_read_big_json():
    path = Path(__file__).parent.joinpath("b.json")
    g = feilian.read_big_json(path)
    d = {k: v for k, v in g}
    assert d == b

def test_read_big_jsonl():
    path = Path(__file__).parent.joinpath("a.jsonl")
    g = feilian.read_big_json(path)
    d = list(g)
    assert d == a

def test_read_big_json_limit():
    path = Path(__file__).parent.joinpath("a.jsonl")
    g = feilian.read_big_json(path, limit=2)
    assert list(g) == a[:2]
    path = Path(__file__).parent.joinpath("b.json")
    g = feilian.read_big_json(path, limit=1)
    assert dict(g) == {"a1": b["a1"]}

def test_read_json_missing_file():
    import pytest
    path = Path(__file__).parent.joinpath("no_such_file.json")
    with pytest.raises(FileNotFoundError):
        feilian.read_json(path)

def test_save_and_read_json(tmp_path):
    for name in ["data.json", "data.jsonl"]:
        path = tmp_path / name
        feilian.save_json(path, a)
        assert feilian.read_json(path) == a

def test_read_big_json_top_level_array(tmp_path):
    data = [[1, 2], [3], {"a": [4, 5]}, "x", None, True, 1.5]
    path = tmp_path / "data.json"
    path.write_text(json.dumps(data))
    g = feilian.read_big_json(path)
    assert list(g) == data
    assert g.data_type == 'list'

def test_read_big_json_nested_values(tmp_path):
    data = {
        "k1": {"a": [1, 2, {"b": "x"}], "c": None, "d": True, "e": 1.5},
        "k2": [{"f": [3]}],
        "k3": "plain",
        "k4": [[1, 2], [3]],
    }
    path = tmp_path / "data.json"
    path.write_text(json.dumps(data))
    g = feilian.read_big_json(path)
    assert dict(g) == data
    assert g.data_type == 'dict'

def test_save_json_jsonl_rejects_non_iterable(tmp_path):
    import pytest
    with pytest.raises(ValueError):
        feilian.save_json(tmp_path / "data.jsonl", {"a": 1})
    with pytest.raises(ValueError):
        feilian.save_json(tmp_path / "data.jsonl", "text")

def test_save_json_jsonl_accepts_any_iterable(tmp_path):
    path = tmp_path / "data.jsonl"
    feilian.save_json(path, tuple(a))
    assert feilian.read_json(path) == a
    feilian.save_json(path, (x for x in a))
    assert feilian.read_json(path) == a

def test_stream_json_reader_is_abstract():
    import pytest
    from feilian.json import StreamJsonReader
    with pytest.raises(TypeError):
        StreamJsonReader("x.json")

def test_write_json_alias(tmp_path):
    path = tmp_path / "data.json"
    feilian.write_json(path, a)
    assert feilian.read_json(path) == a

def test_read_json_jsonl_suffix_with_regular_json(tmp_path):
    # a .jsonl file that actually contains a pretty-printed json
    path = tmp_path / "data.jsonl"
    path.write_text(json.dumps(b, indent=2))
    assert feilian.read_json(path) == b

def test_read_jsonl_with_blank_lines(tmp_path):
    path = tmp_path / "data.jsonl"
    path.write_text('{"a":1}\n\n{"a":2}\n  \n{"a":3}\n\n')
    assert feilian.read_json(path) == [{"a": 1}, {"a": 2}, {"a": 3}]

def test_read_big_jsonl_with_blank_lines(tmp_path):
    path = tmp_path / "data.jsonl"
    path.write_text('{"a":1}\n\n{"a":2}\n\n{"a":3}\n')
    assert list(feilian.read_big_json(path)) == [{"a": 1}, {"a": 2}, {"a": 3}]
    # limit only counts valid lines
    assert list(feilian.read_big_json(path, limit=2)) == [{"a": 1}, {"a": 2}]
