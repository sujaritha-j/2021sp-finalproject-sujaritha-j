from unittest import TestCase
from random import randint
import numpy
import numpy as np
import os
from word_embedding.cosineutil import get_cosine_distance, cosine_similarity
from word_embedding.embedding import WordEmbedding
import mock

class CosineUtilityTests(TestCase):

    def get_mock_data(self) -> object:
        """Create 2 vectors by randomly generating them for testing purposes.
        rtype: nparray, nparray"""
        vector_1 = np.random.randint(1, 100, 10)
        vector_2 = np.random.randint(1, 100, 10)
        return vector_1, vector_2

    def test_cosine_distance(self):
        """Ensure expected csci salt value is the same as what is retrieved from env file """
        vector_1, vector_2 = self.get_mock_data()
        result = get_cosine_distance(vector_1, vector_2)
        assert result is not None

    def test_cosine_distance_same_vectors(self):
        """Ensure expected csci salt value is the same as what is retrieved from env file """
        vector_1, vector_2 = self.get_mock_data()
        vector_3 = vector_1
        print(vector_1, vector_1)
        result = get_cosine_distance(vector_1, vector_3)
        print(result)
        assert round(result, 6) <= 0

    def test_cosine_distance_different_vectors(self):
        """Ensure expected csci salt value is the same as what is retrieved from env file """
        vector_1, vector_2 = self.get_mock_data()
        print(vector_1, vector_2)
        result = get_cosine_distance(vector_1, vector_2)
        assert result is not None

    def test_cosine_similarity(self):
        """Ensure expected csci salt value and what is retrieved from env file is different """
        vector_1, vector_2 = self.get_mock_data()
        cosine_value = cosine_similarity(vector_1, vector_2)
        assert cosine_value is not None


class WordEmbeddingTests(TestCase):

    def test_from_files_success(self):
        """Ensure file exists after being written successfully"""

        word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
        assert word_embedding is not None


    def test_from_files_failure(self):
        """Ensure that file does not exist after failure during write"""
        try:
            file_name = "words" + str(randint(0, 999999)) + ".txt"
            word_embedding = WordEmbedding.from_files(file_name, 'vectors.npy.gz')
            assert word_embedding is None
        except FileNotFoundError:
            assert 1 == 1

    def test_embed_document_success(self):
        document = 'All the worlds a stage, and all the men and women merely players'
        word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
        user_vector = word_embedding.embed_document(document)
        assert user_vector is not None

    def test_embed_document_failure(self):
        document = ''
        word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
        user_vector = word_embedding.embed_document(document)
        assert numpy.all(user_vector == 0)

    def test_word_vector_success(self):
        word = 'the'
        word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
        vector_for_word = word_embedding(word)

        assert vector_for_word is not None


class DataDownloadTaskTests(TestCase):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    LOCAL_ROOT = 'pset_5/data'
    S3_MOCKED_BUCKET = 'suji-cscie29-data'
    s3_data_path = 's3://cscie29-data/14a291ef/pset_5/yelp_data/*.csv'
    test_path = 'data/'
    ext = 'csv'

    @mock.patch('final_project_file_load.tasks.DataDownloadTask')
    @mock.patch('csci_utils.luigi.dask_target.CSVTarget')
    def test_data_download_success(self, csv_target, data_download_task):
        """ Testing Stylize success
        :return: boolean"""
        job = data_download_task(s3_data_path=self.s3_data_path)
        job.run()
        is_local_exists = csv_target(path=os.path.join(self.test_path, 'YelpReviews'), glob='part-*.' + self.ext)
        self.assertIsNotNone(is_local_exists)
