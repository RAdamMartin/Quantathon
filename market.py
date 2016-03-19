class market(object):
    def __init__(self,n=100):
        self.stocks = []
        for i in range(n):
            self.stocks.append(Stock())