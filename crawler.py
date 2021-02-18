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


def check_if_link_in_file(link):
    with open("visited.txt") as visited_txt:
        lines = [line.rstrip() for line in visited_txt]
        for line in lines:
            if link == line:
                return True
    return False


def requestUrl(url):
    try:
        r = requests.get(url)
        return r
    except Exception as ex:
        print("Exception from " + url + ": " + str(ex))
        return None


class Crawler:
    queue = []
    visited = []
    documents = []

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
        if self.warm_start:
            visited_txt = open("visited.txt", "w").close()
            self.visited.clear()
            self.queue.clear()

        self.queue.append(self.url)
        self.crawl(self.queue[0])
        t2 = time.perf_counter()
        print("Time Elapsed: " + str(t2 - t1) + "s." + "\n-----------------")
        print(len(self.visited) == self.n)

    # Crawl method
    def crawl(self, url):
        if len(self.visited) >= self.n:
            return
        if url in self.visited:
            self.queue.pop(0)
            self.crawl(self.queue[0])
        else:
            self.visited.append(url)
            # with ThreadPoolExecutor(max_workers=self.threads) as executor:
            #     print("Creating task!")
            #     task = executor.submit(requestUrl, url)
            #     print("Adding callback!")
            #     task.add_done_callback(self.callbackContinue)
            #     print("Callback added!")
            self.callbackContinue(url)
            self.crawl(self.queue[0])

    def callbackContinue(self, url):
        try:
            links = []
            texts = ''
            result = requestUrl(url)
            if result.status_code == 200:
                soup = BeautifulSoup(result.content, "lxml")
                for link in soup.find_all('a', href=True):
                    links.append(link.get("href"))
                links = remove_duplicates(links)
                for p in soup.findAll('p'):
                    texts += p.get_text() + '\n'
                doc = Document(url, texts)
                self.documents.append(doc)
                if self.algo == "DFS":
                    for link in links:
                        self.queue.insert(0, link)
                elif self.algo == "BFS":
                    for link in links:
                        self.queue.append(link)
        except Exception as ex:
            print(url.url + str(ex))
        except UnicodeEncodeError as er:
            print(url.url + str(er))

    # def write_file(self):
    #     # if dont exist creates and appends too
    #     visited_txt = open("visited.txt", "a+")
    #     for link in self.visited:
    #         visited_txt.write(link + "\n")
    #     visited_txt.close()
