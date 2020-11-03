import urllib.request
import urllib.response
import re


class Crawler:



    #Constructor
    def __init__(self, url, n, threads, warm_start, algo):
        self.url = url
        self.n = n
        self.threads = threads
        self.warm_start = warm_start
        self.algo = algo

    def initializeCrawl(self):

        if not self.warm_start:
            self.visited.clear();

        with urllib.request.urlopen(self.url) as response:
            html = response.read().decode('utf-8')
            links = self.findLinks(html)
        print(*links,sep = '\n')
        self.visited.append(self.url)
        self.queue.append(self.url)

        if self.algo == 'BFS':
            self.crawlBFS(links);

        if self.algo == 'DFS':
            self.crawlDFS(links);

    #Crawling using Breadth First Search of links
    def crawlBFS(self, links):
        for link in links[0:self.n+1]:
            pass

    #Crawling using Depth First Search of links
    def crawlDFS(self, links):
        pass

    #Using regular expression to find all links in a single link's source file.
    def findLinks(self, link):
        pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  #regex for href=
        return re.findall(pattern, link)

