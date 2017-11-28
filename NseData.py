# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 21:50:44 2017

@author: Sujay
"""

import mechanize 
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt


class NseData:
    StockName = 'None'
    HistoricalData = []
    KeyWords = []

    def __init__(self, stock_name):
        self.StockName = stock_name
        
    def GetHistoricalData(self):
        url = "https://www.nseindia.com/products/content/equities/equities/eq_security.htm"
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.set_handle_refresh(False)
        br.set_handle_robots(False)
        br.open(url)
        br.form  = list(br.forms())[0]
        
        #print br.form
        Datatype = br.form.find_control("dataType")
        Symbol = br.form.find_control("symbol")
        Series =  br.form.find_control("series")
        Period = br.form.find_control("dateRange")
               
        CurrentSyymbol = self.StockName
        Datatype.value = ['priceVolumeDeliverable']
        Symbol.value = CurrentSyymbol
        Series.value = ['ALL']
        
        Period.value=['12month']
        #fromDate.value = '22-10-2017'
        #toDate.value = '22-11-2017'
       
    
        response = br.submit()
        result = response.read()
        soup = bs(result, 'lxml')
        HistoricalData = soup.find("div",{"id": "csvContentDiv"})
        
        HistoricalData = str(HistoricalData)
        #print HistoricalData
        #remove div tag
        HistoricalData = HistoricalData[HistoricalData.find('>')+1:]
        HistoricalData = HistoricalData[:HistoricalData.find(":</div>")]
        
        #remove all "
        HistoricalData = "".join(HistoricalData.split())
        HistoricalData = HistoricalData.replace('"', "")
        
        #Make lists
        HDList  = HistoricalData.split(':')
        
        #get Keyword list
        
        self.KeyWords = HDList[0].split(',')
        
        HDList = HDList[1:]
        
        for i in HDList:
            self.HistoricalData.append(i.split(','))
        print self.KeyWords
        print self.HistoricalData[1]
    def GetHistoricalDataList(self, key):
        DataList =[]
        index = self.KeyWords.index(key)
        for i in self.HistoricalData:
            if i[self.KeyWords.index("Series")] == "EQ":
                DataList.append(i[index])
        return DataList

    def GetDataFromDate(self, date, key):
        index = self.KeyWords.index(key)
        for i in self.HistoricalData:
            if i[self.KeyWords.index("Date")] == date:
                 return i[index]
        return "NONE"

n= NseData('GEECEE')
n.GetHistoricalData()
plt.plot(n.GetHistoricalDataList("AveragePrice"))
print n.GetDataFromDate('23-Nov-2017', 'AveragePrice')



#Keywards ['Symbol', 'Series', 'Date', 'PrevClose', 'OpenPrice', 'HighPrice', 'LowPrice', 'LastPrice', 'ClosePrice', 'AveragePrice', 'TotalTradedQuantity', 'Turnover', 'No.ofTrades', 'DeliverableQty', '%DlyQttoTradedQty']
#HistroricalData[1] ['GEECEE', 'EQ', '30-Nov-2016', '128.60', '128.60', '129.75', '124.15', '127.90', '127.40', '126.89', '38211', '4848403.80', '1029', '20556', '53.80']