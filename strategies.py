import pandas as pd
import pandas_ta as ta
import numpy as np
import os
import matplotlib.pyplot as plt
class Strategy:
    def __init__(self, name,exchange,entry,exit):
        self.name=name
        self.exchange=exchange
        self.algorithm={
            'entry':entry,
            'exit':exit
        }

    def backtest(self,startIndex):
        if len(self.algorithm['entry'])==0 or len(self.algorithm['exit'])==0:
            return 0
        indi=self.indi
        strategy=pd.DataFrame()
        strategy['position'] = indi['EMA20 Close'] > indi['EMA50 Close']
        strategy['pre_position'] = strategy['position'].shift(1)
        strategy.dropna(inplace=True) # dropping the NaN values
        strategy['crossover'] = np.where(strategy['position'] == strategy['pre_position'], False, True)
        indi.index = pd.to_datetime(indi.index)
        indi=indi.iloc[1: , :]
        print(indi[50:51].index[0])
        #print(indi)
        #print(strategy)
        #print(indi[70:71]['EMA20 Close'][0])

        for i in range(startIndex,len(indi)-1):
            balance=indi[i:i+1]['close'][0]
            break
        latestBalance=balance
        latestBalances=[]
        bals=pd.DataFrame()
        lastBalancesDates=[]
        bought=False

        for i in range(startIndex,len(indi)-1):
            if indi[i:i+1]['EMA20 Close'][0] > indi[i:i+1]['EMA50 Close'][0] and bought==False:
                if strategy[i:i+1]['crossover'][0]==True:
                    bought=True
                    balance=balance/indi[i:i+1]['close'][0]
                    #print("buy",indi[i:i+1]['close'][0],balance)


            if indi[i:i+1]['EMA20 Close'][0] < indi[i:i+1]['EMA50 Close'][0] and bought==True:
                if strategy[i:i+1]['crossover'][0]==True:
                    balance=balance*indi[i:i+1]['close'][0]
                    #print("sell",indi[i:i+1]['close'][0],balance)
                    bought=False
            if bought==False:
                latestBalance=balance
            if bought==True:
                latestBalance=latestBalance
            latestBalances.append(latestBalance)
            lastBalancesDates.append(indi[i:i+1].index[0])

        bals['dates']=lastBalancesDates
        bals['balance']=latestBalances
        bals.set_index('dates')
        bals.index = pd.to_datetime(bals.index)
        #print(bals)
        indi=indi.iloc[501: , :]
        indi['balance']=bals['balance'].to_numpy()
        #print(indi)
        plt.plot(indi)
        plt.show()

        print(indi.tail(50))


    def getIndicators(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        exchangePath = os.path.join(dir_path, self.exchange+"\\"+"BTC"+"\_1H\\").replace("\\","/")
        try:
            indi=pd.read_pickle(exchangePath+"indicators.pkl")
        except:
            indi=pd.DataFrame()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        exchangePath = os.path.join(dir_path, self.exchange+"\\"+"BTC"+"\_1H\\").replace("\\","/")
        data=pd.read_pickle(exchangePath+"pikl.pkl")
        data=data.sort_index()
        indi["EMA20 Close"] = ta.ema(data["close"], length=20)
        indi["EMA50 Close"] = ta.ema(data["close"], length=50)
        indi['close']=data['close']
        self.indi=indi


strat=Strategy("alex","coinbase",["if indi['EMA20 Close'] > indi['EMA50 Close'] and strategy['crossover']=='True'"], ["if EMA20 Close < EMA50 Close and strategy['crossover']=='True'"])

print(strat.getIndicators())
strat.backtest(500)


