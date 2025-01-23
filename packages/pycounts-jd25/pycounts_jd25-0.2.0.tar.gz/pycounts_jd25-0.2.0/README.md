# pycounts_jd25

[![codecov](https://codecov.io/github/jdaduica/pycounts_jd25/graph/badge.svg?token=01X3OJTTOQ)](https://codecov.io/github/jdaduica/pycounts_jd25)

Calculate word counts in a text file!

Author:Julian Daduica

Year: 2025

## Installation

```bash
$ pip install pycounts_jd25
```

## Usage

`pycounts_jd25` can be used to count words in a text file and plot results
as follows:

```python
from pycounts_jd25.pycounts_jd25 import count_words
from pycounts_jd25.plotting import plot_words
import matplotlib.pyplot as plt

file_path = "test.txt"  # path to your file
counts = count_words(file_path)
fig = plot_words(counts, n=10)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. 
Please note that this project is released with a Code of Conduct. 
By contributing to this project, you agree to abide by its terms.

## License

`pycounts_jd25` was created by Julian Daduica. It is licensed under the terms
of the MIT license.

## Credits

`pycounts_jd25` was created with 
[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and 
the `py-pkgs-cookiecutter` 
[template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
