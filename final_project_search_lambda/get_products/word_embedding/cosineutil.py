import numpy as np
import math


def cosine_similarity(x: object, y: object) -> object:
    """
    Takes 2 vectors x and y and calculates the cosine similarity according to the definition of the dot product.

    :param x(ndarray):  First vector used to calculate cosine similarity
    :param y(ndarray): Second vector used to calculate cosine similarity

    :return: (ndarray): Returns the cosine similarity between the 2 vectors
    """
    _y = np.array(y.replace("[", "").replace("]", "").split(), dtype=float)
    dot_product = np.dot(x, _y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(_y)
    return dot_product / (norm_x * norm_y)


def get_cosine_distance(x, y):
    """
    Takes 2 vectors x and y and calculates the cosine distance between the vectors.
    Lower the distance, more similar the vectors.

    :param x(ndarray): First vector used to calculate the cosine distance
    :param y(ndarray): Second vector used to calculate the cosine distance

    :return: distance(float): Returns the cosine distance between the 2 vectors
    """
    try:
        cosine_similarity_value = cosine_similarity(x, y)
        if math.isnan(cosine_similarity_value):
            cosine_similarity_value = 0
        distance = 1.0 - cosine_similarity_value
    except:  # catch all exception and return 1. the max value for the distance
        distance = 1
    return distance
