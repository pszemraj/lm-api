#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    query-vs-dataframe.py - loads a CSV/xlsx/JSON file using Pandas, then sends an API query for each row in <key_column> in the file. Outputs the query and response to a text file.

    python query-vs-dataframe.py -h for help
"""


import argparse
import logging
import os
import random
import time
from os.path import join
from pathlib import Path

import openai
from tqdm import tqdm

from utils import append_entry_outtxt, df_to_list, flex_load_pandas

logging.basicConfig(
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s %(message)s",
    filename=f"api_dataframe_query.log",
)
logger = logging.getLogger(__name__)

def query_terms(
    term_list,
    prefix,
    suffix,
    verbose=False,
    model_id="gpt-neo-20b",
    n_tokens=128,
    frequency_penalty=0.3,
    presence_penalty=0.05,
    temperature=1,
    out_path=None,
):
    """
    query_terms - queries the API for each term in the term_list

    Args:
        term_list (list): list of terms to query
        prefix (str): prefix to add to each query
        suffix (str): suffix to add to each query
        verbose (bool, optional): _description_. Defaults to False.
        model_id (str, optional): _description_. Defaults to "gpt-neo-20b".
        n_tokens (int, optional): _description_. Defaults to 128.
        frequency_penalty (float, optional): _description_. Defaults to 0.3.
        presence_penalty (float, optional): _description_. Defaults to 0.05.
        temperature (int, optional): _description_. Defaults to 1.
        out_path (_type_, optional): _description_. Defaults to None.
    """
    if verbose:
        print(f"querying {len(term_list)} terms")
    for term in tqdm(term_list, desc="querying terms", total=len(term_list)):

        time.sleep(random.random() * 2)
        _query = f"{prefix} {term} {suffix}"
        _query_token_count = int(len(_query.split()) / 4)
        if verbose:
            print(f"querying {term}:\n\t{_query}")

        # query the API
        completion = openai.Completion.create(
            engine=model_id,
            prompt=_query,
            max_tokens=_query_token_count + n_tokens,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            temperature=temperature,
        )
        # append the response to the output text file
        append_entry_outtxt(
            _query,
            completion.choices[0].text,
            out_path=out_path,
            model_name=model_id,
            verbose=verbose,
        )


def get_parser():
    """
    get_parser - a helper function for the argparse module
    """
    parser = argparse.ArgumentParser(description="Split text by percent")

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
        default="goose",
        help="provider to connect to for API. Defaults to goose (openai is other)",
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        default=None,
        help="API key for the provider if needed",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        required=False,
        default="Explain the following Natural Language Processing (NLP) concept(s):",
        type=str,
        help="prefix to add to each query",
    )
    parser.add_argument(
        "-s",
        "--suffix",
        required=False,
        default=" An acceptable solution to the problem would be similar to:",
        type=str,
        help="suffix to add to each query",
    )
    parser.add_argument(
        "-kc",
        "--key-column",
        required=False,
        default="terms",
        type=str,
        help="name of the column in the input file that contains the terms to query",
    )
    parser.add_argument(
        "-m",
        "--model-id",
        required=False,
        default="gpt-neo-20b",  # gpt-j-6b
        type=str,
        help="model id to use for the API query",
    )
    parser.add_argument(
        "-n",
        "--n-tokens",
        required=False,
        default=128,
        type=int,
        help="number of tokens to use for the API query",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        required=False,
        default=0.7,
        type=float,
        help="temperature to use for the API query",
    )
    parser.add_argument(
        "-f2",
        "--frequency-penalty",
        required=False,
        default=0.15,
        type=float,
        help="frequency penalty to use for the API query",
    )
    parser.add_argument(
        "-p2",
        "--presence-penalty",
        required=False,
        default=0.05,
        type=float,
        help="presence penalty to use for the API query",
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
    input_id = Path(args.input_file) if args.input_file else Path.cwd() / 'data' / 'test_queries.xlsx'
    output_dir = args.output_dir or Path.cwd() / "out"
    output_dir.mkdir(exist_ok=True)

    key_column = args.key_column
    prefix = args.prefix
    suffix = args.suffix
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
    if provider_id == "openai" and model_id not in engines:
        logging.warning(
            f"model {model_id} not found in openai.Engine.list(), using text-davinci-002"
        )
        model_id = "text-davinci-002"
    # load the dataframe
    df = flex_load_pandas(input_id)
    assert (
        key_column in df.columns
    ), f"key_column (-kc switch) must be in the dataframe columns"
    # get the list of terms
    terms = df_to_list(df, key_column, verbose=False)

    # query the API
    query_terms(
        term_list=terms,
        prefix=prefix,
        suffix=suffix,
        verbose=verbose,
        model_id=model_id,
        n_tokens=n_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        out_path=output_dir,
    )

    print(f"done")
