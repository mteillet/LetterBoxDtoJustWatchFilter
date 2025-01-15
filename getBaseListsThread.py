# getBaseListsThread.py
import io
from time import sleep

import requests
import webbrowser
from PySide2 import QtCore, QtGui
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from PIL import Image


class ListsWorkerSignals(QtCore.QObject):
    """
    Signals for worker threads
    """
    #result = QtCore.Signal(str)
    result = QtCore.Signal(str, dict)

class GenericListsScannerThread(QtCore.QRunnable):
    def __init__(self, key, list_link):
        super().__init__()
        self.key = key
        self.list_link = list_link
        self.signals = ListsWorkerSignals()

    def run(self):
        print(f"Running thread for {self.key} in thread: {QtCore.QThread.currentThread()}")
        title, href, poster_list = self.scrape_data()
        self.emit_result(title, href, poster_list)

    def emit_result(self, title, href, poster_list):
        self.signals.result.emit(title, {"title" : title, "link" : href, "poster" : poster_list})
        #self.signals.result.emit("test", {"title": "test", "link": "test", "posters": "test"})
        print(f"Emitted result for thread {self.key} in thread: {QtCore.QThread.currentThread()}")

    def scrape_data(self):
        """
        Perform web scraping for the list data.
        """
        white_poster = True
        while white_poster:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.list_link)
                page.wait_for_selector("ul.poster-list img", state="visible")
                soup = BeautifulSoup(page.content(), "html.parser")
                browser.close()

            title = soup.select_one(".list.-overlapped.-summary h2 a").get_text()
            href = soup.select_one(".list.-overlapped.-summary a.list-link")["href"]
            posters = [requests.get(poster.select_one("img")["src"]).content for poster in soup.select("ul.poster-list li.film-poster")[:5]]

            for image in posters:
                if self.check_blank_image(Image.open(io.BytesIO(image))):
                    print(f"Placeholder image detected for {title}. Retrying...")
                    white_poster = True
                    break
                else:
                    white_poster = False

        return title, href, list(reversed(posters))

    def check_blank_image(self, image):
        """
        Check if an image is blank.
        """
        grayscale_image = image.convert("L")
        extrema = grayscale_image.getextrema()
        return extrema[0] == extrema[1]


