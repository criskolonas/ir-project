from crawler import Crawler
from indexer import Indexer

if __name__ == '__main__':
    r1 = Crawler('https://www.in.gr/', 10, 5, False, 'BFS')
    r1.initializeCrawl()
    ind = Indexer(r1.soups)
    ind.create_indexer()
    ind.tfidf('τραμπ')