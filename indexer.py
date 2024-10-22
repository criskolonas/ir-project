import math
import re
from appearance import Appearance
from concurrent.futures import ThreadPoolExecutor


class Indexer:
    tokens = []
    inverted_index = {}

    def __init__(self, documents):
        self.documents = documents

    def add_document(self, doc):
        self.documents.append(doc)

    def clean_text(self):
        for doc in self.documents:
            doc.text = string_cleanup(doc)

    def find_tokens(self):
        for doc in self.documents:
            split_doc = doc.text.split()
            for word in split_doc:
                self.tokens.append(word)
        self.tokens = list(dict.fromkeys(self.tokens))  # remove duplicates

    #
    def create_indexer(self):
        self.clean_text()

        self.find_tokens()
        for i in range(len(self.tokens)):
            self.inverted_index[self.tokens[i]] = []

        for i in range(len(self.tokens)):
            for doc in self.documents:
                occur = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(self.tokens[i]), doc.text))
                self.inverted_index[self.tokens[i]].append(Appearance(doc, occur))

    def calculate_scores(self):
        for term in self.inverted_index.keys():
            for appearance in self.inverted_index[term]:
                appearance.score = tfidf(term, appearance, self.documents)


# does basic cleaning converts to lowercase and removes punctuation
def string_cleanup(doc):
    doc_lowercase = doc.text.lower()
    doc_no_punctuation = re.sub(r'[^\w\s]', '', doc_lowercase)
    return doc_no_punctuation


def tfidf(term, appear, documents):
    return tf(appear) * idf(term, documents)


def tf(appear):
    total_terms = len(appear.doc.text.split())
    if total_terms <= 0:
        return 0
    return appear.freq / float(total_terms)


def idf(term, documents):
    n_of_docs_containing = 0
    for doc in documents:
        if term in doc.text:
            n_of_docs_containing = n_of_docs_containing + 1
    ret = math.log(len(documents) / (1.0 + n_of_docs_containing))
    if (ret < 0.0):
        return 0.0
    return ret
