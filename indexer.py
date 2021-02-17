import math
import re
from appearance import Appearance

class Indexer:
    tokens = []
    inverted_index = {}

    def __init__(self,documents):
        self.documents = documents

    def clean_text(self):
        for doc in self.documents:
            doc = string_cleanup(doc)

    def find_tokens(self):
        for doc in self.documents:
            split_doc = doc.text.split()
            for word in split_doc:
                self.tokens.append(word)
        self.tokens = list(dict.fromkeys(self.tokens))#remove duplicates

    def create_indexer(self):
        self.find_tokens()
        for i in range(len(self.tokens)):
            self.inverted_index[self.tokens[i]] = []

        for i in range(len(self.tokens)):
            for doc in self.documents:
                occur = len(re.findall(self.tokens[i],doc.text))
                if(occur>0):
                    self.inverted_index[self.tokens[i]].append(Appearance(doc,occur))

    def tf(self,appear):
        total_terms = len(appear.doc.text.split())
        return appear.freq / float(total_terms)
    def idf(self,term):
        n_of_docs_containing = 0
        for doc in self.documents:
            if term in doc.text:
                n_of_docs_containing= n_of_docs_containing+1
        ret = math.log(len(self.documents) / (1.0 + n_of_docs_containing))
        if (ret < 0.0):
            return 0.0
        return ret

    def calculate_scores(self):
        for term in self.inverted_index.keys():
            for appearance in self.inverted_index[term]:
                appearance.score = self.tfidf(term,appearance)


    def tfidf(self,term,appear):
        return self.tf(appear) * self.idf(term)


#does basic cleaning converts to lowercase and removes punctuation
def string_cleanup(doc):
    doc_lowercase = doc.lower()
    doc_no_punctuation  = re.sub(r'[^\w\s]', '', doc_lowercase)
    return doc_no_punctuation

