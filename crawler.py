import urllib.request
import urllib.response
import re
from bs4 import BeautifulSoup

class Crawler:

    queue = []
    visited = []


    #Constructor
    def __init__(self, url, n, threads, warm_start, algo):
        self.url = url
        self.n = n
        self.threads = threads
        self.warm_start = warm_start
        self.algo = algo

    def initializeCrawl(self):
        if not self.warm_start:
            self.visited.clear()
        
        links = self.generateUrl(self.url)
        self.visited.append(self.url)
        self.parseHTML(self.url)
        for link in links:
            self.queue.append(link)

        if self.algo == 'BFS':
            self.crawlBFS(self.queue)

        if self.algo == 'DFS':
            self.crawlDFS(self.queue)

        print(self.visited)
        print(self.queue)


    #Crawling using Breadth First Search of links
    def crawlBFS(self, queue):
        for url in queue:
            if len(self.visited) >= self.n:
                break
            self.visited.append(url)
            links = self.generateUrl(url)
            for link in links:
                queue.append(link)

    #Crawling using Depth First Search of links
    def crawlDFS(self, queue):
        for url in queue:
            if len(self.visited) >= self.n:
                break
            self.visited.append(url)
            self.parseHTML(url)


            links = self.generateUrl(url)
            for link in links:
                queue.insert(0, link)

    #Using regular expression to find all links in a single link's source file.
    def findLinks(self, link):
        pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  #regex for href=
        return re.findall(pattern, link)

    #Function generating all links from a given url
    def generateUrl(self,url):
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            links = self.findLinks(html)
        return links

    def parseHTML(self, link):
        with urllib.request.urlopen(link) as response:
            linkHTML = BeautifulSoup(response, 'html.parser')
            try:
                print(linkHTML.html.title)
            except AttributeError:
                print(link)