import re
from bs4 import BeautifulSoup
from urllib import request

class Indexer:
    documents = []
    tokenized_docs = []
    inverted_index = {}

    def __init__(self,soup_objects):
        self.soup_objects = soup_objects

    def extract_text(self):
        for s_obj in self.soup_objects:
            s_obj.find_all('p')
            self.documents.append(s_obj.text)

    def create_indexer(self):


    def tokenize_documents(self):
        for doc in self.documents:
            doc = self.string_cleanup(doc)
            self.tokenized_docs.append(doc.split())

    def string_cleanup(self,doc):
        doc_lowercase = doc.lower()
        doc_no_punctuation = s = re.sub(r'[^\w\s]', '', doc_lowercase)
        return doc_no_punctuation

    def update_indexer(self):


if __name__ == '__main__':
    inde = Indexer()

