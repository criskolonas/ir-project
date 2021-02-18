from crawler import Crawler
from crawler1 import Crawler1
from indexer import Indexer
from document import  Document
from time import sleep
if __name__ == '__main__':
    # r1 = Crawler('https://www.in.gr/', 50, 5, False, 'BFS')
    # r1.initializeCrawl()
    # sleep(5.0)
    # print("THREAD-TIME!")
    r2 = Crawler1('https://www.in.gr/', 50, 5, False, 'BFS')
    r2.initializeCrawl()
    # documents = []
    # d1 = Document('www.instagram.gr','Python is a 2000 made-for-TV horror movie directed by RichardClabaugh. The film features several cult favorite actors, including William Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy, Keith Coogan, Robert Englund')
    # d2 = Document('www.google.gr','Python is a very nice programming programming programming language William Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy, Keith Coogan, Robert Englund')
    # d3 = Document('www.google.gr','Python is a very nice programming programming programming language William Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy, Keith Coogan, Robert Englund')
    # d4 = Document('www.google.gr','Python is a very nice programming programming programming language William Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy, Keith Coogan, Robert Englund')
    # d5 = Document('www.google.gr','Python is a very nice programming programming programming language William Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy, Keith Coogan, Robert Englund')
    # d6 = Document('www.google.gr','Python is a very nice programming programming programming language William Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy, Keith Coogan, Robert Englund')
    #
    #
    # documents.append(d1)
    # documents.append(d2)
    # documents.append(d3)
    # documents.append(d4)
    # documents.append(d5)
    # documents.append(d6)
    # #
    # for doc in Crawler1.documents:
    #     print(doc.text)
    #     print("-------")
    # ind = Indexer(Crawler1.documents)
    # ind.create_indexer()
    # ind.calculate_scores()
    # for term in ind.inverted_index.keys():
    #     print(term)
    #     for app in ind.inverted_index[term]:
    #         print(app.score,'\n')