import requests
from bs4 import BeautifulSoup
import re
import time
from document import Document
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

"""Method to find link format using regex and to delete the duplicate links
Returns clean links"""


def remove_duplicates(links):
    links_clean = []
    for link in links:
        match = re.search("(?P<url>https?://[^\s]+)", link)
        if match is not None:
            links_clean.append((match.group("url")))
        links_clean = list(dict.fromkeys(links_clean))
    return links_clean


"""Function that finds all text in paragraphs from soup object"""


def parseInfo(soup):
    texts = ''
    for p in soup.findAll('p'):
        texts += p.text
    return texts


class Crawler:
    new_size_visited = 0
    new_size_queue = 0

    """Constructor"""

    def __init__(self, url, n, threads, warm_start, algo):
        self.url = url
        self.n = n
        self.threads = threads
        self.warm_start = warm_start
        self.algo = algo
        self.visited = []
        self.queue = Queue()
        self.documents = []

    """Crawler initializer"""

    def initializeCrawl(self):
        t1 = time.perf_counter()
        self.warmStartCheck()
        self.queue.put(self.url)
        self.crawl()
        self.write_file()
        t2 = time.perf_counter()
        print("Time Elapsed: {} s.".format(t2 - t1))
        exit(0)

    """Crawl method"""
    def crawl(self):
        while len(self.visited) <= (self.n + self.new_size_visited):
            url = self.queue.get()
            ThreadPoolExecutor(max_workers=self.threads).submit(self.requestUrl, url)

    """Function that makes a request from a url"""
    def requestUrl(self, url):
        try:
            r = requests.get(url)
            self.callbackContinue(r)
        except Exception:
            print(url)

    """The callback function - general function method of the threadpool executor"""

    def callbackContinue(self, response):
        if response is None:
            self.queue.get()
        else:
            time.sleep(0.02)
            result = response
            url = result.url
            self.visited.append(url)
            # print("crawling {}".format(url))
            soup = BeautifulSoup(result.content, "lxml")
            if result.status_code == 200:
                doc = Document(url, parseInfo(soup))
                self.documents.append(doc)
                self.findLinks(soup)
                self.queue.get()
            else:
                self.findLinks(soup)
                self.queue.get()

    """Method that finds links from given file, and adds them to 
    visited or queue list respectively"""

    def findLinks(self, soup):
        links = []
        for link in soup.find_all('a', href=True):
            links.append(link.get("href"))
        links = remove_duplicates(links)
        if self.algo == "BFS":
            for link in reversed(links):
                self.queue.put(link)
        elif self.algo == "DFS":
            for link in links:
                self.queue.put(link)

    """Check for warm_start variable.
    If True, erase both .txt files and start crawling from begining
    If False, continue from the first line-link in the queue.txt until n number of crawls. """

    def warmStartCheck(self):
        if self.warm_start:
            open("visited.txt", "w").close()
            open("queue.txt", "w").close()
        else:
            # queue_links = []
            with open("visited.txt", "r", encoding='utf-8') as visited_txt:
                with open("queue.txt", "r", encoding='utf-8') as queue_txt:
                    txt_links = visited_txt.readlines()
                    if len(txt_links) == 0:
                        print("File is Empty, thus -False- parameter is not allowed.\nPlease try again!")
                        exit(3)
                    for line in txt_links:
                        line = re.sub("\\n+", "", line)
                        self.visited.append(line)
                    queue_links = queue_txt.readlines()
                    # for i in range(self.n):
                    #     queue_links.append(queue_txt.readline())
                    if len(queue_links) == 0:
                        print("Queue is Empty, thus -False- parameter is not allowed.\nPlease try again!")
                        exit(4)
                    for line in queue_links:
                        line = re.sub("\\n+", "", line)
                        self.queue.put(line)
            self.url = self.queue.get()
            self.new_size_visited = len(self.visited)

    """Method that writes to files"""

    def write_file(self):
        # if dont exist creates and appends too
        visited_txt = open("visited.txt", "a+", encoding='utf-8')
        queue_txt = open("queue.txt", "a+", encoding='utf-8')
        counter_visited = self.new_size_visited
        counter_queue = self.new_size_queue
        for i in range(counter_visited, len(self.visited)):
            visited_txt.write(self.visited[i] + "\n")
        for i in range(counter_queue, self.queue.qsize()):
            queue_txt.write(self.queue.get() + "\n")
