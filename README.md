<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/lm-api.svg?branch=main)](https://cirrus-ci.com/github/<USER>/lm-api)
[![ReadTheDocs](https://readthedocs.org/projects/lm-api/badge/?version=latest)](https://lm-api.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/lm-api/main.svg)](https://coveralls.io/r/<USER>/lm-api)
[![PyPI-Server](https://img.shields.io/pypi/v/lm-api.svg)](https://pypi.org/project/lm-api/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/lm-api.svg)](https://anaconda.org/conda-forge/lm-api)
[![Monthly Downloads](https://pepy.tech/badge/lm-api/month)](https://pepy.tech/project/lm-api)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/lm-api)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# lm-api

> Utilities large language model API queries

## Usage

Command line scripts are located in `src/lm_api/`. For example, run

```
python query_api.py -i <input_file> -m 'gpt-j-6b' -o <output_dir>
```

This will query each row in the input file and output the results to the output directory using the gpt-j-6b model (on Goose API).

**IMPORTANT:** your API key must be set in the environment variable `GOOSE` and `OPENAI` or passed as an argument to the script with the `-k` flag.

## Installation

After cloning, `cd` into the `lm-api` directory and run

```bash
pip install -e .
```

A quick test can be run with the `src/lm_api/test_goose_api.py` script.

---
