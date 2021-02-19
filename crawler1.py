import requests
from bs4 import BeautifulSoup
import re
import time
from document import Document
from concurrent.futures import ThreadPoolExecutor


# Method to find link format using regex and to delete the duplicate links
# Returns clean links
def remove_duplicates(links):
    links_clean = []
    for link in links:
        match = re.search("(?P<url>https?://[^\s]+)", link)
        if match is not None:
            links_clean.append((match.group("url")))
        links_clean = list(dict.fromkeys(links_clean))
    return links_clean


# def check_if_link_in_file(link):
#     with open("visited.txt") as visited_txt:
#         lines = [line.rstrip() for line in visited_txt]
#         for line in lines:
#             if link == line:
#                 return True
#     return False


def requestUrl(url):
    try:
        r = requests.get(url)
        return r
    except Exception as ex:
        print("Exception from " + url + ": " + str(ex))
        return None


def parseInfo(soup):
    texts = ''
    for p in soup.findAll('p'):
        texts += p.text + '\n'
    return texts


class Crawler1:
    queue = []
    visited = []
    documents = []
    new_size_visited = 0
    new_size_queue = 0

    # Constructor
    def __init__(self, url, n, threads, warm_start, algo):
        self.url = url
        self.n = n
        self.threads = threads
        self.warm_start = warm_start
        self.algo = algo

    # Crawler1 initializer
    def initializeCrawl(self):
        t1 = time.perf_counter()
        self.warmStartCheck()
        self.crawl(self.url)
        self.write_file()
        t2 = time.perf_counter()
        print("Time Elapsed: {} s.".format(t2 - t1))
        print(len(self.visited) == (self.n + self.new_size_visited))

    # Crawl method
    def crawl(self, url):
        while len(self.visited) < (self.n + self.new_size_visited):
            print("Target url: {}".format(self.url))
            if url in self.visited:
                self.queue.pop(0)
            else:
                print("Crawling url: {}".format(url))
                self.visited.append(url)
                with ThreadPoolExecutor(max_workers=self.threads) as executor:
                    task = executor.submit(requestUrl, url)
                    task.add_done_callback(self.callbackContinue)
                url = self.queue[0]

    def callbackContinue(self, url):
        try:
            result = url.result()
            soup = BeautifulSoup(result.content, "lxml")
            if result.status_code == 200:
                doc = Document(url, parseInfo(soup))
                self.documents.append(doc)
                self.findLinks(soup)
                self.queue.pop(0)
            else:
                self.findLinks(soup)
                self.queue.pop(0)
        except Exception as ex:
            print(url.url + str(ex))
        except UnicodeEncodeError as er:
            print(url.url + str(er))

    def findLinks(self, soup):
        links = []
        for link in soup.find_all('a', href=True):
            links.append(link.get("href"))
        links = remove_duplicates(links)
        if self.algo == "DFS":
            for link in links:
                self.queue.insert(0, link)
        elif self.algo == "BFS":
            for link in links:
                self.queue.append(link)

    def warmStartCheck(self):
        if self.warm_start:
            visited_txt = open("visited.txt", "w").close()
            queue_txt = open("queue.txt", "w").close()
            self.visited.clear()
            self.queue.clear()
            print("To be added to the .txt file: +{} links".format(self.n))
        else:
            with open("visited.txt", "r") as visited_txt:
                with open("queue.txt", "r") as queue_txt:
                    txt_links = visited_txt.readlines()
                    if len(txt_links) == 0:
                        print("File is Empty, thus -False- parameter is not allowed.\nPlease try again!")
                        exit(3)
                    for line in txt_links:
                        line = re.sub("\\n+", "", line)
                        self.visited.append(line)
                    queue_links = queue_txt.readlines()
                    if len(queue_links) == 0:
                        print("Queue is Empty, thus -False- parameter is not allowed.\nPlease try again!")
                        exit(4)
                    for line in queue_links:
                        line = re.sub("\\n+", "", line)
                        self.queue.append(line)
            self.url = self.queue[0]
            self.queue.pop(0)
            self.new_size_visited = self.n
            print("To be added to the .txt file: +{} links".format(self.new_size_visited))

    def write_file(self):
        # if dont exist creates and appends too
        visited_txt = open("visited.txt", "a+")
        queue_txt = open("queue.txt", "a+")
        counter_visited = self.new_size_visited
        counter_queue = self.new_size_queue
        for i in range(counter_visited, len(self.visited)):
            visited_txt.write(self.visited[i] + "\n")
        for i in range(counter_queue, len(self.queue)):
            queue_txt.write(self.queue[i] + "\n")