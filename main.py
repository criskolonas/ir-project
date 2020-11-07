from crawler import Crawler
import threading


if __name__ == '__main__':
    r1 = Crawler('https://www.roh.gr/',5,2,False,'DFS')
    r1.initializeCrawl()
