import os

import numpy as np
import pandas as pd


def load_words(filename):
    """Load a file containing a list of words as a python list
    use case: data/words.txt
    :param str filename: path/name to file to load
    :rtype: list
    """
    w_list = []
    with open(filename, "r") as file:
        for line in file:
            w_list.extend(line.split())
    return w_list


def load_vectors(filename):
    """Loads a file containing word vectors to a python numpy array
    use case: `data/vectors.npy.gz`
    :param str filename:
    :returns: 2D matrix with shape (m, n) where m is number of words in vocab
        and n is the dimension of the embedding
    :rtype: ndarray
    """
    return np.load(filename)


def load_data(filename):
    """Load student response data in parquet format
    use case: data/project.parquet
    :param str filename:
    :returns: dataframe indexed on a hashed github id
    :rtype: DataFrame
    """
    # Get the hashed_id column from the parquet file to a pandas data frame
    df_parquet = pd.read_parquet(
        filename
    )
    df_parquet = df_parquet.sort_index()
    return df_parquet


def get_file_path(filename) -> str:
    """Takes the filename as the parameter and returns back the full path with the filename
    :param filename: str
    :rtype: str
    """
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.split(current_dir)[0]
    load_filename_path = os.path.join(parent_dir, 'data', filename)
    return load_filename_path
