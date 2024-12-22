# main_controller.py
import re
from time import sleep
import threading

import requests
from bs4 import BeautifulSoup
from PySide2 import QtWidgets, QtCore
from playwright.sync_api import sync_playwright

from view.results_window import ResultsWindow
from filmScannerThread import MovieScannerThread

class Init_main_controller():
    def __init__(self, model, view):
        """
        Initializing the main controller with references to the model and view
        """
        self.model = model
        self.view = view
        self.connect_initial_signals()

        # Getting the generic dict from model
        generic_list = self.model.get_generic_list()
        generic_list_dict = self.build_generic_lists(generic_list)
        # Sending the results back to model bdd
        self.model.set_generic_lists_dict(generic_list_dict)

        # Calling gui build here to get the finish signal
        self.view.build_homepage(self.model.get_generic_lists_dict())
        self.applyStyleSheet(self.view)
        self.connect_signals()

    def connect_initial_signals(self):
        """
        Connecting signals between the model and view before bulding the gui 
        to link right away with the model
        """
        self.view.finished_homepageBuild.connect(self.init_model)

    def init_model(self):
        '''
        Links the model to the corresponding gui widgets
        '''
        # Getting the popular week list names and images, and sending them to the model
        popular_dict = self.get_letterboxd_popular_week()
        self.model.set_popular_list_dict(popular_dict)
        # For debugging purposes, uncomment the following line
        # print(self.model.get_popular_list_dict())

        # Adding the dbd popular film lists to homepage
        self.view.add_popular_week(self.model.get_popular_list_dict())

    def connect_signals(self):
        """
        Connecting signals between the model and view
        """
        self.view.popular_list_signal.connect(self.list_clicked)

    def fetch_gui_country(self):
        """
        Returns the country selected in the main window ComboBox
        """
        return self.view.languageCbox.currentIndex()

    def list_clicked(self, link):
        """
        Launching the results view after scanning the clicked list
        """
        # In case the link is coming from one of the shortened urls
        if link.startswith("/"):
            link = "https://letterboxd.com%s" % link
        # Sending link to model data bdd
        self.model.set_list_scan_url(link)
        # Making sur data is in model bdd
        print("Scanning list : %s" % self.model.get_list_scan_url())
        film_list = self.scan_list()
        self.model.set_film_list(film_list)
        # Printing the list fo movies
        for film in self.model.get_film_list():
            print(film)

        ####################################################
        ##  LAUNCH THE RESULTS WINDOW AND ITS CONTROLLER  ##
        ####################################################
        self.results_view = ResultsWindow()
        self.results_controller = ResultsController(self.model, self.results_view, self)
        self.results_controller.show_results()


    def scan_list(self):
        """
        Scanning a new list and returning the list of movies
        """
        url_to_scan = self.model.get_list_scan_url()
        list_page = requests.get(url_to_scan)

        if list_page.status_code != 200:
            return print("ERROR LOADING THE LINK : %s" % url_to_scan)

        # Checking if there are multiple pages
        pageSoup = ["filmContainer"]
        fetchedFilmsContainers = []

        # In case the url was shortened
        full_url = requests.get(url_to_scan).url

        current = 1
        while len(pageSoup) >> 0:
            new_url= "%spage/%i/" % (full_url, current)
            list_page = requests.get(new_url)
            if list_page.status_code != 200:
                return print("ERROR LOADING URL : %s" % new_url)
                break
            else:
                print("Found page : %s" % new_url)
            soup = BeautifulSoup(list_page.content, features = "html.parser")
            pageSoup = soup.find_all("li", class_="poster-container")
            if len(pageSoup) >> 0:
                fetchedFilmsContainers += pageSoup
            current += 1

        # Debug print, no need to uncomment
        # print(fetchedFilmsContainers)

        # Now need to find the actual name of the movies
        filmList = []
        for film in fetchedFilmsContainers:
            poster_container = film.find("div", class_ = "really-lazy-load")
            regex = re.compile('data-film-slug=["\'](.*?)["\']')
            movie_name = regex.search(str(poster_container)).group(1)
            filmList.append(movie_name)

        return filmList

    def get_letterboxd_popular_week(self):
        """
        Getting letterboxD lists data
        This week's popular categories
        """
        link = self.model.get_popular_link()
        # Trying playwright
        with sync_playwright() as p:
            # Launch headless browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(link)

            # Wait for images within the poster list to load
            page.wait_for_selector("ul.poster-list img", state="visible")
            
            # Get the page content after JavaScript has executed
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            browser.close()

            # Parsing the soup to get the relevant data
            listDict = {}
            filmLists = soup.select(".list.-overlapped.-summary")[:2]
            for section in filmLists:
                title = section.select("h2 a")[0].get_text()
                link = section.select("a.list-link")
                href = link[0]["href"] if link else None
                posters = section.select("ul.poster-list li.film-poster")
                poster_urls = []
                for poster in posters:
                    # poster_urls.append(poster.find("img")["src"])
                    img_url = poster.find("img")["src"]
                    img_data = requests.get(img_url).content
                    #print(img_url)
                    poster_urls.append(img_data)
                listDict[title] = {}
                listDict[title]["posters"] = poster_urls
                listDict[title]["link"] = href
        return listDict

    def build_generic_lists(self, generic_list):
        """
        Feeding the list urls to the parser function, and building the needed
        Dict from it
        """
        generic_list_dict = {}
        for key, value in generic_list.items():
            name, results = self.list_url_scraping(key, value)
            generic_list_dict[key] = results
            generic_list_dict[key]["title"] = name
            print("Scraping for %s, %s -> DONE" % (key, value))

        return generic_list_dict

    def list_url_scraping(self, list_name, url):
        """
        Scraping the url, returns a dict containing :
        dict = {
            ["posters"] = [list of poster href from urls]
            ["link"] = link to the list for when it is clicked
        }
        """
        with sync_playwright() as p:
            # Launch headless browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            # Wait for images within the poster list to load
            page.wait_for_selector("ul.poster-list img", state="visible")
            sleep(0.1)
            
            # Get the page content after JavaScript has executed
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            browser.close()

        # Parsing the soup to get the relevant data
        listDict = {}
        filmLists = soup.select(".list.-overlapped.-summary")
        # Getting the needed data
        title = filmLists[0].select("h2 a")[0].get_text()
        link = filmLists[0].select("a.list-link")
        href = link[0]["href"]
        posters = filmLists[0].select("ul.poster-list li.film-poster")
        poster_urls = []
        # Getting the posters data
        for poster in posters:
            try :
                img_url = poster.find("img")["srcset"]
            except KeyError :
                img_url = poster.find("img")["src"]
            img_data = requests.get(img_url).content
            poster_urls.append(img_data)
        results = {}
        results["posters"] = poster_urls
        results["link"] = href

        return title, results


    def applyStyleSheet(self, window):
        """
        Base StyleSheet for homepage
        """
        #background-color: rgb(30,35,45);
        stylesheet = """
            /* General Styling */
            QWidget {
                background-color: #1A1A1A;
                color: #FFFFFF;
                font-family: Arial, Helvetica, sans-serif;
            }

            /* Labels */
            QLabel {
                color: #E0E0E0;
                font-weight: bold;
                font-size: 14px;
            }

            /* Buttons */
            QPushButton {
                background-color: #333333;
                color: #A3E635;
                padding: 6px 12px;
                border: 1px solid #333333;
                border-radius: 5px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #444444;
                border: 1px solid #A3E635;
            }

            QPushButton:pressed {
                background-color: #555555;
            }

            /* Line Edits */
            QLineEdit {
                background-color: #2A2A2A;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 5px;
                color: #FFFFFF;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #A3E635;
            }

            /* ComboBox */
            QComboBox {
                background-color: #2A2A2A;
                color: #FFFFFF;
                border: 1px solid #444444;
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #444444;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }

            QComboBox QAbstractItemView {
                background-color: #2A2A2A;
                selection-background-color: #A3E635;
                selection-color: #1A1A1A;
            }

            /* Text Edits */
            QTextEdit, QPlainTextEdit {
                background-color: #2A2A2A;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 5px;
                color: #FFFFFF;
                font-size: 14px;
            }

            /* Scrollbars */
            QScrollBar:vertical {
                background: #1A1A1A;
                width: 8px;
                margin: 2px 0px 2px 0px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #333333;
                min-height: 20px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #444444;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }

            /* GroupBox */
            QGroupBox {
                border: 1px solid #333333;
                border-radius: 5px;
                margin-top: 10px;
                font-size: 14px;
                color: #A3E635;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 5px;
            }

            /* Checkboxes and Radio Buttons */
            QCheckBox, QRadioButton {
                color: #E0E0E0;
                font-size: 14px;
            }

            QCheckBox::indicator, QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 2px;
                background-color: #2A2A2A;
                border: 1px solid #444444;
            }

            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background-color: #A3E635;
                border: 1px solid #A3E635;
            }
            """
        # self.view.setStyleSheet(stylesheet)
        window.setStyleSheet(stylesheet)


