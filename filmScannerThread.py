# filmScannerThread.py
import requests
from time import sleep
from PySide2 import QtCore

from bs4 import BeautifulSoup

class MovieScannerThread(QtCore.QRunnable):
    """
    Thread class scanning just watch for each movie
    """
    # result_ready = QtCore.Signal(dict)

    def __init__(self, movie_name, header, jw_url, signal):
        super().__init__()
        self.movie_name = movie_name
        self.header = header
        self.jw_url = jw_url
        self.signal = signal

    def run(self):
        """
        Scan the JW page for the movie
        """
        result_dict = {}
        result_dict[self.movie_name] = {}
        print("Scanning %s" % self.movie_name)
        search_url = "%s%s" % (self.jw_url, self.movie_name)
        html = requests.get(search_url, headers = self.header)

        count = 1
        if html.status_code == 429: # In case the serve finds too many requests 
            while html.status_code == 429:
                sleep(count)
                html = requests.get(search_url, headers = self.header)
                count += 1

        if html.status_code != 200:
            result_dict[self.movie_name]["Error"] = True
            #print("Error for movie %s on url %s" % (self.movie_name, search_url))
        else:
            result_dict[self.movie_name]["Error"] = False
            self.parse_page(html)

        self.signal.emit(result_dict)


    def parse_page(self, html):
        """
        Parsing the JW html to get the relevant informations
        """
        soup = BeautifulSoup(html.content, features="html.parser")
        return "Result"


