#!/usr/bin/python

import stockmarket as sm
import numpy as np
import sys, getopt, math
from scipy import optimize 

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

def sharpe_ratio(gains):
    print(gains)
    print('ret: ' + str(sum(gains)/len(gains)))
    print('std: '+str(np.std(gains)))
    return math.sqrt(252)*sum(gains)/len(gains)/np.std(gains)

def get_result_from_alphas(src, dst, alphas):
    mkt = sm.Market(100)
    i = 1;
    wgt = PartOneWeight()
    gains = []
    src.seek(0,0)
    for line in src:
        arr = line.split(', ')
        for j in range (1, len(arr), 6):
            mkt.update_stock(int(j/6), arr[j:j+6])
        if i > 2:
            mkt.set_averages()
            #CHANGE False TO True TO CHECK IND VALUES
            gains.append(mkt.calculate_delta(wgt,0,False))
        i += 1
        if i > 262:
            break;
    dst.write(str(gains)[1:-1])    
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
    print('Input file is', inputfile)
    print('Output file is', outputfile)

    dst = open(outputfile, 'w')
    src = open(inputfile, 'r')

    src.seek(0,0)
    alphas = [1,1,1,1, 1,1,1,1, 1,1,1,1]
    func = lambda x : get_result_from_alphas(src, dst, x)
    # alphas = [ 0.99991629,  1.00006079,  0.99992389,  0.99999325, -2.85022159,
    #     9.39757373, -2.80218762,  0.92436028,  1.        ,  1.        ,
    #     1.        ,  1.        ]
#     alphas = [1.00627894 , 1.00627894 , 1.00627894 , 1.00627894 , 1.00627894 , 1.01773727,
#   0.99461806 , 0.97485532 , 1.00627894 , 1.00627894 , 1.00627894 , 1.00627894]
    # res = optimize.fmin(func, alphas)
    # res = optimize.fmin(func=func, x0=alphas, maxiter=100)
    # print(res)  
    print(get_result_from_alphas(src, dst, alphas))
    src.close()
    dst.close()

if __name__ == "__main__":
    main(sys.argv[1:])