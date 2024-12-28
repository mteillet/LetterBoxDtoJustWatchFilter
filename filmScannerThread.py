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
        #result_dict["worker"] = self
        search_url = f"{self.jw_url}{self.movie_name}"
        print(search_url)

        try:
            # Simulate a network request
            html = requests.get(search_url, headers=self.header)

            if html.status_code == 429:  # Simulate too many requests
                count = 1
                timeout = 4
                while html.status_code == 429:
                    print(f"Retrying {self.movie_name} (attempt {count})...")
                    sleep(timeout)
                    html = requests.get(search_url, headers=self.header)
                    count += 1
                    timeout += 4

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
            #self.signals.finished.emit()
            #print("EMITTING RESULTS : %s" % result_dict)

    def parse_page(self, html):
        """
        Parsing the JW html to get the relevant informations
        Returns a data_dict containing
        {jw_title, poster, stream, rent, stream_list, rent_list }
        """
        data_dict = {}
        soup = BeautifulSoup(html.content, features="html.parser")
        data_dict["jw_title"] = soup.find("a", class_="title-list-row__column-header").find("span", class_="header-title").get_text(strip=True)
        data_dict["poster"] = requests.get(soup.find("picture", class_="picture-comp title-poster__image").find("img")["src"]).content

        # Checking rent and stream availability
        streamSoup = soup.find("div", class_="title-list-row__row").find("div", class_="buybox-row stream inline")
        if streamSoup:
            data_dict["stream"] = True
            data_dict["stream_list"] = self.parse_offers(streamSoup.find_all("a", class_="offer"))
        else:
            data_dict["stream"] = False
            data_dict["stream_list"] = []
        rentSoup = soup.find("div", class_="title-list-row__row").find("div", class_="buybox-row rent inline")
        if rentSoup:
            data_dict["rent"] = True
            data_dict["rent_list"] = self.parse_offers(rentSoup.find_all("a", class_="offer"))
        else:
            data_dict["rent"] = False
            data_dict["rent_list"] = []
        return data_dict
    
    def parse_offers(self, html):
        """
        Parsing the offers of the JW html
        Returns a dict containing
        {
            serviceTitle1 :
                {
                    img : url of the service logo img
                    link : url to be sent to the service itself
                },
            serviceTitle2 : {img, link},
            ...
        }
        """
        service_result = {}
        for service in html:
            service_result[service.find("picture", class_="picture-element").find("img")["title"]] = {}
            service_result[service.find("picture", class_="picture-element").find("img")["title"]]["img"] = service.find("picture", class_="picture-element").find("img")["src"]
            tracking_url = service["href"]
            # Shortening the url as much as possible if possible for convenience
            start = tracking_url.find("r=")
            if start != -1:
                start += 2  # Move past "r="
                end = tracking_url.find("&", start)  # Find the end of the encoded URL
                encoded_url = tracking_url[start:end] if end != -1 else tracking_url[start:]
                # Decode the URL manually by replacing percent-encoded characters
                tracking_url = encoded_url.replace("%3A", ":").replace("%2F", "/")
            service_result[service.find("picture", class_="picture-element").find("img")["title"]]["link"] = tracking_url
        return service_result

