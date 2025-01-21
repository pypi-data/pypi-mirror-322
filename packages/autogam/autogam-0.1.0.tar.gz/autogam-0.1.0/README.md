# autogam

Automate the Creation of Generalized Additive Models (GAMs)

## Installation

```bash
$ pip install autogam
```

## Usage

### Example 1: Fitting AutoGAM on a Random Dataset

```python
import numpy as np
import pandas as pd
from autogam.autogam import AutoGAM

# Generate a random dataset
df_random = pd.DataFrame({
    'x1': np.random.uniform(0, 10, 100),
    'x2': np.random.uniform(0, 10, 100),
    'y': np.random.uniform(0, 10, 100)
})

# Fit the model using AutoGAM
ag_random = AutoGAM(df_random, 'y')

# Display the model summary
ag_random.summary()

# Display the performance metrics
ag_random.print()
```

### Example 2: Fitting AutoGAM on the `df_autos` Dataset

```python
import pandas as pd
from statsmodels.gam.tests.test_penalized import df_autos
from autogam.autogam import AutoGAM

# Use the `df_autos` dataset from statsmodels
ag_autos = AutoGAM(df_autos, 'city_mpg')

# Display the model summary
ag_autos.summary()

# Display the performance metrics
ag_autos.print()
```

## License

`autogam` was created by Chitu Okoli. It is licensed under the terms of the MIT license.

## Credits

`autogam` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
