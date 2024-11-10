# model.py


class Init_model():
    def __init__(self):
        self.data = None
        self.popular_list_dict = {}

    def set_popular_list_dict(self, data):
        self.popular_list_dict = data

    def get_popular_list_dict(self):
        return self.popular_list_dict

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
