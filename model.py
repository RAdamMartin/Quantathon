#!/usr/bin/python

import stockmarket as sm
import numpy as np
import sys, getopt, math

class PartOneWeight(sm.Weighting):
    def __init__(self):
        pass
    
    def get_weight(self, mkt, stk, n=100):
        return -(1/n)*(stk.roc()-mkt.AvrRCC)
        
class PartTwoThreeWeight(sm.Weighting):
    def __init__(self, alphas):
        self.alphas = alphas
    
    def get_weight(self, mkt, stk, n=100):
        weight = 0;
        rcc = (stk.rcc(-1)-mkt.AvrRCC) / mkt.n
        roo = (stk.roo( 0)-mkt.AvrROO) / mkt.n
        roc = (stk.roc(-1)-mkt.AvrROC) / mkt.n
        rco = (stk.rco( 0)-mkt.AvrRCO) / mkt.n
        tvl = (stk.tvl(-1)-mkt.AvrTVL) / mkt.n
        rvp = (stk.rvp(-1)-mkt.AvrRVP) / mkt.n
        weight += (self.alphas[0] + self.alphas[4]*tvl + self.alphas[ 8]*rvp) * rcc
        weight += (self.alphas[1] + self.alphas[5]*tvl + self.alphas[ 9]*rvp) * roo
        weight += (self.alphas[2] + self.alphas[6]*tvl + self.alphas[10]*rvp) * roc
        weight += (self.alphas[3] + self.alphas[7]*tvl + self.alphas[11]*rvp) * rco
        return weight

def sharpe_ratio(gains):
    return math.sqrt(252)*sum(gains)/len(gains)/np.std(gains)

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
    print('Input file is', inputfile)
    print('Output file is', outputfile)

    dst = open(outputfile, 'w')
    src = open(inputfile, 'r')

    mkt = sm.Market(100)
    i = 1;
    #SET WEIGHTINGS HERE
    alphas = np.random.rand(12)
    #alphas = [1,1,1,1, 0,0,0,0, 0,0,0,0]
    wgt = PartTwoThreeWeight(alphas)
    gains = []
    for line in src:
        arr = line.split(', ')
        for j in range (1, len(arr), 6):
            mkt.update_stock(int(j/6), arr[j:j+6])
        if i > 2:
            mkt.set_averages()
            #CHANGE False TO True TO CHECK IND VALUES
            gains.append(mkt.calculate_delta(wgt,1,False))
        i += 1
    
    src.seek(0,0)
    for a in alphas:
        dst.write(str(a)+',')
    dst.write(str(sharpe_ratio(gains))+'\n')   
        
    src.close()
    dst.close()
    
    # print(np.std(gains))
    # print(sharpe_ratio(gains))

if __name__ == "__main__":
    main(sys.argv[1:])