from urllib import request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import time


class Crawler:
    queue = []
    visited = []
    soups = []

    # Constructor
    def __init__(self, url, n, threads, warm_start, algo):
        self.url = url
        self.n = n
        self.threads = threads
        self.warm_start = warm_start
        self.algo = algo

    # Crawler initializer
    def initializeCrawl(self):
        t1 = time.perf_counter()
        if not self.warm_start:
            self.visited.clear()
            self.queue.clear()

        self.visited.append(self.url)
        self.queue = self.getLinks(self.url)

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.crawlStart, self.queue)
        t2 = time.perf_counter()
        print(t2 - t1)
        print(len(self.visited))

    # Method to generate links from given url and create "soup" objects for each link
    def getLinks(self, url):
        with request.urlopen(url) as response:
            try:
                html = response.read().decode('utf-8')
                soup = BeautifulSoup(html,"html.parser")
                self.soups.append(soup.prettify())
                pattern = re.compile(
                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                links = re.findall(pattern, html)
                links_clean = list(dict.fromkeys(links))
                return links_clean
            except Exception as exc:
                print(exc)

    # Crawling using Selected Algorithm
    def crawlStart(self, url):
        if len(self.visited) >= self.n:
            return 0
        if url in self.visited:
            self.queue.pop(0)
        else:
            self.visited.append(url)
            links = self.getLinks(url)
            if self.algo == "DFS":
                for link in links:
                    self.queue.insert(0, link)
            elif self.algo == "BFS":
                for link in links:
                    self.queue.append(link)
