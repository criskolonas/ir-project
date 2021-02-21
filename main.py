from crawler import Crawler
from indexer import Indexer
from query_processor import QuerryProcessor
from document import  Document
from time import sleep
if __name__ == '__main__':

    # sleep(5.0)
    # print("THREAD-TIME!")
    r2 = Crawler('https://www.in.gr', 20, 5, True, 'BFS')
    r2.initializeCrawl()

    ind = Indexer(Crawler.documents)


    query = input("Enter your search query:")
    ind.add_document(Document('search_query',query))
    print('Building Indexer...')
    ind.create_indexer()
    print('Calculating TF-IDFs. May take a while.')
    ind.calculate_scores()

    qp = QuerryProcessor(ind.inverted_index,len(ind.documents))
    docs_with_cos_ = qp.compare_documents()
    docs_with_cos_ = sorted(docs_with_cos_, key=lambda x: x[1], reverse=True)#sorting based on cosine similarity scores
    print(f'Showing top results based on your query "{query}":')
    for doc in docs_with_cos_:
        print(doc[0].link)