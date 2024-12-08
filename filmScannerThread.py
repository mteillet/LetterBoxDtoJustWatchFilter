# filmScannerThread.py
import threading
import requests

from bs4 import BeautifulSoup

class MovieScannerThread(threading.Thread):
    """
    Thread class scanning just watch for each movie
    """
    def __init__(self, movie_name, results, lock):
        super().__init__()
        self.movie_name = movie_name
        self.results = results 
        self.lock = lock

    def run(self):
        """
        Scan the JW page for the movie
        """
        print("Scanning %s" % self.movie_name)
        self.update_results(self.movie_name)

    def parse_page(self, html):
        """
        Parsing the JW html to get the relevant informations
        """
        return "Result"

    def update_results(self, result):
        """
        Update the shared results list
        """
        with self.lock:
            self.results.append(result)
            print("Finished scanning : %s" % result)

