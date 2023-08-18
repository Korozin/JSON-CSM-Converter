import json
from PyQt5 import QtWidgets, QtCore, QtGui

class JSON_Text_Box(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isLocalFile() and url.toString().endswith('.json'):  # check if URL is a local file and ends with .json
                self.dropEvent(url)
    
    def dropEvent(self, url):
        path = url.toLocalFile()  # get file path as string
        with open(path, 'r') as f:
            data = json.load(f)
            self.insertPlainText(json.dumps(data, indent=8))
