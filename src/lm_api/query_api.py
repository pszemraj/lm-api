#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    query_vs_dataframe.py - loads a CSV/xlsx/JSON file using Pandas, then sends an API query for each row in <key_column> in the file. Outputs the query and response to a text file.

    python query_vs_dataframe.py -h for help
"""


import argparse
import logging
import os
import sys
import random
import time
from pathlib import Path

import openai
from tqdm import tqdm

from lm_api.utils import append_entry_outtxt, df_to_list, flex_load_pandas

logging.basicConfig(
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s %(message)s",
    filename=f"api_dataframe_query.log",
)
logger = logging.getLogger(__name__)


def query_terms(
    term_list,
    prefix: str = "",
    suffix: str = "",
    model_id: str = "text-davinci-003",
    n_tokens: int = 128,
    frequency_penalty: float = 0.15,
    presence_penalty: float = 0.05,
    temperature: float = 0.7,
    out_path: str or Path = None,
    source_path: str or Path = None,
    verbose=False,
):
    """
    query_terms - sends a query to the API for each term in the list

    :param term_list: list of terms to query
    :param str prefix: prefix to add to each query
    :param str suffix: suffix to add to each query
    :param str model_id: model id to use for the API query (default: text-davinci-003)
    :param int n_tokens: number of tokens to use for the API query (default: 128)
    :param float frequency_penalty: frequency penalty to use for the API query (default: 0.15)
    :param float presence_penalty: presence penalty to use for the API query (default: 0.05)
    :param float temperature: temperature to use for the API query (default: 0.7)
    :param strorPath out_path: path to the output file (default: None)
    :param strorPath source_path: path to the source file (default: None)
    :param bool verbose: verbose output (default: False)
    :return list: list of responses from the API
    """
    if verbose:
        print(f"querying {len(term_list)} terms")
    for term in tqdm(term_list, desc="querying terms", total=len(term_list)):

        time.sleep(random.random() * 2)
        query = f"{prefix} {term} {suffix}".strip()
        _query_token_count = int(len(query.split()) / 4)  # approx 4 tokens per word
        if verbose:
            print(f"querying {term}:\n\t{query}")

        # query the API
        completion = openai.Completion.create(
            engine=model_id,
            prompt=query,
            max_tokens=_query_token_count + n_tokens,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            temperature=temperature,
        )

        # remove the prefix and suffix from the query
        query = query.replace(prefix, "").replace(suffix, "")

        # append the response to the output text file
        out_file_path = append_entry_outtxt(
            query,
            completion.choices[0].text,
            out_path=out_path,
            model_name=model_id,
            source_path=source_path,
            verbose=verbose,
        )
    return out_file_path


def get_parser():
    """
    get_parser - a helper function for the argparse module
    """
    parser = argparse.ArgumentParser(
        description="Query a list of terms from a pandas-compatible file to a language model API"
    )

    parser.add_argument(
        "-i",
        "--input-file",
        required=False,
        default=None,
        type=str,
        help="name of the input file or link to the input file",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        required=False,
        default=None,
        type=str,
        help="path to directory to write output files (new folder created). Defaults to input-dir",
    )
    parser.add_argument(
        "-provider",
        "--provider-id",
        required=False,
        type=str,
        default="openai",
        help="provider to connect to for API. Defaults to openai (options: openai, goose)",
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        default=None,
        help="API key for the provider if needed (or set as environment variable OPENAI or GOOSE)",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        required=False,
        default="Explain the following concept(s) to a Master's student in the field:",
        type=str,
        help="prefix to add to each query (spaces added automatically)",
    )
    parser.add_argument(
        "-s",
        "--suffix",
        required=False,
        default="An acceptable solution to the problem would be similar to:",
        type=str,
        help="suffix to add to each query (spaces added automatically)",
    )
    parser.add_argument(
        "--simple",
        "--no_prefix_suffix",
        required=False,
        default=False,
        action="store_true",
        help="do not add a prefix or suffix to the query",
    )
    parser.add_argument(
        "-kc",
        "--key-column",
        required=False,
        default="terms",
        type=str,
        help="name of the column in the input file that contains the terms to query. Defaults to 'terms'",
    )
    parser.add_argument(
        "-m",
        "--model-id",
        required=False,
        default="text-davinci-003",
        type=str,
        help="model id to use for the API query. OpenAI models (text-davinci-003, ada, etc) Goose models (gpt-neo-20b, gpt-j-6b, etc). Defaults to text-davinci-003",
    )
    parser.add_argument(
        "-n",
        "--n-tokens",
        required=False,
        default=128,
        type=int,
        help="number of tokens to use for the API query (default: 128)",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        required=False,
        default=0.7,
        type=float,
        help="temperature to use for the API query (default: 0.7)",
    )
    parser.add_argument(
        "-f2",
        "--frequency-penalty",
        required=False,
        default=0.15,
        type=float,
        help="frequency penalty to use for the API query (default: 0.15)",
    )
    parser.add_argument(
        "-p2",
        "--presence-penalty",
        required=False,
        default=0.05,
        type=float,
        help="presence penalty to use for the API query (default: 0.05)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        default=False,
        action="store_true",
        help="verbose output",
    )
    return parser


if __name__ == "__main__":

    PROVIDERS = ["goose", "openai"]
    parser = get_parser()
    args = parser.parse_args()
    input_id = (
        Path(args.input_file)
        if args.input_file
        else Path.cwd() / "data" / "test_queries.xlsx"
    )
    output_dir = Path(args.output_dir) or Path.cwd() / "out"
    output_dir.mkdir(exist_ok=True)

    key_column = args.key_column
    prefix = args.prefix
    suffix = args.suffix
    if args.no_prefix_suffix:
        logger.info("no prefix or suffix added to queries")
        prefix = ""
        suffix = ""
    model_id = args.model_id
    key = args.key
    provider_id = args.provider_id
    assert provider_id in PROVIDERS, f"provider_id must be one of {PROVIDERS}"

    n_tokens = args.n_tokens
    frequency_penalty = args.frequency_penalty
    presence_penalty = args.presence_penalty
    verbose = args.verbose

    env_var = os.environ.get(provider_id.upper())
    openai.api_key = env_var if key is None else str(key)
    openai.api_base = (
        "https://api.goose.ai/v1"
        if provider_id == "goose"
        else "https://api.openai.com/v1"
    )
    engines = openai.Engine.list()

    """
    engines has the following structure:
    engines: {
      "data": [
        {
          "created": null,
          "id": "davinci-instruct-beta",
          "object": "engine",
          "owner": "openai",
          "permissions": null,
          "ready": true
        },
        ...
        ]
        // some stuff that doesn't matter
    }
    We access it via engines["data"][i]
    """
    engine_ids = [e["id"] for e in engines["data"]]

    if provider_id == "openai" and model_id not in engine_ids:
        print(
            f"{model_id} not found in openai.Engine.list(). Continue with text-davinci-003?"
        )
        if input("y/n: ") == "y":
            model_id = "text-davinci-003"
        else:
            print("Exiting. Use -m to specify a valid model id")
            sys.exit()

    if input_id.suffix == ".txt":
        with open(input_id, "r", encoding="utf-8", errors="ignore") as f:
            terms = f.readlines()
    else:
        # assume dataframe
        # load the dataframe
        df = flex_load_pandas(input_id)
        assert (
            key_column in df.columns
        ), f"key_column (-kc switch) must be in the dataframe columns"
        # get the list of terms
        terms = df_to_list(df, key_column, verbose=False)

    # query the API
    out_file_path = query_terms(
        term_list=terms,
        prefix=prefix,
        suffix=suffix,
        verbose=verbose,
        model_id=model_id,
        n_tokens=n_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        out_path=output_dir,
        source_path=input_id,
    )

    print(f"done, output file:\n\t{out_file_path}")
