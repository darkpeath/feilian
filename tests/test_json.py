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
