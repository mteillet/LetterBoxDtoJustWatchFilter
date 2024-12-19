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
        #self.signal = signal
        self.signals = MovieWorkersSignal()

    def run(self):
        """
        Scan the JW page for the movie
        """
        if not hasattr (self, "movie_name"):
            print("No movie name attrib !")
            self.signals = MovieWorkersSignal()
            self.signals.result.emit("None")
            return
        print("Scanning %s" % self.movie_name)
        result_dict = {}
        result_dict[self.movie_name] = {}

        search_url = "%s%s" % (self.jw_url, self.movie_name)
        html = requests.get(search_url, headers = self.header)

        count = 1
        try:
            if html.status_code == 429: # In case the serve finds too many requests 
                '''
                while html.status_code == 429:
                    sleep(count)
                    html = requests.get(search_url, headers = self.header)
                    count += 1
                '''
                result_dict["Error"] = "Requeue"

            if html.status_code != 200:
                result_dict[self.movie_name]["Error"] = True
                #print("Error for movie %s on url %s" % (self.movie_name, search_url))
            else:
                result_dict[self.movie_name]["Error"] = False
                result_dict[self.movie_name]["Data"] = self.parse_page(html)
        except Exception as e:
            print("Error Scanning: %s" % self.movie_name)
            result_dict[self.movie_name]["Error"] = True
            result_dict[self.movie_name]["Exception"] = str(e)

        # Emit result back to the main thread
        self.signals.result.emit(result_dict)
        self.signals.finished.emit()

    def parse_page(self, html):
        """
        Parsing the JW html to get the relevant informations
        """
        soup = BeautifulSoup(html.content, features="html.parser")
        return "Parsed Data placeholder"


