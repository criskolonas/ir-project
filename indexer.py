import re


def string_cleanup(doc):
    doc_lowercase = doc.lower()
    doc_no_punctuation = s = re.sub(r'[^\w\s]', '', doc_lowercase)
    return doc_no_punctuation


class Indexer:
    documents = []
    tokenized_docs = []

    def __init__(self, soup_objects):
        self.soup_objects = soup_objects

    def extract_text(self):
        for s_obj in self.soup_objects:
            s_obj.find_all('p')
            self.documents.append(s_obj.text)

    def create_indexer(self):
        inverted_index = {}
        self.tokenize_documents()
        for i in range(len(self.tokenized_docs)):
            for y in range(len(self.tokenized_docs[i])):
                name = self.tokenized_docs[i][y]
                inverted_index[name] = {}

        for key in inverted_index.keys():
            for i in range(len(self.documents)):
                inverted_index[key]["d" + str(i + 1)] = len(re.findall(key, self.documents[i]))

        return inverted_index

    def tokenize_documents(self):
        self.extract_text()
        for doc in self.documents:
            doc = string_cleanup(doc)
            self.tokenized_docs.append(doc.split())