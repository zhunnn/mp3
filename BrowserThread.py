import os
import pathlib
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserThread(QThread):
    callback = pyqtSignal(object)

    def __init__(self, path):
        super().__init__(None)
        self.path = path

    def run(self):
        ops = Options()
        ops.add_argument('--disable-gpu')
        ops.add_argument('--headless')
        ops.add_experimental_option('excludeSwitches', ['enable-logging'])
        # 更改 chrome 預設下載目錄
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.path}
        ops.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome(os.path.dirname(os.path.realpath(sys.argv[0]))+'/chromedriver', options=ops)
        self.callback.emit(browser)
