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

# lm-api

> Command-line utilities for querying large language models

This repo is built around making is easy to run a set of queries against a large language model (LM) and get back a set of results via CLI, but also has basic Python API functionality.

Queries are expected to be in a pandas-compatible format, and results are written to a text file with markdown formatting for easy viewing/sharing.

## Installation

After cloning, `cd` into the `lm-api` directory and run

```bash
# create a virtual environment (optional)
pip install -e .
```

Alternatively, directly install via pip+git:

```bash
# create a virtual environment (optional)
pip install git+https://github.com/pszemraj/lm-api.git
```

A quick test can be run with the `src/lm_api/test_goose_api.py` script.

## On API Keys

You will need an API key for each provider you want to query. Currently, the following providers are supported:

- [Goose](https://goose.ai/)
- [OpenAI](https://beta.openai.com/playground)

API keys can be set in the environment variables `GOOSE` and `OPENAI` or passed as an argument to the script with the `-k` flag.

## Usage

Command line scripts are located in `src/lm_api/`. And become installed as CLI commands. Currently, the commands are limited to `lm-api`. **IMPORTANT: your API key must be set in the environment variable `GOOSE` and `OPENAI` or passed as an argument to the script with the `-k` flag.**

An example:

```bash
lm-api -i data/test_queries.xlsx -o ./my-test-folder
```

This will run the queries in `data/test_queries.xlsx` and write the results to a `.md` file in `my-test-folder/` in your current working directory. There are many options for the script, which can be viewed with the `-h` flag (e.g. `lm-api -h`).

```bash
usage: lm-api [-h] [-i INPUT_FILE] [-o OUTPUT_DIR] [-provider PROVIDER_ID] [-k KEY] [-p PREFIX] [-s SUFFIX] [-simple]
              [-kc KEY_COLUMN] [-m MODEL_ID] [-n N_TOKENS] [-t TEMPERATURE] [-f2 FREQUENCY_PENALTY]
              [-p2 PRESENCE_PENALTY] [-v]
```

## TODO / Roadmap

_Note: this is a work in progress, and the following is a running list of things that need to be done. This may and likely will be updated._

- [ ] adjust the `--prefix` and `--suffix` flags to a "prompt engine" switch that can augment/update the prompt with a variety of options (e.g. `--prompt-engine=prefix` or `--prompt-engine=prefix+suffix`)
- [ ] create simple CLI that does not require a query file
- [ ] validate performance as package / adjust as needed (i.e. import `lm_api` should work)
- [ ] setup tests

---

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
