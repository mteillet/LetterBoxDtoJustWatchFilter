# model.py


class Init_model():
    def __init__(self):
        self.data = None
        self.popular_list_dict = {}
        self.generic_lists = {}
        self.generic_lists["Romance"] = "https://letterboxd.com/search/lists/Love+Movies/"
        self.generic_lists["Horror"] = "https://letterboxd.com/search/lists/Horror/"
        self.generic_lists["Action"] = "https://letterboxd.com/search/lists/Action+Movies/"
        self.generic_lists["Comedy"] = "https://letterboxd.com/search/lists/Comedy+Movies/"
        self.generic_lists["Drama"] = "https://letterboxd.com/search/lists/Drama+Movies/"
        self.generic_lists["Thriller"] = "https://letterboxd.com/search/lists/Thriller+Movies/"
        self.generic_lists["Mystery"] = "https://letterboxd.com/search/lists/mistery/"
        self.generic_lists["Animated"] = "https://letterboxd.com/search/lists/Animated+Movies/"
        self.generic_lists["Documentaries"] = "https://letterboxd.com/search/lists/Documentaries/"
        self.generic_lists["Science-Fiction"] = "https://letterboxd.com/search/lists/SF+Movies/"
        self.generic_lists["True Story"] = "https://letterboxd.com/search/lists/True+Story+Movies/"
        self.generic_lists["Musical"] = "https://letterboxd.com/search/lists/musicals/"
        self.popular_link = "https://letterboxd.com/lists/popular/this/week/"
        self.generic_lists_dict = {}
        # List Scanning
        self.list_scan_url = ""
        # Film names fils
        self.film_list = []
        # JustWatchUrls
        self.justWatch_urls = {}
        self.set_justWatch_urls()

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
            "france" : "https://www.justwatch.com/fr/recherche?q=",
            "germany" : "https://www.justwatch.com/de/Suche?q=",
            "spain" : "https://www.justwatch.com/es/buscar?q=",
            "united-kingdom" : "https://www.justwatch.com/uk/search?q=",
            "united-states" : "https://www.justwatch.com/us/search?q=",
                }

    def get_justWatch_urls(self):
        return self.justWatch_urls

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
