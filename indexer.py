from bs4 import BeautifulSoup
import re


class Indexer:
    inverted_index = []

    def string_cleanup(self,doc):
        doc_lowercase = doc.lower()
        doc_no_punctuation = s = re.sub(r'[^\w\s]', '', doc_lowercase)
        return doc_no_punctuation

    def create_word_dictionary(self, documents):
        dictionary = list()
        for doc in documents:
            doc = self.string_cleanup(doc)
            doc_words = doc.split()
            for word in doc_words:
                dictionary.append(word)
        dictionary = list(set(dictionary))
        print(dictionary)
