from crawler import Crawler

if __name__ == '__main__':
    r1 = Crawler('https://www.in.gr/', 200, 5, False, 'BFS')
    r1.initializeCrawl()
