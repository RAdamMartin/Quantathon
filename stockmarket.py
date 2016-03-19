from abc import ABCMeta

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
    def __init__(self, sc=0):
        self.cur  = Ticker()
        self.prev = Ticker()
        
    def set_vals(self, arr):
        self.prev = self.cur
        self.cur.set_vals(arr)

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
        
    def ind(self):
        return self.cur.ind    
            
        
class Weighting(object):
    __metaclass__ = ABCMeta

    def get_weight(self, mkt, stk, n):
        pass
        
class PartOneWeight(Weighting):
    def __init__(self):
        pass
    
    def get_weight(self, mkt, stk, n=100):
        return -(1/n)*(stk.roc()-mkt.AvrRCC)
        
class PartTwoThreeWeight(Weighting):
    def __init__(self, alphas):
        self.alphas = alphas
    
    def get_weight(self, mkt, stk, n=100):
        weight = 0;
        return weight
        
class Market(object):
    def __init__(self, n=100):
        self.stocks = []
        self.weights = []
        self.n = n
        self.AvrROO = 0
        self.AvrROC = 0
        self.AvrRCO = 0
        self.AvrRCC = 0
        self.AvrTVL = 0
        self.AvrRVP = 0
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
        self.AvrTVL = 0
        self.AvrRVP = 0
        for s in self.stocks:
            self.AvrROO = s.roo()
            self.AvrROC = s.roc(-1)
            self.AvrRCO = s.rco()
            self.AvrRCC = s.rcc(-1)
            self.AvrTVL = s.tvl(-1)
            # self.AvrRVP = 0
        self.AvrROO /= self.n
        self.AvrROC /= self.n
        self.AvrRCO /= self.n
        self.AvrRCC /= self.n
        self.AvrTVL /= self.n
        self.AvrRVP /= self.n

    def calculate_delta(self, weighter, start=1, check_fill=False):
        total = 0
        denom = 0
        for i in range(self.n):
            stk = self.stocks[i]
            delta = stk.rco()
            if start == 0 :
                delta = stk.rcc()
            weight = weighter.get_weight(self, stk)
            ind = stk.ind()
            if (not check_fill) or (ind*weight >= 0) : 
                total += weight*delta
                denom += weight

        return total/denom