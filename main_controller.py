# main_controller.py
import re
from time import sleep
from functools import partial

import io
import requests
import webbrowser
from PySide2 import QtCore
from PIL import Image
from bs4 import BeautifulSoup
from PySide2 import QtWidgets, QtCore
from playwright.sync_api import sync_playwright

from view.results_window import ResultsWindow
from view.custom_list_popup import Custom_List_Popup
from filmScannerThread import MovieScannerThread
from getBaseListsThread import GenericListsScannerThread


class LoadingController(QtCore.QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.splash_view = view
        self.connect_splashscreen_signals()
        self.splash_view.show()

    def connect_splashscreen_signals(self):
        """
        Connect the splash screen's initialized signal
        """
        # print("Connecting splashscreen signals")
        self.splash_view.initialized.connect(self.get_generic_list)
        # print("Signal connected")

    def get_generic_list(self):
        """
        Getting generic lists data from the database and building the homepage.
        """
        print("Get generic list called")
        generic_list = self.model.get_generic_list()
        self.build_generic_lists(generic_list)

    def build_generic_lists(self, generic_list):
        """
        Creating worker threads to fetch data for each list.
        """
        self.active_list_workers = []
        for key, url in generic_list.items():
            print(f"Starting worker for {key} at {url}")
            # Implement thread workers as needed
        print("Finished")

    @QtCore.Slot(str, dict)
    def workerList_result(self, result):
        """
        Handle results from the worker thread.
        """
        key, data = result
        print(f"Result received for {key}: {data}")


class MainController():
    def __init__(self, model, view):
        """
        Initializing the main controller with references to the model and view
        """
        self.model = model
        self.view = view
        self.pool = QtCore.QThreadPool()
        self.pool.setMaxThreadCount(6)

        self.connect_initial_signals()
        self.initialize_generic_list()
        self.applyStyleSheet(self.view)
        self.connect_signals()

    def connect_initial_signals(self):
        """
        Connecting signals between the model and view before bulding the gui 
        to link right away with the model
        """
        self.view.finished_homepageBuild.connect(self.init_model)
        
    def initialize_generic_list(self):
        """
        Getting generic lists data from bdd and building the homepage accordingly
        """
        generic_list = self.model.get_generic_list()
        generic_list_dict = self.build_generic_lists(generic_list)
        self.model.set_generic_lists_dict(generic_list_dict)
        self.view.build_homepage(self.model.get_generic_lists_dict())

    def init_model(self):
        '''
        Links the model to the corresponding gui widgets using the popular lists on letterboxd
        '''
        popular_dict = self.get_letterboxd_popular_week()
        self.model.set_popular_list_dict(popular_dict)
        self.view.add_popular_week(self.model.get_popular_list_dict())

    def connect_signals(self):
        """
        Connecting signals between the model and view
        """
        self.view.popular_list_signal.connect(self.list_clicked)
        self.view.customList_btn.clicked.connect(self.custom_list_btn_clicked)

    def custom_list_btn_clicked(self):
        """
        Handling custom list btn clicked signal
        """
        self.popup_view = Custom_List_Popup()
        self.applyStyleSheet(self.popup_view)
        self.popup_view.show()
        self.popup_link_signals()

    def popup_link_signals(self):
        """
        Linking popup view ( Custom_List_Popup ) signals to the controller
        """
        self.popup_view.ok_btn.clicked.connect(self.custom_list_ok_btn_clicked)
        self.popup_view.link_line_edit.returnPressed.connect(self.custom_list_ok_btn_clicked)

    def custom_list_ok_btn_clicked(self):
        """
        Checking the validity of the custom list, and feeding it to the scanner if it is
        """        
        custom_list_link = self.popup_view.link_line_edit.text()
        if self.is_valid_url(custom_list_link):
            self.popup_view.text_label.setText("URL : %s is Ok" % custom_list_link)
            self.popup_view.close()
            #self.model.set_film_list(custom_list_link)
            self.list_clicked(custom_list_link)
        else:
            self.popup_view.text_label.setText("%s is not a valid URL, try another one please" % custom_list_link)

        
    def is_valid_url(self, url):
        """
        Check if an url can be reached
        """
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code == 200  # URL is reachable and responds with OK
        except requests.RequestException:
            return False

    def fetch_gui_country(self):
        """
        Returns the country selected in the main window ComboBox
        """
        return self.view.languageCbox.currentIndex()

    def ensure_full_url(self, link):
        """
        Checks the letterbox url format. If it is a shortened url, returning a full one
        """
        return "https://letterboxd.com%s" % link if link.startswith("/") else link

    def list_clicked(self, link):
        """
        Launching the results view after scanning the clicked list
        """
        self.model.reset_scan_results()
        self.model.set_list_scan_url(self.ensure_full_url(link))

        print("Scanning list : %s" % self.model.get_list_scan_url())
        film_list = self.scan_list()
        print("FILM LIST :" % film_list)
        self.model.set_film_list(film_list)

        print("Movies:", *film_list, sep="\n")

        self.launch_results_view()

    def launch_results_view(self):
        """
        Launching the actural result window and its result controller
        """
        self.results_view = ResultsWindow()
        self.results_controller = ResultsController(self.model, self.results_view, self)
        self.results_controller.show_window()
        self.start_scan()

    def start_scan(self):
        """
        Getting the film list from model bdd and starting the scan
        """
        # Dummy data for testing
        #film_titles = ['hiroshima-mon-amour', 'in-the-mood-for-love', 'her', 'pretty-in-pink', '10-things-i-hate-about-you', 'whats-your-number', 'made-of-honor', 'when-harry-met-sally', 'set-it-up', 'love-rosie', 'before-sunrise', 'how-to-lose-a-guy-in-10-days', 'pride-prejudice', 'letters-to-juliet', 'plus-one-2019', 'romeo-juliet-1996', 'emma-2020', 'tune-in-for-love', 'chungking-express', 'stuck-in-love', 'just-my-luck-2006', '500-days-of-summer', 'eternal-sunshine-of-the-spotless-mind', 'the-notebook', 'your-name', 'la-la-land', 'blue-valentine', 'flipped', 'portrait-of-a-lady-on-fire', 'carol-2015', 'happy-together-1997']
        #jw_search_url = "https://www.justwatch.com/fr/recherche?q="
        #headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.active_workers = []

        film_titles = self.model.get_film_list()
        jw_search_url = self.get_jw_country_url()
        request_header = self.model.get_request_headers()

        print("Will scan the movies : \n %s \n Through URL : %s\nTotal : %s films to scan" % (film_titles, jw_search_url, len(film_titles)))

        for movie_name in film_titles:
            worker = MovieScannerThread(movie_name, request_header, jw_search_url)
            worker.signals.result.connect(self.worker_result, QtCore.Qt.QueuedConnection)
            self.active_workers.append(worker)
            self.pool.start(worker)
 
    @QtCore.Slot(dict)
    def worker_result(self, result):
        """
        Obtaining result from worker once finished
        """
        self.model.add_scan_results(result)
        print("Worker Finished : %s = %s" % (list(result.keys())[0], result[list(result.keys())[0]]["Data"].keys()))
        self.log_message("%s found as : %s ; %s/%s" % (list(result.keys())[0], result[list(result.keys())[0]]["Data"]["jw_title"], len(list(self.model.get_scan_results().keys())), len(self.model.get_film_list())))
        self.results_controller.update_ui_scan(result)

        QtCore.QCoreApplication.processEvents()

        if len(list(self.model.get_scan_results().keys())) == len(self.model.get_film_list()):
            self.log_message("FINISHED SCAN")
            for key in list(self.model.get_scan_results().keys()):
                self.log_message("%s = Stream : %s services, Rent : %s services" % (key, len(self.model.get_scan_results()[key]["Data"]["stream_list"]), len(self.model.get_scan_results()[key]["Data"]["rent_list"]) ))
            self.log_message("%s films scanned" % len(list(self.model.get_scan_results().keys())))
            self.results_controller.update_ui_scan_finished(len(self.model.get_film_list()))
        # Need this print for now as raising an error is the only way found to ensure thread slots are always triggered
        print(result["dummyKey"])

    def log_message(self, message):
        self.results_view.log.append(str(message))

    def get_jw_country_url(self):
        """
        Fetches the country urls and returns the correct one based
        on the gui selection
        """
        country_urls = self.model.get_justWatch_urls()
        return country_urls[str(self.fetch_gui_country())]

    def scan_list(self):
        """
        Scanning a new list and returning the list of movies
        """
        url_to_scan = self.model.get_list_scan_url()
        film_list = []
        current_page = 1

        while True:
            page_url = "%spage/%s/" % (url_to_scan, current_page)
            print("Scanning : %s" % page_url)
            response = requests.get(page_url)
            if response.status_code != 200:
                print("Error loading the link : %s" % page_url)
                break

            soup = BeautifulSoup(response.content, "html.parser")
            posters = soup.find_all("li", class_="poster-container")
            if not soup.find_all("li", class_="poster-container"):
                break

            for poster in posters:
                container = poster.find("div", class_ = "really-lazy-load")
                regex = re.compile('data-film-slug=["\'](.*?)["\']')
                film_slug = regex.search(str(container)).group(1)
                if film_slug:
                    film_list.append(film_slug)

            current_page += 1

        return film_list

    def get_letterboxd_popular_week(self):
        """
        Getting letterboxD lists data
        This week's popular categories
        """
        link = self.model.get_popular_link()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(link)
            page.wait_for_selector("ul.poster-list img", state="visible")
            
            soup = BeautifulSoup(page.content(), "html.parser")
            browser.close()

        return self.parse_popular_lists(soup) 

    def parse_popular_lists(self, soup):
        """
        Getting this week's first two popular lists 
        """
        list_dict = {}
        film_lists = soup.select(".list.-overlapped.-summary")[:2]

        for section in film_lists:
            img_posters = []
            title = section.select_one("h2 a").get_text()
            href = section.select_one("a.list-link")["href"]
            posters = [requests.get(poster.select_one("img")["src"]).content for poster in section.select("ul.poster-list li.film-poster")]

            list_dict[title] = {"posters" : list(reversed(posters)),
                                "link" : href}

        return list_dict

    def build_generic_lists(self, generic_list):
        """
        Feeding the list urls to the parser function, and building the needed
        Dict from it
        """
        self.active_list_workers = []
        for key, url in generic_list.items():
            print("Scraping : %s at %s ..." % (key, url))
            # TODO
            #workerList = GenericListsScannerThread(key, url)
            #workerList.signals.result.connect(self.workerList_result, QtCore.Qt.QueuedConnection)
            #self.active_list_workers.append(workerList)
            #self.pool.start(workerList)

            
            title, results = self.scrape_generic_list(url)
            generic_list_dict[key] = results
            generic_list_dict[key]["title"] = title
            print("Scraping : %s OK" % key)

        return generic_list_dict

    @QtCore.Slot(tuple)
    def workerList_result(self, result):
        """
        Adding the result from the worker thread to the bdd
        """
        key, list_scan_result = result
        print("Scraping : %s OK" % key)
        generic_list_dict = {}
        generic_list_dict[key] = list_scan_result
        generic_list_dict[key]["title"] = key

    def scrape_generic_list(self, url):
        """
        Scraping an url, returning a dict containing 
        the list of posters and the link to the list
        """
        white_poster = True
        while white_poster:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                page.wait_for_selector("ul.poster-list img", state="visible")
                soup = BeautifulSoup(page.content(), "html.parser")
                browser.close()

            title = soup.select_one(".list.-overlapped.-summary h2 a").get_text()
            href = soup.select_one(".list.-overlapped.-summary a.list-link")["href"]
            posters = [requests.get(poster.select_one("img")["src"]).content for poster in soup.select("ul.poster-list li.film-poster")[:5]]
            for image in posters:
                if self.check_blank_image(Image.open(io.BytesIO(image))):
                    print("Placeholder image detected for posters of %s -- > Requeue" % title)
                    white_poster = True
                    break
                else:
                    white_poster = False
        return title, {"posters": list(reversed(posters)), "link" : href}

    def check_blank_image(self, image):
        """
        Check if an image is blank (e.g., all white).
        """
        grayscale_image = image.convert("L")
        extrema = grayscale_image.getextrema()
        return extrema[0] == extrema[1]

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


            QScrollBar::handle:horizontal{
                background: #333333;
                min-height: 10px;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #444444;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal{
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
    def __init__(self, model, view, main_controller):
        super().__init__()
        self.model = model
        self.view_results = view
        self.main_controller = main_controller

    def show_window(self):
        self.view_results.show()
        self.view_results.resize(1280, 720)
        self.main_controller.applyStyleSheet(self.view_results)
        self.style_labels(self.get_all_widgets(self.view_results.bottom_bar_layout))
        self.link_signals()

    def link_signals(self):
        """
        Linking the signals that are always in the UI to logic here
        """
        self.view_results.filter_text_edit.returnPressed.connect(self.filter_movies_enter_pressed)
        self.view_results.stream_btn.clicked.connect(self.filter_stream_btn_pressed)
        self.view_results.rent_btn.clicked.connect(self.filter_rent_btn_pressed)

    def filter_movies_enter_pressed(self):
        """
        Filtering services movie display based on the QLineEdit text
        """
        self.main_controller.log_message("Filtering : %s" % self.view_results.filter_text_edit.text())
        self.filtering_logic(self.view_results.filter_text_edit.text(), self.view_results.stream_btn.isChecked(), self.view_results.rent_btn.isChecked())

    def filter_stream_btn_pressed(self):
        """
        Filtering stream serices, based on the button checked state or not
        """
        print("Stream fitlering : %s" % self.view_results.stream_btn.isChecked())
        self.btn_checking_stylesheet(self.view_results.stream_btn, self.view_results.stream_btn.isChecked())
        self.filtering_logic(self.view_results.filter_text_edit.text(), self.view_results.stream_btn.isChecked(), self.view_results.rent_btn.isChecked())

    def filter_rent_btn_pressed(self):
        """
        Filtering rent serices, based on the button checked state or not
        """
        print("Rent fitlering : %s" % self.view_results.rent_btn.isChecked())
        self.btn_checking_stylesheet(self.view_results.rent_btn, self.view_results.rent_btn.isChecked())
        self.filtering_logic(self.view_results.filter_text_edit.text(), self.view_results.stream_btn.isChecked(), self.view_results.rent_btn.isChecked())

    def filtering_logic(self, filter_string, stream_btn, rent_btn):
        """
        Fitlering the movie lists widgets visibility based on:
            - The QLineEdit if it isn't empty or "Filter Services"
            - The stream checkable btn
            - The rent checkable btn
            - The Radio btns states
        """
        stream_services_dict = self.model.get_stream_services()
        rent_services_dict = self.model.get_rent_services()
        radio_btns_dict = self.model.get_stream_rent_btns()
        need_filter_text = False

        if self.view_results.filter_text_edit.text() != "Filter Services" and self.view_results.filter_text_edit.text() != "":
            # print("Need filtering, since filter text is : \n%s" % self.view_results.filter_text_edit.text())
            need_filter_text = True

        if stream_btn:
            for key, values in stream_services_dict.items():
                if radio_btns_dict["stream"][key].isChecked():
                    if need_filter_text:
                        if self.view_results.filter_text_edit.text().lower() in values["label"].text().lower():
                            values["scrollArea"].setVisible(True)
                            values["label"].setVisible(True)
                        else:
                            values["scrollArea"].setVisible(False)
                            values["label"].setVisible(False)
                    else:
                        values["scrollArea"].setVisible(True)
                        values["label"].setVisible(True)
        else:
            for key, values in stream_services_dict.items():
                values["scrollArea"].setVisible(False)
                values["label"].setVisible(False)

        if rent_btn :
            for key, values in rent_services_dict.items():
                if radio_btns_dict["rent"][key].isChecked():
                    if need_filter_text:
                        if self.view_results.filter_text_edit.text().lower() in values["label"].text().lower():
                            values["scrollArea"].setVisible(True)
                            values["label"].setVisible(True)
                        else:
                            values["scrollArea"].setVisible(False)
                            values["label"].setVisible(False)
                    else:
                        values["scrollArea"].setVisible(True)
                        values["label"].setVisible(True)
        else:
            for key, values in rent_services_dict.items():
                values["scrollArea"].setVisible(False)
                values["label"].setVisible(False)
        

    def btn_checking_stylesheet(self, widget, status):
        """
        If the btn status is true, set default stylesheet
        Else, set a stylesheet with red instead of green
        """
        unchecked_stylesheet = """
            /* Buttons */
            QPushButton {
                background-color: #333333;
                color: #FF4D4D; /* Red text for better contrast */
                padding: 6px 12px;
                border: 1px solid #FF4D4D;
                border-radius: 5px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #444444;
                border: 1px solid #FF4D4D;
            }

            QPushButton:pressed {
                background-color: #555555; /* Neutral gray for pressed state */
            }
        """
        if status:
            self.main_controller.applyStyleSheet(widget)
        else:
            widget.setStyleSheet(unchecked_stylesheet)

    def update_ui_scan(self, data):
        """
        Updating the current film being scan and the scan percentage
        """
        percent = 100 * len(list(self.model.get_scan_results().keys())) / len(self.model.get_film_list())
        self.view_results.percentage_lbl.setText("{}%".format(str(round(percent)).zfill(2)))
        bar = self.view_results.loading_bar.text()
        for i in range(round(percent*0.1)):
            bar = bar[:i+1] + "#" + bar[i+2:] 
        self.view_results.loading_bar.setText(bar)
        self.view_results.status_lbl.setText("Scan done fore %s" % list(data.keys())[0])

        self.add_widgets_to_ui(data)

        # Adding this call to update_ui_scan_finished in case one of the worker signals is triggered
        # after the initial call to update_ui_scan_finished
        if len(list(self.model.get_scan_results().keys())) == len(self.model.get_film_list()):
            self.update_ui_scan_finished(len(self.model.get_film_list()))

    def add_widgets_to_ui(self, data):
        """
        Adding the scan result to the UI and the bdd
        """
        film_title = list(data.keys())[0]
        self.handle_stream_and_rent_services_ui(data, film_title)

    def handle_stream_and_rent_services_ui(self, data, film_title):
        """
        If stream and/or rent service found, add to bdd if it doesn't already exist 
        also handles layout and radio buttons creation in the UI
        """
        self.new_movie_buttons = []

        # Stream
        if data[film_title]["Data"]["stream"]:
            for key, value in data[film_title]["Data"]["stream_list"].items():
                if key not in self.model.get_stream_services():
                    # Creating the layout for the movies linked to the service
                    new_service_layout = self.view_results.create_service_movies_layout(key, "Stream")
                    # Registers layout and key to bdd
                    self.model.add_stream_service({key : new_service_layout})
                    # Create its service radio button
                    streamrent, button = self.view_results.create_service_stream_radio_button(key)
                    self.model.add_stream_btn({key : button})
                    button.clicked.connect(partial(self.radio_btn_clicked, streamrent, button))
                # Adding the movie to the matching lists
                new_movie_button = self.view_results.add_movie_to_service_layout(data[film_title]["Data"]["jw_title"], data[film_title]["Data"]["poster"], data[film_title]["Data"]["stream_list"][key]["link"], self.model.get_stream_services()[key]["layout"])
                self.new_movie_buttons.append(new_movie_button)
                new_movie_button.clicked.connect(partial(self.movie_btn_link_url, data[film_title]["Data"]["stream_list"][key]["link"]))
        # Rent
        if data[film_title]["Data"]["rent"]:
            for key, value in data[film_title]["Data"]["rent_list"].items():
                if key not in self.model.get_rent_services():
                    new_service_layout = self.view_results.create_service_movies_layout(key, "Rent")
                    self.model.add_rent_service({key : new_service_layout})
                    streamrent, button = self.view_results.create_service_rent_radio_button(key)
                    self.model.add_rent_btn({key : button})
                    button.clicked.connect(partial(self.radio_btn_clicked, streamrent, button))
                new_movie_button = self.view_results.add_movie_to_service_layout(data[film_title]["Data"]["jw_title"], data[film_title]["Data"]["poster"], data[film_title]["Data"]["rent_list"][key]["link"], self.model.get_rent_services()[key]["layout"])
                self.new_movie_buttons.append(new_movie_button)
                new_movie_button.clicked.connect(partial(self.movie_btn_link_url, data[film_title]["Data"]["rent_list"][key]["link"]))

    def radio_btn_clicked(self, streamrent, button):
        """
        Handles lists of films visibility for buttons clicked
        """
        print("Toggling results visibility to %s for %s %s" % (button.isChecked(), button.text(), streamrent))

        if streamrent == "stream":
            film_layout = self.model.get_stream_services()[button.text()]
        else:
            film_layout = self.model.get_rent_services()[button.text()]

        if button.isChecked():
            film_layout["scrollArea"].setVisible(True)
            film_layout["label"].setVisible(True)
        else:
            film_layout["scrollArea"].setVisible(False)
            film_layout["label"].setVisible(False)

    def movie_btn_link_url(self, link):
        """
        Link the movie button to the url it was linked to in BDD
        """
        print(link)
        webbrowser.open(link, new=0, autoraise=True)

    def update_ui_scan_finished(self, data):
        """
        Updating the UI when scan is over
        """
        self.view_results.status_lbl.setText("Finished scanning %s films" % str(data))

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

    def style_labels(self, widgets):
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

