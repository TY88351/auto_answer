import sys,requests,json
from PyQt5.QtWidgets import  QMainWindow,QApplication,   QMessageBox
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi('maingui.ui', self)
        self.init_t()

    def init_t(self):
        self.pushButton.clicked.connect(self.search)

    def search(self):
        try:
            text = self.textEdit.toPlainText().strip()
            if (len(text) < 6):
                QMessageBox.warning(self, "Warning", "题目少于6个字", QMessageBox.Yes, QMessageBox.Yes)
            else:
                url="http://39.108.63.141:8932/?q="+text
                res=requests.get(url=url)
                if(res.status_code==200):
                    res=json.loads(res.text)
                    if(res["status"]=="ok"):
                        data=res["data"]
                        s="题目：【{}】\n答案：【{}】".format(data["question"],data["answer"])
                        QMessageBox.information(self, "提醒",s,
                                            QMessageBox.Yes, QMessageBox.Yes)
                        self.textEdit.clear()
                    else:
                        QMessageBox.warning(self, "Warning", "api响应异常，响应信息为：{}".format(res),
                                            QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.warning(self, "Warning", "api响应异常，响应状态码为：{}".format(res.status_code), QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            QMessageBox.warning(self, "Warning", "程序出错：{}".format(e),
                                QMessageBox.Yes, QMessageBox.Yes)
            s = sys.exc_info()
            print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())