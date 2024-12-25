# filmScannerThread.py
import requests
from time import sleep

from PySide2 import QtCore
from bs4 import BeautifulSoup

class MovieWorkersSignal(QtCore.QObject):
    """
    Signals available from worker threads
    """
    finished = QtCore.Signal()
    result = QtCore.Signal(dict)

class MovieScannerThread(QtCore.QRunnable):
    """
    Thread class scanning just watch for each movie
    """
    def __init__(self, movie_name, header, jw_url):
        super().__init__()
        self.movie_name = movie_name
        self.header = header
        self.jw_url = jw_url
        self.signals = MovieWorkersSignal()  # Create once during initialization

    def run(self):
        """
        Scanning a page for a movie
        """
        print(f"Starting scan for {self.movie_name}")
        result_dict = {self.movie_name: {}}
        search_url = f"{self.jw_url}{self.movie_name}"
        print(search_url)

        try:
            # Simulate a network request
            html = requests.get(search_url, headers=self.header)

            if html.status_code == 429:  # Simulate too many requests
                count = 1
                while html.status_code == 429:
                    print(f"Retrying {self.movie_name} (attempt {count})...")
                    sleep(count)
                    html = requests.get(search_url, headers=self.header)
                    count += 1

            if html.status_code != 200:
                result_dict[self.movie_name]["Error"] = True
                result_dict[self.movie_name]["Message"] = f"HTTP Error {html.status_code}"
            else:
                result_dict[self.movie_name]["Error"] = False
                result_dict[self.movie_name]["Data"] = self.parse_page(html)
        except Exception as e:
            result_dict[self.movie_name]["Error"] = True
            result_dict[self.movie_name]["Exception"] = str(e)
        finally:
            self.signals.result.emit(result_dict)

    def parse_page(self, html):
        """
        Parsing the JW html to get the relevant informations
        """
        soup = BeautifulSoup(html.content, features="html.parser")
        return "Got : %s from Soup" % soup.find("a", class_="title-list-row__column-header").find("span", class_="header-title").get_text(strip=True)

