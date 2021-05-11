from unittest import TestCase
from random import randint
import numpy
import numpy as np
import os
from word_embedding.cosineutil import get_cosine_distance, cosine_similarity
from word_embedding.embedding import WordEmbedding
import mock


class CosineUtilityTests(TestCase):
    """
    Class that contains all the methods/test cases for testing the CosineUtilities
    """
    def get_mock_data(self) -> object:
        """
        Create 2 vectors by randomly generating them for testing purposes.

        return: vector1(nparray), vector2(nparray): Returns the 2 generated numpy vectors.
        """
        vector_1 = np.random.randint(1, 100, 10)
        vector_2 = np.random.randint(1, 100, 10)
        return vector_1, vector_2

    def test_cosine_distance(self):
        """
        Ensure expected csci salt value is the same as what is retrieved from env file

        return: (boolean): Returns boolean value based on if we get a cosine distance value
        """
        vector_1, vector_2 = self.get_mock_data()
        result = get_cosine_distance(vector_1, vector_2)
        assert result is not None

    def test_cosine_distance_same_vectors(self):
        """
        Ensure expected csci salt value is the same as what is retrieved from env file

        return: (boolean): Returns boolean value based on the cosine distance
        """
        vector_1, vector_2 = self.get_mock_data()
        vector_3 = vector_1
        print(vector_1, vector_1)
        result = get_cosine_distance(vector_1, vector_3)
        print(result)
        assert round(result, 6) <= 0

    def test_cosine_distance_different_vectors(self):
        """
        Ensure expected csci salt value is different from what is retrieved from env file by calculating
        cosine distance

        return: (boolean): Returns boolean value based on the cosine distance
        """
        vector_1, vector_2 = self.get_mock_data()
        print(vector_1, vector_2)
        result = get_cosine_distance(vector_1, vector_2)
        assert result is not None

    def test_cosine_similarity(self):
        """
        Test cosine similarity between the randomly generated vectors - vector1 and vector2

        return: (boolean): Returns boolean value based on the cosine similarity value
        """
        vector_1, vector_2 = self.get_mock_data()
        cosine_value = cosine_similarity(vector_1, vector_2)
        assert cosine_value is not None


class WordEmbeddingTests(TestCase):
    """
    Class that contains all the methods/test cases for WordEmbedding
    """
    def test_from_files_success(self):
        """
        Ensure file exists after being written successfully

        return: (boolean): Returns 'True' if the file exist or 'False' otherwise
        """

        word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
        assert word_embedding is not None


    def test_from_files_failure(self):
        """
        Ensure that file does not exist after failure during write

        return: (boolean): Returns 'True' if file does not exist after failure otherwise returns 'False'
        """
        try:
            file_name = "words" + str(randint(0, 999999)) + ".txt"
            word_embedding = WordEmbedding.from_files(file_name, 'vectors.npy.gz')
            assert word_embedding is None
        except FileNotFoundError:
            assert 1 == 1

    def test_embed_document_success(self):
        """
        Tests the success of embed_document by passing a document and checking to see if it returns a vector

        :return: (boolean): Returns 'True' if user_vector is returned, 'False' if it returns None.
        """
        document = 'All the worlds a stage, and all the men and women merely players'
        word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
        user_vector = word_embedding.embed_document(document)
        assert user_vector is not None

    def test_embed_document_failure(self):
        """
        Tests the failure of embed_document by passing a null document and checking to see if it returns a zero vector

        :return: (boolean): Returns 'True' if it retyrns 0, 'False' otherwise.
        """
        document = ''
        word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
        user_vector = word_embedding.embed_document(document)
        assert numpy.all(user_vector == 0)

    def test_word_vector_success(self):
        """
        Checks to see if a vetor is returned when we pass a word.

        :return: (boolean): Returns 'True' if it retyrns a not None value, 'False' otherwise.
        """
        word = 'the'
        word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
        vector_for_word = word_embedding(word)

        assert vector_for_word is not None

