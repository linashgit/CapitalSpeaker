import pandas_datareader as web
import pandas #
import numpy
import os

class LoadData:
    def __init__(self):
        pass
    
    def loadYahooFinanceData(self, tickers, start=None, end=None, dropna=True):
        '''
        tickers: It is a list
        '''
        data = {}
        count = 0
        for ticker in tickers:
            count += 1
            try:
                data[ticker]=web.DataReader(ticker ,"yahoo",start=start, end=end) #2010-01-01
                df = data[ticker]
                # 是否drop NaN
                if dropna == True:
                    df.dropna()
                    
                print('download data:', count, '/', len(tickers), ticker)
                
            except:
                print('loading error:', ticker)
        return data
    
    def loadLocalFinanceData(self, folder_path, file_type='xlsx', index_col='Date', dropna=True):
        # 資料類別
        typedic = {'csv': pandas.read_csv, 
                   'xlsx': pandas.read_excel}
        
        # 取得資料夾位置
        path = folder_path#os.path.join(os.getcwd(), 'excel')
        tickers = os.listdir(path) # 取得資料夾內檔案
        
        # 寫入字典
        data = {}
        count = 0
        for ticker in tickers:
            count += 1
            try:
                filename = os.path.join(path, ticker) # 取得檔案位置
                ticker = ticker.replace('.' + file_type, '') # 刪除副檔名
                df = typedic[file_type](filename, index_col=index_col)
                # 是否drop NaN
                if dropna == True:
                    df.dropna()
                    
                data[ticker] = df # 寫入
                
                print('use data:', count, '/', len(tickers), ticker)
            
            except:
                print('loading error:', ticker)
        return data
                
    def loadTEJFinanceData(self, file_path, dropna=True):
        '''
        file: It is .csv.
        '''
        # 資料先處理
        stockDataPath = file_path
        stockData = pandas.read_csv(stockDataPath, index_col='年月日')
        stockData.index = pandas.to_datetime(stockData.index)
        
        # 分類
        sector = stockData.groupby('證券代碼')
        stockData = stockData.loc[:, ['開盤價', '最高價', '最低價', '收盤價', '成交量']]
        stockData.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        tickers = sector.size().index
        data = {}
        
        # 寫入字典
        for ticker in tickers:    
            df = sector.get_group(ticker)
            # 是否drop NaN
            if dropna == True:
                df.dropna()
            data[str(ticker)] = df
        return data
    
if __name__ == '__main__':
    # TEJ使用方法
    '''path = os.path.join(os.getcwd(), 'TEJ', 'all_stocks_utf8.csv')
    data = LoadData.loadTEJFinanceData(path)'''
    
    # LocalData使用方法
    '''path = os.path.join(os.getcwd(), 'excel')
    data = LoadData.loadLocalFinanceData(path)'''

    #YAHOO
    tickers = ['2330.TW']
    load = LoadData()
    alldata = load.loadYahooFinanceData(tickers)

     
    
    