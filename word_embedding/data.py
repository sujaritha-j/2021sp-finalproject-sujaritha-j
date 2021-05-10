import os

import numpy as np
import pandas as pd


def load_words(filename):
    """
    Load a file containing a list of words as a python list.
    use case: data/words.txt

    :param filename(str): Path/filename of the file to convert to python list

    :return: w_list(list): Returns the word list
    """
    w_list = []
    with open(filename, "r") as file:
        for line in file:
            w_list.extend(line.split())
    return w_list


def load_vectors(filename):
    """
    Loads a file containing word vectors to a python numpy array
    use case: `data/vectors.npy.gz`

    :param filename(str): Path/filename of the file to be converted to a numpy array.

    :return: (ndarray): Returns the 2D matrix with shape (m, n) where m is number of words in vocab
                       and n is the dimension of the embedding
    """
    return np.load(filename)


def load_data(filename):
    """
    Load data in parquet format
    use case: data/project.parquet

    :param filename(str): Path and filename of the of the file to convert to dataframe

    :return: df_parquet(dataframe): Returns the dataframe sorted by the index
    """
    # Get the hashed_id column from the parquet file to a pandas data frame
    df_parquet = pd.read_parquet(
        filename
    )
    df_parquet = df_parquet.sort_index()
    return df_parquet


def get_file_path(filename) -> str:
    """
    Takes the filename as the parameter and returns back the full path with the filename

    :param filename(str): Filename for which we need the full path with the filename

    :return: load_filename_path(str): Returns the filename with the full path
    """
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.split(current_dir)[0]
    load_filename_path = os.path.join(parent_dir, 'data', filename)
    return load_filename_path
