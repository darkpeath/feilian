# feilian

General data processing tool.

## Features

- More default values, less necessary arg.
- Encapsulation of panda dataframe for simple usage.

## Usage

### Process data with pandas dataframe

#### Read a file as dataframe

```python
import feilian

input_file = ''     # file can be any csv, json, parquet or xlsx format
df = feilian.read_dataframe(input_file)
```

#### Write dataframe to a file

```python
import feilian
import pandas as pd

df = pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))
output_file = ''  # file can be any csv, json, parquet or xlsx format
feilian.save_dataframe(output_file, df)
```

#### Iter a dataframe with a progress bar

```python
import feilian
import pandas as pd

df = pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))
feilian.iter_dataframe(data=df, progress_bar="process")
```

#### Extract sample from a dataframe

```python
import feilian
import pandas as pd

df = pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))
sample = feilian.extract_dataframe_sample(size=2, shuffle=True)
```

#### Test text value in dataframe

```python
import feilian

s = ''

# test if s is na or empty string
feilian.is_empty_text(s)

# test if s is not na and non-empty string
feilian.is_nonempty_text(s)

# test if s is na or blank string
feilian.is_blank_text(s)

# test if s is not na and non-blank string
feilian.is_non_blank_text(s)
```

#### Merge same id rows to one row

```python
import feilian
import pandas as pd

df = pd.DataFrame([
    {"a": "1", "b": "2", "c": "5"},
    {"a": "2", "b": 6, "c": "8"},
    {"a": "1", "b": 8, "c": "9"},
])

res = feilian.merge_dataframe_rows(df, col_id="a", join_sep=",")
```

### IO for json file

#### Read a json file

```python
import feilian

input_file = ''
data = feilian.read_json(input_file)
```

#### Write a json file

```python
import feilian

data = [
    {"a": "1", "b": "2", "c": "5"},
    {"a": "2", "b": 6, "c": "8"},
    {"a": "1", "b": 8, "c": "9"},
]
output_file = ''
feilian.save_dataframe(output_file, data)
```

### Datetime format

```python
import feilian
import datetime

d = datetime.datetime.now()

# format a date string
feilian.format_date(d, sep='-')

# format a time string
feilian.format_time(d, fmt='%H:%M:%S')
```

### Process dict

#### Flatten dict value

```python
import feilian

data = {
    "a": 12,
    "b": ["4", "s"],
    "c": {
        "l": 0,
        "j": {
            "se": "we",
            "t": 5,
        }
    },
    "f": 7,
    "g": {
        "ts": "9w",
        "j2": 8,
    },
    "w": {
        "s": {
            "ge": 89,
            "00": "ej",
        },
        "r": {
            "le": 33,
            "03": "ef",
        }
    },
    "sk": {
        "a": "23",
        "b": {
            "s": 9,
            "g": 0,
            "p": 4,
        },
        "c": {
            "s": 8,
            "t": "w",
            "j": "23",
        }
    },
}
res = feilian.flatten_dict(data, frozen={"g", "w.s", "sk."}, exclude="f")
```

### Process args 

```python
from feilian import ArgValueParser

value = ''

# split value
ArgValueParser.split_strs_to_list(value)
ArgValueParser.split_strs_to_set(value)

# bound value
ArgValueParser.bound_set_if_singleton(value)
ArgValueParser.bound_tuple_if_singleton(value)
ArgValueParser.bound_list_if_singleton(value)

# force value type
ArgValueParser.ensure_set(value)
ArgValueParser.ensure_list(value)
ArgValueParser.ensure_tuple(value)
```

