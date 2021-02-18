import numpy as np
class QuerryProcessor:


    def __init__(self,query,indexer,d_n):
        self.d_n = d_n
        self.query = query
        self.inverted_index = indexer
    #creates and returns a numpy vector for the query made
    #the query is the last document of the indexer, meaning the last appearance of every term in the indexer dictionary
    def get_query_vector(self):
        tfid_list = []
        for term in self.inverted_index.keys():
            tfid_list.append(self.inverted_index[term][self.d_n-1].score)
        return np.array(tfid_list)
    #calculates the cosine similarity and return a list of top-k documents closest to the given query
    def calculate_cosine_similarity(self,k,query_vector):
        top_k_docs = []


