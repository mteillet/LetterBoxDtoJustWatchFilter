# model.py

class Init_model():
    def __init__(self):
        self.data = None
        self.popular_list_dict = {}
        self.generic_lists = {}
        self.generic_lists["Romance"] = "https://letterboxd.com/search/lists/Love+Movies/"
        #self.generic_lists["Horror"] = "https://letterboxd.com/search/lists/Horror/"
        #self.generic_lists["Action"] = "https://letterboxd.com/search/lists/Action+Movies/"
        #self.generic_lists["Comedy"] = "https://letterboxd.com/search/lists/Comedy+Movies/"
        #self.generic_lists["Drama"] = "https://letterboxd.com/search/lists/Drama+Movies/"
        #self.generic_lists["Thriller"] = "https://letterboxd.com/search/lists/Thriller+Movies/"
        #self.generic_lists["Mystery"] = "https://letterboxd.com/search/lists/mistery/"
        #self.generic_lists["Animated"] = "https://letterboxd.com/search/lists/Animated+Movies/"
        #self.generic_lists["Documentaries"] = "https://letterboxd.com/search/lists/Documentaries/"
        #self.generic_lists["Science-Fiction"] = "https://letterboxd.com/search/lists/SF+Movies/"
        #self.generic_lists["True Story"] = "https://letterboxd.com/search/lists/True+Story+Movies/"
        #self.generic_lists["Musical"] = "https://letterboxd.com/search/lists/musicals/"
        self.popular_link = "https://letterboxd.com/lists/popular/this/week/"
        self.generic_lists_dict = {}
        # List Scanning
        self.list_scan_url = ""
        # Film names fils
        self.film_list = []
        # JustWatchUrls
        self.justWatch_urls = {}
        self.set_justWatch_urls()
        self.request_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.scan_results = {}
        # UI data
        self.stream_services = {}
        self.rent_services = {}

    def add_rent_service(self, data):
        self.rent_services.update(data)
        
    def get_rent_services(self):
        return self.rent_services

    def add_stream_service(self, data):
        self.stream_services.update(data)

    def get_stream_services(self):
        return self.stream_services

    def reset_scan_results(self):
        self.scan_results = {}
        self.stream_services = {}
        self.rent_services = {}

    def get_scan_results(self):
        return self.scan_results

    def add_scan_results(self, data):
        self.scan_results.update(data)

    def set_film_list(self, data):
        self.film_list = data

    def get_film_list(self):
        return self.film_list

    def set_list_scan_url(self, data):
        self.list_scan_url = data

    def get_list_scan_url(self):
        return self.list_scan_url

    def set_generic_lists_dict(self, data):
        self.generic_lists_dict = data

    def get_generic_lists_dict(self):
        return self.generic_lists_dict

    def get_popular_link(self):
        return self.popular_link

    def get_generic_list(self):
        return self.generic_lists

    def set_popular_list_dict(self, data):
        self.popular_list_dict = data

    def get_popular_list_dict(self):
        return self.popular_list_dict

    def set_justWatch_urls(self):
        """
        Lists of urls to do web searches with the countries availability
        """
        self.justWatch_urls = {
            "0" : "https://www.justwatch.com/fr/recherche?q=",
            "1" : "https://www.justwatch.com/de/Suche?q=",
            "2" : "https://www.justwatch.com/es/buscar?q=",
            "3" : "https://www.justwatch.com/uk/search?q=",
            "4" : "https://www.justwatch.com/us/search?q=",
                }

    def get_request_headers(self):
        """
        Returns the request headers for url requests
        """
        return self.request_headers

    def get_justWatch_urls(self):
        return self.justWatch_urls

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
