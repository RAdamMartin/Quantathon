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
    wgt = PartTwoThreeWeight(alphas)
    gains = []
    src.seek(0,0)
    for line in src:
        arr = line.split(', ')
        dst.write(arr[0] + ',')
        for j in range (1, len(arr), 6):
            mkt.update_stock(int(j/6), arr[j:j+6])
        if i > 2:
            mkt.set_averages()
            #CHANGE False TO True TO CHECK IND VALUES
            vals = mkt.get_delta(wgt, 0, False)
            delta = vals[0]/vals[1]
            dst.write(str(delta)+',')
            gains.append(delta)
            dst.write(str(sum(gains))+',')
            dst.write(str(vals[1])+',')
            dst.write(str(abs(delta)/delta)+',')
            for w in vals[2]:
                dst.write(str(w)+',')
            for d in vals[3]:
                dst.write(str(d)+',')
        else :
            for n in range(104):
                dst.write('99,')
        i += 1
        # if i > 262:
        #     break;
        dst.write('\n')
    
    # dst.write(str(gains)[1:-1])    
    return sharpe_ratio(gains)

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
    # alphas = [1,1,1,1, 1,1,1,1, 1,1,1,1]
#     alphas = [0.4432457, 0.92085776, -0.42230354, -0.19270864, -11.35844271,
#   11.53977411, 0.10461944, 11.31787075, 0.69421351, 0.94783086,
#   0.57559752, -0.12383039]
    alphas = [ 8.77519381e+05, -9.14005195e+05, -4.27731027e+05,
        1.45712088e+07, -1.06063059e+01, 1.26390855e+01,
        -1.64257209e+00, 4.03828123e+01, -2.25249306e+01,
         -2.19522184e+01, -2.18636677e+01, -2.25134671e+01]
    func = lambda x : get_result_from_alphas(src, dst, x)
    print(get_result_from_alphas(src, dst, alphas))
    src.close()
    dst.close()

if __name__ == "__main__":
    main(sys.argv[1:])