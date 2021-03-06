import stockmarket as sm
import sys, getopt, math

class PartOneWeight(sm.Weighting):
    def __init__(self):
        pass
    
    def get_weight(self, mkt, stk, n=100):
        return -(stk.rcc(-1)-mkt.AvrRCC)/n
        
class PartTwoThreeWeight(sm.Weighting):
    def __init__(self, alphas):
        self.alphas = alphas
    
    def get_weight(self, mkt, stk, n=100):
        weight = 0;
        rcc = (stk.rcc(-1)-mkt.AvrRCC) / mkt.n
        roo = (stk.roo( 0)-mkt.AvrROO) / mkt.n
        roc = (stk.roc(-1)-mkt.AvrROC) / mkt.n
        rco = (stk.rco( 0)-mkt.AvrRCO) / mkt.n
        tvl = (stk.tvl(-1)-stk.AvrTVL) / mkt.n
        rvp = (stk.rvp(-1)-stk.AvrRVP) / mkt.n
        weight += (self.alphas[0] + self.alphas[4]*tvl + self.alphas[ 8]*rvp) * rcc
        weight += (self.alphas[1] + self.alphas[5]*tvl + self.alphas[ 9]*rvp) * roo
        weight += (self.alphas[2] + self.alphas[6]*tvl + self.alphas[10]*rvp) * roc
        weight += (self.alphas[3] + self.alphas[7]*tvl + self.alphas[11]*rvp) * rco
        return weight
        
class PartFourWeight(sm.Weighting):
    def __init__(self, alphas):
        self.alphas = alphas
    
    def get_weight(self, mkt, stk, n=100):
        weight = 0;
        rcc = (stk.rcc(-1) - mkt.AvrRCC) / mkt.n
        roo = (stk.roo( 0) - mkt.AvrROO) / mkt.n
        roc = (stk.roc(-1) - mkt.AvrROC) / mkt.n
        rco = (stk.rco( 0) - mkt.AvrRCO) / mkt.n
        tvl = (stk.tvl(-1) - stk.AvrTVL) / mkt.n
        rvp = (stk.rvp(-1) - stk.AvrRVP) / mkt.n
        weight += (self.alphas[0] + self.alphas[4]*tvl + self.alphas[ 8]*rvp) * rcc
        weight += (self.alphas[1] + self.alphas[5]*tvl + self.alphas[ 9]*rvp) * roo
        weight += (self.alphas[2] + self.alphas[6]*tvl + self.alphas[10]*rvp) * roc
        weight += (self.alphas[3] + self.alphas[7]*tvl + self.alphas[11]*rvp) * rco
        # weight += (self.alphas[0] + self.alphas[4]*tvl) * rcc
        # weight += (self.alphas[1] + self.alphas[5]*tvl) * roo
        # weight += (self.alphas[2] + self.alphas[6]*tvl) * roc
        # weight += (self.alphas[3] + self.alphas[7]*tvl) * rco
        # weight += self.alphas[12]*tvl/stk.AvrTVL
        # weight += self.alphas[13]*stk.rco(0)
        # weight += self.alphas[13]*rvp/stk.AvrRVP
        # weight += self.alphas[14]* 
        if (weight < 0 and mkt.date.isoweekday() == 5):
            weight*=1.2
            if mkt.date.day < 24:
                weight*=1.2
          
        return weight
            