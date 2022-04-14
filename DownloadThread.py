import time

from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DownloadThread(QThread):
    callback = pyqtSignal(object)
    finished = pyqtSignal()

    def __init__(self, browser, chks):
        super().__init__(None)
        self.runFlag = True  # 記錄目前正在執行
        self.browser = browser
        self.chks = chks

    def run(self):
        for chk in self.chks:
            title = chk.split(' url=')[0]
            url = chk.split(' url=')[1]
            url = url.replace('youtube', 'backupmp3')
            self.callback.emit(f'{title[:20]}...')
            self.browser.get(url)  # 開始下載歌曲
            try:
                # 預防第一次要下載時要選取格式
                self.browser.switch_to.frame('IframeChooseDefault')
                try:
                    WebDriverWait(self.browser, 20, 0.1).until(EC.presence_of_element_located(By.ID, 'MP3Format'))
                except:
                    pass
                btn = self.browser.find_element(By.ID, 'MP3Format')
                btn.click()
            except:
                pass
            time.sleep(2)
        self.finished.emit()