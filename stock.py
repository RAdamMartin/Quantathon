class stock(object):
    def __init__(self, sc=0):
        self.so = 0
        self.sh = 0
        self.sl = 0
        self.sc = 0
        self.sc_prev = sc
        self.tvl = 0
        self.ind = 0