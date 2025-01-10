from PySide2.QtCore import Qt, QRunnable, QThreadPool, QObject, Signal, Slot, QThread
from PySide2.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
import time

class WorkerSignals(QObject):
    result = Signal(str)

class TestWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    def run(self):
        print(f"Running in thread: {QThread.currentThread()}")
        time.sleep(4)  # Simulate a long-running task
        self.signals.result.emit("Task Complete")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(2)

        self.label = QLabel("Click the button to start a task")
        self.button = QPushButton("Start Task")
        self.button.clicked.connect(self.start_task)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def start_task(self):
        for i in range(25):
            worker = TestWorker()
            worker.signals.result.connect(self.task_complete)
            self.threadpool.start(worker)
            self.label.setText("Task running...")

    @Slot(str)
    def task_complete(self, message):
        print("Task complete slot triggered")
        self.label.setText(message)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

