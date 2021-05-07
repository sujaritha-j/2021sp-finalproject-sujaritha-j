import functools
import re
import warnings

import numpy as np
import os
from word_embedding.data import load_words, load_vectors, get_file_path

warnings.filterwarnings(action='ignore')


class WordEmbedding(object):

    def __init__(self, words, vectors):
        self.words = words
        self.vectors = vectors
        self.word_vector_dict = dict(zip(words, vectors))

    def __call__(self, word):
        """Embed a word. This is O(1) because we use dictionary. So however big the dataset is, it would be constant time -O(1).
        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """
        # Consider how you implement the vocab lookup.  It should be O(1).
        # check if the word exists
        if word is None:
            return np.zeros(self.vectors.shape[1])

        if word in self.word_vector_dict.keys():
            return np.array(self.word_vector_dict[word])
        else:
            return np.zeros(self.vectors.shape[1])

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instantiate an embedding from files
        Example::embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')
        :param cls: obj
        :param word_file : str
        :param vec_file : str
        :rtype: cls
        """
        str_word_file = get_file_path(word_file)
        str_vec_file = get_file_path(vec_file)
        if os.path.exists(str_word_file) & os.path.exists(str_vec_file):
            return cls(load_words(str_word_file), load_vectors(str_vec_file))
        else:
            raise FileNotFoundError()

    @staticmethod
    def tokenize(text):
        """Get all "words", including contractions from passed text.
        Example::embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')
        :param text: str
        :rtype: str
        """
        # Get all "words", including contractions
        # eg tokenize("Hello, I'm Scott") --> ['hello', "i'm", 'scott']
        return re.findall(r"\w[\w']+", text.lower())

    def embed_document(self, document):
        """Convert text to vector, by finding vectors for each word and combining
        :param str document: the document (one or more words) to get a vector
            representation for
        :return: vector representation of document
        :rtype: ndarray (1D)
        """
        if document is None or document == '':
            return np.zeros(self.vectors.shape[1])

        # vector_array = np.empty((0, 300), self.vectors.dtype)
        v_list = []
        for word in self.tokenize(document):
            v_list.append(self(word))

        if len(v_list) > 0:
            vector_array = functools.reduce(lambda a, b: a + b, v_list)
            return vector_array
        else:
            return np.zeros(self.vectors.shape[1])

