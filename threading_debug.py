import sys
import requests
from time import sleep
from PySide2 import QtCore, QtWidgets
from bs4 import BeautifulSoup

class MovieWorkersSignal(QtCore.QObject):
    """
    Signals available from worker threads
    """
    finished = QtCore.Signal()
    result = QtCore.Signal(dict)

class MovieScannerThread(QtCore.QRunnable):
    """
    Thread class scanning a dummy URL for testing
    """
    def __init__(self, movie_name, header, jw_url):
        super().__init__()
        self.movie_name = movie_name
        self.header = header
        self.jw_url = jw_url
        self.signals = MovieWorkersSignal()

    def run(self):
        """
        Simulates scanning a page for a movie
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

        self.signals.result.emit(result_dict)

    def parse_page(self, html):
        """
        Dummy parsing function
        """
        soup = BeautifulSoup(html.content, features="html.parser")
        return "Parsed Data placeholder %s" % soup.find("a", class_="title-list-row__column-header").find("span", class_="header-title").get_text(strip=True)

class ThreadingTestApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.pool = QtCore.QThreadPool()
        #self.pool.setMaxThreadCount(2)

    def init_ui(self):
        self.setWindowTitle("Threading Test")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.start_button = QtWidgets.QPushButton("Start Threading Test")
        self.start_button.clicked.connect(self.start_test)
        self.layout.addWidget(self.start_button)

        self.log = QtWidgets.QTextEdit(self)
        self.log.setReadOnly(True)
        self.layout.addWidget(self.log)

    def log_message(self, message):
        self.log.append(message)

    def start_test(self):
        # Dummy data for testing
        film_titles = ['hiroshima-mon-amour', 'in-the-mood-for-love', 'her', 'pretty-in-pink', '10-things-i-hate-about-you', 'whats-your-number', 'made-of-honor', 'when-harry-met-sally', 'set-it-up', 'love-rosie', 'before-sunrise', 'how-to-lose-a-guy-in-10-days', 'pride-prejudice', 'letters-to-juliet', 'plus-one-2019', 'romeo-juliet-1996', 'emma-2020', 'tune-in-for-love', 'chungking-express', 'stuck-in-love', 'just-my-luck-2006', '500-days-of-summer', 'eternal-sunshine-of-the-spotless-mind', 'the-notebook', 'your-name', 'la-la-land', 'blue-valentine', 'flipped', 'portrait-of-a-lady-on-fire', 'carol-2015', 'happy-together-1997']
        jw_search_url = "https://www.justwatch.com/fr/recherche?q="
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        for movie_name in film_titles:
            worker = MovieScannerThread(movie_name, headers, jw_search_url)
            worker.signals.result.connect(self.worker_finished)
            self.pool.start(worker)

        self.log_message("Threading test started.")

    @QtCore.Slot(dict)
    def worker_finished(self, result):
        """
        Handles results from the worker threads
        """
        self.log_message(f"Worker finished: {result}")
        if self.pool.activeThreadCount() == 0:
            self.log_message("All threads have completed.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ThreadingTestApp()
    window.show()
    sys.exit(app.exec_())

