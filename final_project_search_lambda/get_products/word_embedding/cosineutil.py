import numpy as np
import math


def cosine_similarity(x: object, y: object) -> object:
    """Takes 2 vectors x and y and returns the cosine similarity according to the definition of the dot product
    :param x: ndarray
    :param y: ndarray
    :rtype: ndarray
    """
    _y = np.array(y.replace("[", "").replace("]", "").split(), dtype=float)
    dot_product = np.dot(x, _y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(_y)
    return dot_product / (norm_x * norm_y)


def get_cosine_distance(x, y):
    """Takes 2 vectors x and y and returns the distance between the vectors. Lower the distance, the vectors are more similar.
    :param x: ndarray
    :param y: ndarray
    :rtype: float
    """
    try:
        cosine_similarity_value = cosine_similarity(x, y)
        if math.isnan(cosine_similarity_value):
            cosine_similarity_value = 0
        distance = 1.0 - cosine_similarity_value
    except:  # catch all exception and return 1. the max value for the distance
        distance = 1
    return distance
