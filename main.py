from crawler import Crawler
from indexer import Indexer
from query_processor import QuerryProcessor
from document import  Document
from time import sleep
if __name__ == '__main__':

    # sleep(5.0)
    # print("THREAD-TIME!")
    r2 = Crawler('https://www.in.gr', 10, 5, True, 'BFS')
    r2.initializeCrawl()

    ind = Indexer(Crawler.documents)


    query = input("Enter your search query")
    ind.add_document(Document('search_query',query))

    ind.create_indexer()
    ind.calculate_scores()
    for term in ind.inverted_index.keys():
        print(term)
        for app in ind.inverted_index[term]:
            print(app.score, '\n')

    qp = QuerryProcessor(ind.inverted_index,len(ind.documents))
    qp.compare_documents()