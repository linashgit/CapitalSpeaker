import os
import comtypes.client
import comtypes.gen.SKCOMLib as sk
import pandas
import numpy

path = os.getcwd()
comtypes.client.GetModule(path + '\\SKCOM.dll')

class CaptialModel:
    def __init__(self, user, passwd, skQ_events, skR_events):
        # 建立物件
        self.skC = comtypes.client.CreateObject(sk.SKCenterLib, interface=sk.ISKCenterLib)
        self.skQ = comtypes.client.CreateObject(sk.SKQuoteLib, interface=sk.ISKQuoteLib)
        self.skR = comtypes.client.CreateObject(sk.SKReplyLib, interface=sk.ISKReplyLib)

        # 事件class 連結
        self.EventQ = skQ_events
        self.ConnectionQ = comtypes.client.GetEvents(self.skQ, self.EventQ)
        self.EventR = skR_events
        self.ConnectionO = comtypes.client.GetEvents(self.skR, self.EventR)

        # 初始狀態
        self.user = user
        self.passwd = passwd

    def getReturnCodeMessage(self):
        pass

    def login(self):
        code = self.skC.SKCenterLib_GetReturnCodeMessage(self.skC.SKCenterLib_Login(self.user, self.passwd))
        return code

    def enterMonitor(self):
        code = self.skC.SKCenterLib_GetReturnCodeMessage(self.skQ.SKQuoteLib_EnterMonitor())
        return code

    def signOut(self):
        code = self.skC.SKCenterLib_GetReturnCodeMessage(self.skQ.SKQuoteLib_LeaveMonitor())
        return code

    def requestTicks(self, num1, num2):
        # api註冊新商品
        code = self.skQ.SKQuoteLib_RequestTicks(num1, num2)
        return code

    def requestStockList(self):
        code = self.skQ.SKQuoteLib_RequestStockList(0)
        return code

    def requestKLineAM(self, stockname):
        # 清除舊資料
        self.EventQ.KlineData = []

        # 獲得k棒
        code = self.skQ.SKQuoteLib_RequestKLineAM(bstrStockNo=stockname, sKLineType=4, sOutType=1, sTradeSession=1)
        print(code)

        # 轉換資料
        data = pandas.DataFrame(self.EventQ.KlineData, dtype=numpy.float64)
        data.iloc[:, 0] = pandas.to_datetime(data.iloc[:, 0])
        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        data.index = data['Date']
        data = data.iloc[:, 1:]

        return data

'''
# skQ事件class
class skQ_events:
    def __init__(self):
        # 儲存k線資料
        self.KlineData = []
        self.stocklist = []

    def OnConnection(self, nKind, Code):
        if Code == 0:
            if nKind == 3001:
                print('連線中 Kind = ' + str(nKind))

            elif Code == 0 & (nKind == 3003):
                print('連線狀態 Kind = ' + str(nKind))

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


if __name__ == '__main__':
    cap = CaptialModel('', '')

    cap.login()

    cap.enterMonitor()

    aaa = cap.requestKLineAM(stockname='TX00')

    # cap.signOut()

'''