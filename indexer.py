from bs4 import BeautifulSoup


class Indexer:
    inverted_index = []

    def __init__(self, documents):
        self.documents = documents  # 2d array with document id and string of document's text

    def create_word_dictionary(self, documents):
        dictionary = list()
        for doc in documents:
            dictionary.append(doc.split())
        dictionary = list(set(dictionary))
        return dictionary
