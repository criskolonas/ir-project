from crawler import Crawler


if __name__ == '__main__':
    r1 = Crawler('https://www.instagram.com/',30,3,False,'DFS')
    r1.initializeCrawl()
