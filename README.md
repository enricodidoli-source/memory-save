# MemorySave: RAM Management in Python

MemorySave is a Python utility class created to handle RAM management efficiently by combining optimized disk serialization with cache cleaning.
It stores variables into a temporary folder, removes them from RAM storage and load them when needed.

---

## Key Features

- **Temp storing:** stores variables into a temporary folder (\temp\var\).
- **RAM cleaning:** removes variables from RAM storage.
- **Variables loading:** loads variables from temporary folder when needed.

---

## Quick Start

### Basic Usage

```python
# 0. Clone the repository and import the class 
!pip install git+https://github.com/enricodidoli-source/memory-save.git

import pandas as pd
from memory_utils import MemorySave

# 1. Initialize MemorySave with a temporary cache directory
mem = MemorySave(base_dir="./temp_var")

# 2. Simulate large data (e.g., a list of pandas DataFrames)
df_list = [pd.DataFrame({'col': range(1000000)}) for _ in range(3)]

# 3. Save to disk (Parquet for DataFrame lists, Pickle for general objects) 
# and automatically clear RAM
mem.save_and_clear(
    variables=[df_list], 
    variables_names=["heavy_dataset"], 
    clear=True,        # Deletes variables and triggers deep RAM cleanup
    force=True         # Overwrites if heavy_dataset is already cached
)

# 4. Inspect currently cached variables
mem.show_vars()

def df_mean(df_list=None, mem=None):
    if mem:
        # 5. Reload variables into local scope only when required for computation
        (df_list,) = mem.load_variables(["heavy_dataset"])
    for df in df_list:
        print(df.mean())
    return

# 6. DO NOT pass saved heavy variables (df_list) directly to functions 
# to avoid pointer duplication and memory retention in stack frames!
df_mean(df_list=None, mem=mem)

# 7. Safely remove specific cached variables or wipe the workspace upon completion
mem.remove_var(["heavy_dataset"])
mem.close()
```