# feilian

General data processing tool.

## Features

- More default values, less necessary arg.
- Encapsulation of panda dataframe for simple usage.

## Usage

### Read a file as dataframe

```python
from feilian import read_dataframe

input_file = ''     # file can be any csv, json or xlsx format
df = read_dataframe(input_file)
```

### Write dataframe to a file

```python
import pandas as pd
from feilian import save_dataframe

df = pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))
output_file = ''  # file can be any csv, json or xlsx format
save_dataframe(output_file, df)
```
