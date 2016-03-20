#!/usr/bin/python
maxs = 0
import stockmarket as sm
import numpy as np
import sys, getopt, math
from scipy import optimize
import weightings as wgts

def sharpe_ratio(gains):
    return math.sqrt(252)*sum(gains)/len(gains)/np.std(gains)

def get_result_from_alphas(hist, wgt, alphas, start=1, check_fill=False):
    global maxs
    gains = hist.getDelta(wgt(alphas), start, check_fill)
    score = sharpe_ratio(gains)
    if score > maxs:
        maxs = score
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

    wgt = wgts.PartTwpThreeWeight
    # alphas = np.random.rand(13)
    # alphas = map((lambda x : 2*(x-0.5)), alphas)
    # alphas = [1.41538746e+12 , -1.72222380e+12  , 2.57813351e+12 , -1.79483444e+17,
    # 1.98851186e+10 , -1.82425433e+10 , -2.27162625e+10 ,  3.17193513e+11,
    # 5.44634656e+09  , 5.44634656e+09  , 5.44634656e+09  , 5.44634656e+09, 0.0, 0.0]
    alphas = [-8.77519381e+05, 9.14005195e+05, 4.27731027e+05,
        -1.45712088e+07, 1.06063059e+01, -1.26390855e+01,
        1.64257209e+00, -4.03828123e+01, -2.25249306e+01,
         2.19522184e+01, 2.18636677e+01, 2.25134671e+01]
    # alphas = []
    # bounds = []
    # for n in range(12):
    #     # alphas[n] = 0.1
    #     bounds.append((-10,10))
    # alphas = [ -1.37873689e+00,  -2.86811840e+01,   2.06475215e+00,
    #     -3.00192275e+01,   1.85853877e+03,   1.08544918e+03,
    #     -2.31144825e+03,  -1.14817264e+03,   1.00000000e+00,
    #      1.00000000e+00,   1.00000000e+00,   1.00000000e+00]
    func = lambda x : get_result_from_alphas(hist, wgt, x, 1, False)
    res = optimize.basinhopping(func=func, x0=alphas, niter=50, minimizer_kwargs={"method": "Powell"})
    # res = optimize.differential_evolution(func, bounds)
    # res = optimize.minimize(fun=func, x0=alphas, method='Powell')
    print(res)  
    # print(func(alphas))
    # dst.close()

if __name__ == "__main__":
    main(sys.argv[1:])