class ResultsController(QtCore.QObject):
    """
    Main Controller for the results window
    """
    # scan_worker_result = QtCore.Signal(dict)

    def __init__(self, model, view, main_controller):
        super().__init__()
        self.model = model
        self.view_results = view
        self.main_controller = main_controller
        # Setup for the threading system
        self.pool = QtCore.QThreadPool.globalInstance()
        # Max concurrent workers
        #self.pool.setMaxThreadCount(2)

    def startScan(self):
        """
        Getting the film list from model bdd
        """
        film_titles = self.model.get_film_list()
        number_of_films = len(film_titles)
        jw_search_url = self.get_jw_country_url()
        print("Will scan the movies : \n %s \n Through URL : %s\nTotal : %s films to scan" % (film_titles, jw_search_url, number_of_films))
        request_header = self.model.get_request_headers()
        self.scan(film_titles, request_header, jw_search_url)
    
    def requeueScan(self, film_titles):
        """
        Requeue missed films to scan
        """
        jw_search_url = self.get_jw_country_url()
        request_header = self.model.get_request_headers()
        self.scan(film_titles, request_header, jw_search_url)

    def scan(self, film_titles, request_header, jw_search_url):
        for movie_name in film_titles:
            worker = MovieScannerThread(movie_name, request_header, jw_search_url)
            worker.signals.result.connect(self.worker_finished)
            self.pool.start(worker)

    @QtCore.Slot(dict) # Explicitly declare as a slot
    def worker_finished(self, result):
        """
        Obtaining result from worker once finished
        """
        print(result)
        # Sending the result to the model bdd
        self.model.add_scan_results(result)
        # Requeue missing member to avoid failed scans
        if self.pool.activeThreadCount == 0:
            self.checkRequeues()

    def checkRequeues(self):
        """
        Compares scan bdd agains film list to requeue missed movies
        """
        film_titles = self.model.get_film_list()
        scanned_films = self.model.get_scan_results()
        need_requeue = []

        for movie_name in film_titles:
            if movie_name not in scanned_films.keys():
                need_requeue.append(movie_name)

        if len(movie_name) > 0:
            self.requeueScan(movie_name)
        else:
            print("All movies are done scannign")

    def show_results(self):
        # print("Calling show on results window from the results controller")
        self.view_results.show()
        self.view_results.resize(1280, 720)
        # StyleSheets
        self.main_controller.applyStyleSheet(self.view_results)
        # Applying other stylesheet on bottom row
        widgetList = self.get_all_widgets(self.view_results.bottom_bar_layout)
        self.label_styling(widgetList)
        self.startScan()

    def get_jw_country_url(self):
        """
        Fetches the country urls and returns the correct one based
        on the gui selection
        """
        country_urls = self.model.get_justWatch_urls()
        current_country = self.main_controller.fetch_gui_country()
        # print("Current country index is : %s" % current_country)
        print("Current country url is %s" % country_urls[str(current_country)])
        return country_urls[str(current_country)]


    def get_all_widgets(self, layout):
        """
        Retrieve all widgets contained in the given layout.
        """
        widgets = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                widgets.append(item.widget())
        return widgets

    def label_styling(self, widgets):
        """
        Apply other stylesheet on the bottom bar labels
        """
        stylesheet = """
            /* Labels */
            QLabel {
                color: #979797;
                font-weight: lighter;
                font-size: 11px;
            }
            """
        for i in widgets:
            i.setStyleSheet(stylesheet)

