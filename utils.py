"""
    utils.py - utility functions for the project
"""


import datetime
import re
from pathlib import Path

import pandas as pd


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
    source_path=None,
    verbose=False,
):
    """
    append_entry_outtxt - append an entry to the outtxt file

    Args:
        prompt, string: the prompt to append
        response, string: the response to append
        out_path, string: the path to the outtxt file. If None, uses the default path.
        file_extension, string: the file extension of the outtxt file.
        model_name, (str, optional): the name of the model. Defaults to "".
        verbose, (bool, optional): Defaults to False.
    """
    source_path = Path(source_path) if source_path else Path(__file__)
    if out_path is None:
        cwd = Path.cwd()
        out_path = cwd / "out"
        out_path.mkdir(exist_ok=True)
        out_path = (
            out_path / f"apiQ__{source_path.stem}_{get_timestamp()}.{file_extension}"
        )
    else:
        out_path = (
            Path(out_path)
            / f"api_queries_{source_path.stem}_{get_timestamp()}.{file_extension}"
        )

    if not out_path.exists():
        with open(out_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(f"API QUERIES FOR {source_path.stem}\n\n")
            f.write(f"- {model_name}\n")
            f.write(f"- {get_timestamp()}\n")
    with open(out_path, "a", encoding="utf-8", errors="ignore") as f:
        f.write(f" ## {prompt}\n")
        f.write(f"Response: \n{response}\n")
        f.write("\n")
    if verbose:
        print(f"wrote to {out_path}")

    return out_path


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


def check_if_link(text: str, verbose=False):
    """
    check_if_link - check if a string is a link

    Args:
        text (str): the string to check
        verbose (bool, optional): . Defaults to False.

    Returns:
        bool: whether or not the string is a link
    """

    if re.findall(r"^https?://", text):
        if verbose:
            print(f"{text} is a link")
        return True
    else:
        if verbose:
            print(f"{text} is not a link")
        return False


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
    return df.convert_dtypes()
