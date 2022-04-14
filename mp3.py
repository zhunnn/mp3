import os
import sys
import pathlib
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListWidgetItem, QFileDialog
from BrowserThread import BrowserThread
from QueryThread import QueryThread
from DownloadThread import DownloadThread
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnQuery.clicked.connect(self.btnQuery_click)
        self.btnPath.clicked.connect(self.btnPath_click)
        self.btnDownload.clicked.connect(self.btnDownload_click)
        self.path =  os.path.dirname(os.path.realpath(sys.argv[0])).__str__()+"/download"
        self.lblPath.setText(self.path)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.disable()
        self.browserThread = BrowserThread(self.path)
        self.browserThread.callback.connect(
            self.browserThreadCallback
        )
        self.browserThread.start()

    def browserThreadCallback(self,browser):
        self.enable()
        self.browser=browser

    def btnQuery_click(self):
        self.listWidget.clear()
        self.song = self.txtSong.text()
        if self.song == '':
            dialog = QMessageBox()
            dialog.setWindowTitle('mp3下載')
            dialog.setText('請填入歌曲或歌手名稱')
            dialog.exec()
            return
        self.lblStatus.setText('Searching...')
        self.btnQuery.setEnabled(False)
        self.btnDownload.setEnabled(False)
        self.btnPath.setEnabled(False)
        self.queryThread = QueryThread(self.browser, self.song)
        self.queryThread.callback.connect(self.queryThreadCallback)
        self.queryThread.start()

    def queryThreadCallback(self, links):
        self.btnQuery.setEnabled(True)
        self.btnDownload.setEnabled(True)
        self.btnPath.setEnabled(True)
        self.lblStatus.setText('')
        for key in links.keys():
            box = QCheckBox(links[key])
            item = QListWidgetItem()  # listWidget 裡的每一空白行
            self.listWidget.addItem(item)  # 加入空白列
            self.listWidget.setItemWidget(item, box)  # 將核取方塊加到空白列

    def downloadThreadCallback(self, msg):
        self.lblStatus.setText(msg)

    def downloadFinished(self):
        self.lblStatus.setText('Download completed !')
        self.enable()

    def btnPath_click(self):
        self.path = QFileDialog.getExistingDirectory()
        print('path:',self.path)
        if self.path != '':
            if not os.path.isdir(self.path):
                os.mkdir(self.path)
            self.disable()
            self.lblPath.setText(self.path)
            self.browser.close()
            self.browserThread = BrowserThread(self.path)
            self.browserThread.callback.connect(self.browserThreadCallback)
            self.browserThread.start()
        print('path:',self.path)

    def btnDownload_click(self):
        # 取得清單項目數量
        count = self.listWidget.count()
        # 取得核取方塊的全部內容
        boxes = [self.listWidget.itemWidget(self.listWidget.item(i)) for i in range(count)]
        # 記錄有被勾選的項目
        chks = []
        for box in boxes:
            # 選取有被勾選的項目
            if box.isChecked():
                chks.append(box.text())
        self.disable()
        self.downloadThread = DownloadThread(self.browser, chks)
        self.downloadThread.callback.connect(self.downloadThreadCallback)  # 每下載完一首歌就會回調
        self.downloadThread.finished.connect(self.downloadFinished)  # 當所有歌曲下載完才會回調
        self.downloadThread.start()

    #  按鈕啟用
    def enable(self):
        self.btnQuery.setEnabled(True)
        self.btnPath.setEnabled(True)
        self.btnDownload.setEnabled(True)

    #  按鈕停用
    def disable(self):
        self.btnQuery.setEnabled(False)
        self.btnPath.setEnabled(False)
        self.btnDownload.setEnabled(False)

    # 按下 X 按鈕呼叫關閉視窗
    def closeEvent(self, event):
        try:
            self.browser.close()
            self.browser.quit()
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()