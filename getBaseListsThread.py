# getBaseListsThread.py
import io

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
    result = QtCore.Signal(tuple)


class GenericListsScannerThread(QtCore.QRunnable):
    """
    Thread class scanning letterboxD for each list
    """
    def __init__(self, key, list_link):
        super().__init__()
        self.key = key
        self.list_link = list_link
        self.signals = ListsWorkerSignals()

    def run(self):
        """
        Getting the list and posters of a list
        """
        print("Running thread for %s, list : %s" % (self.key, self.list_link))
        white_poster = True
        '''
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
                    print("Placeholder image detected for posters of %s --> Requeue" % title)
                    white_poster = True
                    break
                else:
                    white_poster = False
        '''
        print("Thread done for %s, list : %s" % (self.key, self.list_link))
        #self.signals.result.emit("result")
        #QtCore.QThread.msleep(10)
        #self.signals.result.emit((title, {"posters" : list(reversed(posters)), "link" : href}))
        self.signals.result.emit((self.key, {"posters" : "posteData"}))
        print("After emission print")

    def check_blank_image(self, image):
        """
        Check if an image is blank
        """
        grayscale_image = image.convert("L")
        extrema = grayscale_image.getextrema()
        return extrema[0] == extrema[1]


