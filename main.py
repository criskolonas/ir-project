from crawler import Crawler
import threading


if __name__ == '__main__':
    r1 = Crawler('https://www.instagram.com/',10,2,False,'BFS')
    print("Hello!")
    r1.crawl()
