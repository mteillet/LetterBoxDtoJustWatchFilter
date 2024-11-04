# main_controller.py


class Init_main_controller():
    def __init__(self, model, view):
        """
        Initializing the main controller with references to the model and view
        """
        self.model = model
        self.view = view

        self.connect_signals()

    def connect_signals(self):
        """
        Connecting signals between the model and view
        """
        print("Connecting Signals")
