#!/usr/bin/python

import stockmarket as sm
import numpy as np
import sys, getopt, math
from scipy import optimize

class PartOneWeight(sm.Weighting):
    def __init__(self):
        pass
    
    def get_weight(self, mkt, stk, n=100):
        return -(1/n)*(stk.rcc()-mkt.AvrRCC)
        
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

def sharpe_ratio(gains):
    return math.sqrt(252)*sum(gains)/len(gains)/np.std(gains)

def get_result_from_alphas(hist, wgt, alphas, start=1, check_fill=False):
    gains = hist.getDelta(wgt(alphas), start, check_fill)
    print(alphas)
    return -sharpe_ratio(gains)

def main(argv):
#adapted from http://www.tutorialspoint.com/python/python_command_line_arguments.htm
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('model.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('model.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    # print('Input file is', inputfile)
    # print('Output file is', outputfile)

    # dst = open(outputfile, 'w')
    src = open(inputfile, 'r')

    mkt = sm.Market(100)
    hist = sm.MarketHistory()
    i = 1;
    for line in src:
        arr = line.split(', ')
        for j in range (1, len(arr), 6):
            mkt.update_stock(int(j/6), arr[j:j+6])
        if i > 2:
            mkt.set_averages()
            hist.addNewDay(mkt)
        i += 1
        if i >= 265: #end sample size
            break;
    src.close() 

    wgt = PartTwoThreeWeight
    alphas = np.random.rand(12)
    alphas = map((lambda x : 2*(x-0.5)), alphas)
    # alphas = []
    bounds = []
    for n in range(12):
        # alphas[n] = 0.1
        bounds.append((-10,10))
    # alphas = [ -1.37873689e+00,  -2.86811840e+01,   2.06475215e+00,
    #     -3.00192275e+01,   1.85853877e+03,   1.08544918e+03,
    #     -2.31144825e+03,  -1.14817264e+03,   1.00000000e+00,
    #      1.00000000e+00,   1.00000000e+00,   1.00000000e+00]
    func = lambda x : get_result_from_alphas(hist, wgt, x, 1, True)
    res = optimize.basinhopping(func=func, x0=alphas, niter=200, minimizer_kwargs={"method": "TNC"})
    # res = de.differential_evolution(func, bounds)
    # res = optimize.minimize(fun=func, x0=alphas, method='Powell')
    print(res)  
    # print(func(alphas))
    # dst.close()

if __name__ == "__main__":
    main(sys.argv[1:])