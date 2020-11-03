import urllib.request
import urllib.response
import re


class Crawler:
    def __init__(self, url, n, threads, warm_start, algo):
        self.url = url
        self.n = n
        self.threads = threads
        self.warm_start = warm_start
        self.algo = algo

    def crawl(self):
        with urllib.request.urlopen(self.url) as response:
            html = response.read().decode('utf-8')
            links = self.findLinks(html)
            print(*links, sep="\n")

        if self.algo == 'BFS':
            self.runBFS();

        if self.algo == 'DFS':
            self.runDFS();

    def runBFS(self):
        pass

    def runDFS(self):
        pass

    def findLinks(self, link):
        pattern = re.compile(r'href=[\'"]?([^\'" >]+)')  #regex for href=
        return re.findall(pattern, link)
