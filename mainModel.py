from window import Ui_Form
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from CapitalClass import *
from MsgControl import *
from LoadFinancialData import *
from

class MainFrame(QFrame, Ui_Form):
    def __init__(self, parent=None):
        # 子繼承父類
        super(MainFrame, self).__init__(parent)

        # 調用介面
        self.setupUi(self)

        # 調用類
        self.msg = MsgControl()

        # 設定全局變數
        ## LOG
        global GlobalLog # status log
        GlobalLog = self.textEdit_Log
        ## 商品窗
        global GlobalStocks, GlobalFutures
        GlobalStocks = QStandardItemModel(0, 0)
        GlobalFutures = QStandardItemModel(0, 0)

        # 事件
        self.pushButton_Login.clicked.connect(self.login) #登入
        self.pushButton_Monitor.clicked.connect(self.enterMonitor) #監控
        self.pushButton_Signout.clicked.connect(self.signOut) #登出
        #self.pushButton_LoadStocks.clicked.connect(self.requestTicks) #獲得報價
        self.pushButton_LoadStocks.clicked.connect(self.graphStockData) #測試

        # 表格
        ## 商品報價
        GlobalStocks.setHorizontalHeaderLabels(['sIndex', 'stock', 'nTimehms', 'nBid', 'nAsk', 'nClose', 'nQty'])
        self.tableView_Stocks.setModel(GlobalStocks)
        self.tableView_Futures.setModel(GlobalFutures)

        # 載入測試資料
        self.load = LoadData()
        tickers = ['2330.TW']
        data = self.load.loadYahooFinanceData(tickers)
        self.df = data['2330.TW']
        self.msg.writeMessage('載入測試資料2330', GlobalLog)

    def login(self):
        #取得帳號密碼
        self.user = self.lineEdit_Id.text()
        self.passwd = self.lineEdit_Pw.text()
        # 調用群益模組
        global GlobalCap #群益api

        global GlobalskQ
        GlobalskQ = skQ_events()
        global GlobalskR
        GlobalskR = skR_events()

        GlobalCap = CaptialModel(self.user, self.passwd, GlobalskQ, GlobalskR)
        # 登入
        code = GlobalCap.login()
        # 寫入lOG
        self.radioButton_Status_Api.setChecked(1) #運作燈
        self.msg.writeMessage(code, GlobalLog)

    def enterMonitor(self):
        code = GlobalCap.enterMonitor()
        self.msg.writeMessage(code, GlobalLog)

    def signOut(self):
        code = GlobalCap.signOut()
        self.radioButton_Status_Api.setChecked(0) #運作燈
        self.msg.writeMessage(code, GlobalLog)

    def requestTicks(self):
        stock = 'TX00'
        code = GlobalCap.requestTicks(0, stock)
        self.msg.writeMessage(stock + '-' + str(code), GlobalLog)

    def graphStockData(self):
        pass

# skQ事件class
class skQ_events:
    def __init__(self):
        # 儲存k線資料
        self.KlineData = []
        self.stocklist = []

    def OnConnection(self, nKind, Code):
        if Code == 0:
            if nKind == 3001:
                a = ('連線中 Kind = ' + str(nKind))
                print(a)
                self.msg.writeMessage(a, GlobalLog)

            elif Code == 0 & (nKind == 3003):
                a = ('連線狀態 Kind = ' + str(nKind))
                print(a)
                self.msg.writeMessage(a, GlobalLog)

    def OnNotifyKLineData(self, bstrStockNo, bstrData):
        _list = bstrData.split(',')
        self.KlineData.append(_list)

    def OnNotifyTicks(self, sMarketNo, sIndex, nPtr, nDate, nTimehms, nTimemillismicros, nBid, nAsk, nClose, nQty,
                      nSimulate):
        print(sIndex, nTimehms, nClose, nQty)

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal):
        pass

    def OnNotifyStockList(self, sMarketNo, bstrStockData):
        _list = bstrStockData.split(',')
        print(_list)


# skR事件class
class skR_events:
    def __init__(self):
        pass

    def OnReplyMessage(self, bstrUserID, bstrMessage, sConfirmCode=0xFFFF):
        # 根據API 手冊，login 前會先檢查這個 callback,
        # 要返回 VARIANT_TRUE 給 server,  表示看過公告了，我預設返回值是 0xFFFF
        # print('OnReplyMessage', bstrUserID, bstrMessage)
        return sConfirmCode
