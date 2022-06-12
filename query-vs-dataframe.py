#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    query-vs-dataframe.py - loads a CSV file and queries it using Pandas, then each row is a query to API
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
    format="%(asctime)s %(message)s",
    filename=f"api_dataframe_query.log",
)
logger = logging.getLogger(__name__)

src_links = {
    "causality_terms": "https://www.dropbox.com/s/gbc0ne8rukkoj7z/summaries-setA.xlsx?dl=1",
}


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
    query_terms - query the API for each term in the list
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
                            verbose=verbose)


def get_parser():
    """
    get_parser - a helper function for the argparse module
    """
    parser = argparse.ArgumentParser(description="Split text by percent")

    parser.add_argument(
        "-i",
        "--input-file",
        required=True,
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
        '-provider',
        '--provider-id',
        required=False,
        type=str,
        default="goose",
        help="provider to connect to for API. Defaults to goose (openai is other)",
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
        "-m",
        "--model-id",
        required=False,
        default="gpt-neo-20b", # gpt-j-6b
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
    input_id = Path(args.input_file)
    output_dir = args.output_dir or os.getcwd()
    output_dir = join(output_dir, "out")
    os.makedirs(output_dir, exist_ok=True)

    prefix = args.prefix
    suffix = args.suffix
    model_id = args.model_id
    provider_id = args.provider_id
    assert provider_id in PROVIDERS, f"provider_id must be one of {PROVIDERS}"
    if provider_id == "openai":
        model_id = "text-davinci-002"
    n_tokens = args.n_tokens
    frequency_penalty = args.frequency_penalty
    presence_penalty = args.presence_penalty
    verbose = args.verbose

    env_var = os.environ.get(provider_id.upper())
    openai.api_key = env_var
    openai.api_base = "https://api.goose.ai/v1"
    # load the dataframe
    df = (
        flex_load_pandas(src_links[input_id])
        if input_id in src_links.keys()
        else flex_load_pandas(input_id)
    )

    # get the list of terms
    terms = df_to_list(df, "terms", verbose=False)

    # query the API
    query_terms(
        terms,
        prefix,
        suffix,
        verbose=verbose,
        model_id=model_id,
        n_tokens=n_tokens,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    print(f"done")
