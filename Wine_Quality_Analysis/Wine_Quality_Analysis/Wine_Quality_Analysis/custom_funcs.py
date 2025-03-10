# custom_funcs.py

def custom_preprocessor(df):  # give the function a more informative name!!!
    """
    Processes the dataframe such that {insert intent here}. (Write better docstrings than this!!!!)

    Intended to be used under this particular circumstance, with {that other function} called before it, and potentially {yet another function} called after it, but optional.

    :param pd.DataFrame df: A pandas dataframe. Should contain the following columns:
        - col1
        - col2
    :returns: A modified dataframe.
    """
    return (df.groupby('col1').count()['col2'])

# notebook.ipynb

import pandas as pd
from projectname.config import data_path
from projectname.custom_funcs import custom_preprocessor

df = pd.read_csv(data_path)
processed = custom_preprocessor(df)