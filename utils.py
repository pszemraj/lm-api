"""
    utils.py - utility functions for the project
"""


from pathlib import Path
import re

import pandas as pd
import datetime


def get_timestamp(verbose=False):
    """
    get_timestamp - get the current timestamp

    Parameters
    ----------
    verbose : bool, optional, default is False

    Returns
    -------
    str
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H")
    if verbose:
        print(f"timestamp: {timestamp}")
    return timestamp


def append_entry_outtxt(
    prompt,
    response,
    out_path=None,
    file_extension="md",
    model_name: str = "",
    verbose=False,
):
    """
    append_entry_outtxt - append a string to the output text file

    Parameters
    ----------
    out_txt : str
        the path to the output text file
    entry : str
        the string to append
    """
    if out_path is None:
        cwd = Path.cwd()
        out_path = (
            cwd / "out" / f"api_queries_{model_name}_{get_timestamp()}.{file_extension}"
        )
    else:
        out_path = (
            Path(out_path)
            / f"api_queries_{model_name}_{get_timestamp()}.{file_extension}"
        )
    with open(out_path, "a", encoding="utf-8", errors="ignore") as f:
        f.write(f" ## {prompt}\n")
        f.write(f"Response: \n{response}\n")
        f.write("\n")
    if verbose:
        print(f"wrote to {out_path}")


def df_to_list(df, column, verbose=False):
    """
    df_to_list - convert a dataframe to a list

    Parameters
    ----------
    df : pandas.DataFrame
        the dataframe to convert
    col_name : str
        the column name to convert
    verbose : bool, optional, default is False
        if true, prints the list

    Returns
    -------
    list, the list of values
    """

    df_list = df[column].tolist()
    if verbose:
        print(f"converted {column} to list: \n{df_list}")
    return df_list


def flex_load_pandas(path_or_url, verbose=False):
    """
    flex_load_pandas - load a pandas dataframe with the correct function depending on the extension.

    Parameters
    ----------
    path_or_url : str,
        the path or url to load
    verbose : bool, optional, default is False

    Returns
    -------
    pandas.DataFrame
    """
    # convert Path to string
    if isinstance(path_or_url, Path):
        path_or_url = str(path_or_url.resolve())

    # handle dropbox urls
    if path_or_url.startswith("https://www.dropbox.com"):
        if verbose:
            print("loading from dropbox url")
        path_or_url = path_or_url.replace("dl=0", "dl=1")
    # handle gdrive urls
    if path_or_url.startswith("https://drive.google.com"):
        if verbose:
            print("loading from google drive url")
        path_or_url = path_or_url.replace("view?usp=sharing", "uc?export=download")

    # load the relevant dataframe depending extension with re findall. need to also account for URLs with extension NOT at the end
    if re.findall(r"\.csv$", path_or_url) or re.findall(r"\.csv\?dl=1$", path_or_url):
        df = pd.read_csv(path_or_url)
    elif re.findall(r"\.xlsx$", path_or_url) or re.findall(
        r"\.xlsx\?dl=1$", path_or_url
    ):
        df = pd.read_excel(path_or_url)
    elif re.findall(r"\.json$", path_or_url) or re.findall(
        r"\.json\?dl=1$", path_or_url
    ):
        df = pd.read_json(path_or_url)
    else:
        ValueError(
            "ERROR! file extension not recognized. Please use .csv, .xlsx or .json"
        )

    if verbose:
        print("loaded pandas dataframe: \n", df)
        print(df.info())
    return df
