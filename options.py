import numpy as np
import pandas as pd
import yfinance as yf

class Options:
    def __init__(self, sym, num):
        self.num = num
        self.sym = sym

    def make_table(self, optiondates, numbermonth):
        list_out = []
        month1 = callsdf[numbermonth]

        for i in range(len(month1['strike'])):
            list_in = []

            for k in range(len(optiondates)):
                for j in range(len(callsdf[k]['strike'])):
                    if month1['strike'][i] == callsdf[k]['strike'][j]:
                        b = callsdf[k].iloc[j]

                        list_in.append(b)
                        break
            list_in = pd.DataFrame(list_in)

            list_out.append(list_in)
        return list_out[self.num], list_out

    def begin(self):
        stock = yf.Ticker(self.sym)
        return stock.options

    def get_option_data(self, optiondates, calls=True):
        #         stock = yf.Ticker(sym)
        #         self.optiondates = stock.options

        if calls == True:
            alist = []
            for i in range(len(optiondates)):
                aoption = yf.Ticker(self.sym).option_chain(optiondates[i])
                alist.append(aoption)
            stockdf = pd.DataFrame(alist)
            callsdf = stockdf['calls']
            for i in range(len(optiondates)):
                callsdf[i]['expiration'] = optiondates[i]

            return callsdf
        if calls == False:      #then it will be puts.

            alist = []
            for i in range(len(stock.options)):
                aoption = yf.Ticker.option_chain(optiondates[i])
                alist.append(aoption)
            stockdf = pd.DataFrame(alist)
            putsdf = stockdf['puts']
            for i in range(len(optiondates)):
                putsdf[i]['expiration'] = optiondates[i]

            return putsdf


sym = 'GME'#input stock
startnum = 3
num = 6 # dataframe number output you want, how many of strike prices you want.
optionobj = Options(sym, num)
optiondates = optionobj.begin()
callsdf = optionobj.get_option_data(optiondates)

print("it worked")
import matplotlib.pyplot as plt

# avg = (forgraph['bid'] + forgraph['ask'])/2

fig, axes = plt.subplots(nrows=num-startnum, ncols=1, figsize=(10,6))  #use nrows=len(list_of_df) for full list
fig.tight_layout()
callsdf = optionobj.get_option_data(optiondates)


for i in range(startnum,num):    #use range(len(list_of_df): for finding all graphs.

    forgraph, _ = optionobj.make_table(optiondates, i+1)
    avg = (forgraph['bid'] + forgraph['ask'])/2
    axes[i-startnum].plot(forgraph['expiration'], avg)
    axes[i-startnum].set_title(str(forgraph['strike'].unique()))


plt.show()