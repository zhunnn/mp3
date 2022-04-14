from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.common.by import By

class QueryThread(QThread):
    callback = pyqtSignal(object)

    def __init__(self, browser, song):
        super().__init__(None)
        self.browser = browser
        self.song = song

    def run(self):
        # https://www.youtube.com/watch?v=0rp3pP2Xwhs&ab_channel=%E8%8C%84%E5%AD%90%E8%9B%8BEggPlantEgg
        # https://www.backupmp3.com/zh/?v=0rp3pP2Xwhs&ab_channel=%E8%8C%84%E5%AD%90%E8%9B%8BEggPlantEgg
        url = f'https://www.youtube.com/results?search_query={self.song}'
        self.browser.get(url)
        tags = self.browser.find_elements(By.TAG_NAME, 'a')
        links = {}
        for tag in tags:
            href = tag.get_attribute('href')
            if 'watch' in str(href):
                title = tag.get_attribute('title')
                if title == '':
                    try:
                        title = tag.find_elements(By.ID, 'video-title').get_attribute('title')
                    except:
                        pass
                if title != '':
                    links[href] = '{0} url={1}'.format(title, href)
                    # links['http://abc....'] = '周XX url = http://abc....'
        self.callback.emit(links)