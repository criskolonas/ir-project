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
            self.tokens.append(doc.split())

    def create_indexer(self):
        for i in range(len(self.tokens)):
            for doc in self.documents:
                self.inverted_index[self.tokens[i]] = list()
                occur = len(re.findall(self.tokens[i],doc))
                if(occur>0):
                    self.inverted_index[self.tokens[i]] = Appearance(doc,occur)



#does basic cleaning converts to lowercase and removes punctuation
def string_cleanup(doc):
    doc_lowercase = doc.lower()
    doc_no_punctuation  = re.sub(r'[^\w\s]', '', doc_lowercase)
    return doc_no_punctuation

