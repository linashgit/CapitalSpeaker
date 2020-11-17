from window import Ui_Form
from PyQt5.QtWidgets import QFrame
from CapitalClass import *
from MsgControl import *

class MainFrame(QFrame, Ui_Form):
    def __init__(self, parent=None):
        # 子繼承父類
        super(MainFrame, self).__init__(parent)

        # 調用介面
        self.setupUi(self)

        # 調用類
        self.msg = MsgControl()

        # 設定全局變數
        global GlobalLog # status log
        GlobalLog = self.textEdit_Log

        # 事件
        self.pushButton_Login.clicked.connect(self.login) #登入
        self.pushButton_Monitor.clicked.connect(self.enterMonitor) #監控
        self.pushButton_Signout.clicked.connect(self.signOut) #登出

    def login(self):
        #取得帳號密碼
        self.user = self.lineEdit_Id.text()
        self.passwd = self.lineEdit_Pw.text()
        # 調用群益模組
        global GlobalCap  # 群益api
        GlobalCap = CaptialModel(self.user, self.passwd)
        # 登入
        code = GlobalCap.login()
        # 寫入lOG
        self.msg.writeMessage(code, GlobalLog)

    def enterMonitor(self):
        code = GlobalCap.enterMonitor()
        self.msg.writeMessage(code, GlobalLog)

    def signOut(self):
        code = GlobalCap.signOut()
        self.msg.writeMessage(code, GlobalLog)

