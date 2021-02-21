import math

import numpy as np


class QuerryProcessor:

    def __init__(self, indexer, d_n):
        self.d_n = d_n
        self.inverted_index = indexer

    def calculate_cosine_similarity(self,vector1,vector2):
        dot_product = sum(p * q for p, q in zip(vector1, vector2))
        magnitude = math.sqrt(sum([val ** 2 for val in vector1])) * math.sqrt(sum([val ** 2 for val in vector2]))
        if not magnitude:
            return 0
        return dot_product / magnitude
    # calculates the cosine similarity and return a list of top-k documents closest to the given query
    def compare_documents(self):
        top_k_docs = []
        tfid_query_list = []
        for term in self.inverted_index.keys():
            tfid_query_list.append(self.inverted_index[term][self.d_n-1].score)
        query_vector = np.array(tfid_query_list)
        for i in range(self.d_n-1):
            tfid_doc_list = []
            for term in self.inverted_index.keys():
                tfid_doc_list.append(self.inverted_index[term][i].score)
            doc_vector = np.array(tfid_doc_list)
            print(self.calculate_cosine_similarity(query_vector,doc_vector))