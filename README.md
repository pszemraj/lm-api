# lm-api: Utilities large language model API queries

Some simple utilities for querying the large language model API. Currently known to be compatible with OpenAI's API and Goose's API.

## Usage

Command line script:

```
python query_api.py -i <input_file> -m 'gpt-j-6b' -o <output_dir>
```

This will query each row in the input file and output the results to the output directory using the gpt-j-6b model (on Goose API).

**IMPORTANT:** your API key must be set in the environment variable `GOOSE` and `OPENAI` or passed as an argument to the script with the `-k` flag.

## Installation

- `cd` to the directory containing this file and run `pip install -r requirements.txt`

A quick test can be run with the `test_goose_api.py` script.

---
