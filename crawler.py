import requests
from bs4 import BeautifulSoup
import re
import time
from document import Document
from pathlib import Path
import pathlib


# NON THREADED VERSION
# import threading
# from concurrent.futures import ThreadPoolExecutor


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

# Attribute remover from soup object
def remove_attrs(soup):
    for tag in soup.findAll(True):
        tag.attrs = None
    return soup


def check_if_link_in_file(link):
    with open("visited.txt") as visited_txt:
        lines = [line.rstrip() for line in visited_txt]
        for line in lines:
            if link == line:
                return True
    return False


class Crawler:
    queue = []
    visited = []
    soups = []
    texts = []

    # Constructor
    def __init__(self, url, n, threads, warm_start, algo):
        self.url = url
        self.n = n
        self.threads = threads
        self.warm_start = warm_start
        self.algo = algo

    # Crawler initializer
    def initializeCrawl(self):
        documents = []

        t1 = time.perf_counter()
        if self.warm_start:
            visited_txt = open("visited.txt", "w").close()
            self.visited.clear()
            self.queue.clear()
            self.soups.clear()

        self.queue = self.getLinks(self.url)
        self.visited.append(self.url)
        # th = threading.Thread(self.crawl(self.queue[0]))
        # th.start()
        self.crawl(self.queue[0])

        # Creating document.py objects
        for i in range(len(self.visited)):
            doc = Document(self.visited[i], self.texts[i])
            documents.append(doc)

        t2 = time.perf_counter()
        print("Time Elapsed: " + str(t2 - t1))

        # Test print
        for doc in documents:
            print(doc.link)
            print(doc.text)

    # Crawl method
    def crawl(self, url):
        if len(self.visited) >= self.n:
            return
        if url in self.visited:
            self.queue.pop(0)
            self.crawl(self.queue[0])
        else:
            self.visited.append(url)
            links = self.getLinks(url)
            if links is None:
                self.queue.pop(0)
                self.crawl(self.queue[0])
            else:
                if self.algo == "DFS":
                    for link in links:
                        self.queue.insert(0, link)
                elif self.algo == "BFS":
                    for link in links:
                        self.queue.append(link)
                self.crawl(self.queue[0])

    # Method to get all links from given url
    def getLinks(self, url):
        links = []
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "lxml")
            self.soups.append(soup)
            for link in soup.find_all('a', href=True):
                links.append(link.get("href"))
            links = remove_duplicates(links)
            # Making new clean_soup version, no tags
            clean_soup = remove_attrs(soup)
            self.texts.append(clean_soup.find_all('p'))
            return links
        except Exception as ex:
            print(url + ": " + str(ex) + "\n")

    def write_file(self):
        # if dont exist creates and appends too
        visited_txt = open("visited.txt", "a+")
        for link in self.visited:
            visited_txt.write(link + "\n")
        visited_txt.close()
