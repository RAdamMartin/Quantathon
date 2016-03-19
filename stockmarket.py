from abc import ABCMeta
import numpy as np
import math
import copy

class Ticker(object):
    def __init__(self):
        self.so = 0
        self.sh = 0
        self.sl = 0
        self.sc = 0
        self.tvl = 0
        self.ind = 0
        self.sc_prev = 0
        self.so_prev = 0

    def set_vals(self, arr):
        self.sc_prev = self.sc
        self.so_prev = self.so

        self.so  = float(arr[0])
        self.sh  = float(arr[1])
        self.sl  = float(arr[2])
        self.sc  = float(arr[3])
        self.tvl =   int(arr[4])
        self.ind =   int(arr[5])
        
    def __str__(self):
        return  str(self.so) + ',' + \
                str(self.sh) + ',' + \
                str(self.sl) + ',' + \
                str(self.sc) + ',' + \
                str(self.tvl)+ ',' + \
                str(self.ind)  

class Stock(object):
    rvp_const = 1/4/np.log(2)
    
    def __init__(self, sc=0):
        self.cur  = Ticker()
        self.prev = Ticker()
        self.tvl_arr = []
        self.rvp_arr = []
        self.AvrTVL = 0
        self.AvrRVP = 0
        
    def set_vals(self, arr):
        self.prev = copy.deepcopy(self.cur)
        self.cur.set_vals(arr)
        
        self.tvl_arr.append(self.tvl())
        self.rvp_arr.append(self.rvp())
        if len(self.tvl_arr) > 200:
            self.tvl_arr.pop(0)
        if len(self.rvp_arr) > 200:
            self.rvp_arr.pop(0)
            
        self.AvrTVL = sum(self.tvl_arr)/len(self.tvl_arr)
        self.AvrRVP = sum(self.rvp_arr)/len(self.rvp_arr)

    def rcc(self, t=0):
        tick = self.cur
        if t == -1:
            tick = self.prev
        
        return tick.sc/tick.sc_prev - 1
    
    def rco(self, t=0):
        tick = self.cur
        if t == -1:
            tick = self.prev
        
        return tick.so/tick.sc_prev - 1

    def roc(self, t=0):
        tick = self.cur
        if t == -1:
            tick = self.prev
        
        return tick.sc/tick.so - 1

    def roo(self, t=0):
        tick = self.cur
        if t == -1:
            tick = self.prev
        
        return tick.so/tick.so_prev - 1
        
    def tvl(self, t=0):
        tick = self.cur
        if t == -1:
            tick = self.prev
        
        return tick.tvl  
        
    def rvp(self, t=0):
        tick = self.cur
        if t == -1:
            tick = self.prev
        
        return self.rvp_const*math.pow(np.log(tick.sh)-np.log(tick.sl),2)
        
    def ind(self):
        return self.cur.ind    
            
        
class Weighting(object):
    __metaclass__ = ABCMeta

    def get_weight(self, mkt, stk, n):
        pass
        
class Market(object):
    def __init__(self, n=100):
        self.stocks = []
        self.weights = []
        self.n = n
        self.AvrROO = 0
        self.AvrROC = 0
        self.AvrRCO = 0
        self.AvrRCC = 0
        for i in range(n):
            self.stocks.append(Stock(0))
            self.weights.append(0)
            
    def update_stock(self, ind, arr):
        self.stocks[ind].set_vals(arr)
        
    def display_stocks(self):
        for s in self.stocks:
            print(s.cur)

    def set_averages(self):
        self.AvrROO = 0
        self.AvrROC = 0
        self.AvrRCO = 0
        self.AvrRCC = 0
        for s in self.stocks:
            self.AvrROO += s.roo()
            self.AvrROC += s.roc(-1)
            self.AvrRCO += s.rco()
            self.AvrRCC += s.rcc(-1)
        self.AvrROO /= self.n
        self.AvrROC /= self.n
        self.AvrRCO /= self.n
        self.AvrRCC /= self.n

    def calculate_delta(self, weighter, start=1, check_fill=False):
        total = 0
        denom = 0
        for i in range(self.n):
            stk = self.stocks[i]
            delta = stk.roc()
            if start == 0 :
                delta = stk.rcc()
            weight = weighter.get_weight(self, stk)
            ind = stk.ind()
            if (not check_fill) or (ind*weight >= 0) : 
                total += weight*delta
                denom += abs(weight)

        return total/denom
        
class MarketHistory(object):
    def __init__(self):
        self.markets = []
    
    def addNewDay(self, mkt):
        self.markets.append(copy.deepcopy(mkt))
        
    def getDelta(self, wgt, start=1, check_fill=False):
        gains = []
        for m in self.markets:
            gains.append(m.calculate_delta(wgt, start, check_fill))
        return gains