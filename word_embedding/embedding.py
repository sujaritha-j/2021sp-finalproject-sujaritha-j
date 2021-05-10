import functools
import re
import warnings

import numpy as np
import os
from word_embedding.data import load_words, load_vectors, get_file_path

warnings.filterwarnings(action='ignore')


class WordEmbedding(object):
    """
    Word embedding class, learn a real-valued vector representation for a predefined fixed sized vocabulary
    from a corpus of text.
    """
    def __init__(self, words, vectors):
        """
        Inits WordEmedding class with words and vectors
        """
        self.words = words
        self.vectors = vectors
        self.word_vector_dict = dict(zip(words, vectors))

    def __call__(self, word):
        """
         Implements vocabulary lookup. The vocabulary lookup is O(1) because of the dictionary used.
         So however big the dataset is, it would be constant of time O(1).

         :param word(str): The 'word' for the vocabulary lookup.

         :return: (ndarray): Returns 'None' if the word is outside the vocabulary.
                            Returns a numpy vector is the word is in the vocabulary.

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
        """
        Instantiate an embedding from files.

        Example::embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')

        :param word_file(str): Filename of the words file
        :param vec_file(str) : Filename of the vectors file

        :return: cls(class object): Returns the class object
        """
        str_word_file = get_file_path(word_file)
        str_vec_file = get_file_path(vec_file)
        if os.path.exists(str_word_file) & os.path.exists(str_vec_file):
            return cls(load_words(str_word_file), load_vectors(str_vec_file))
        else:
            raise FileNotFoundError()

    @staticmethod
    def tokenize(text):
        """
        Get all words, including contractions from passed text.
        Example::embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')

        :param text(str): Text to tokenize

        :return: (list): word list from text after tokenization
        """
        # Get all "words", including contractions
        # eg tokenize("Hello, I'm Scott") --> ['hello', "i'm", 'scott']
        return re.findall(r"\w[\w']+", text.lower())

    def embed_document(self, document):
        """
        Convert text to vector, by finding vectors for each word and combining them.

        :param document(str): The document/text string with one or more words for which
                              we need vector representation

        :return: (ndarray): vector representation of document
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

