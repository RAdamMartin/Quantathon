#!/usr/bin/python

import stockmarket as sm
import weightings as wgts
import numpy as np
import sys, getopt, math
from scipy import optimize 


def sharpe_ratio(gains):
    # print(gains)
    print('ret: ' + str(sum(gains)/len(gains)))
    print('std: '+str(np.std(gains)))
    return math.sqrt(252)*sum(gains)/len(gains)/np.std(gains)

def get_result_from_alphas(src, dst, alphas):
    start = 0#348
    end = 500
    mkt = sm.Market(100)
    i = 1;
    wgt = wgts.PartTwoThreeWeight(alphas)
    # wgt = wgts.EqualWeight()
    # wgt = wgts.PartFourWeight(alphas)
    gains = []
    src.seek(0,0)
    for line in src:
        if i >= start:
            arr = line.split(', ')
            dst.write(arr[0] + ',')
            for j in range (1, len(arr), 6):
                mkt.update_stock(int(j/6), arr[j:j+6])
        if i > start+2:
            mkt.set_averages()
            #CHANGE False TO True TO CHECK IND VALUES
            # print(arr[0])
            vals = mkt.get_delta(wgt, 1, True)
            delta = vals[0]/vals[1]
            # gains.append(mkt.calculate_delta(wgt, 1, False))
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
        # if i > end:
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
    #part 2
#     alphas = [ -1.40079453 ,  2.15137419  , 3.84102477 , -4.80420109 ,  0.66858495,
#   10.8904451 , -11.62914075 ,-11.95806813  ,-0.81271439 , -0.4571093,
#   -0.42007713 ,  0.39063521] #1.6 buckets
    # alphas = [-8.77519381e+05, 9.14005195e+05, 4.27731027e+05,
    #     -1.45712088e+07, 1.06063059e+01, -1.26390855e+01,
    #     1.64257209e+00, -4.03828123e+01, -2.25249306e+01,
    #      2.19522184e+01, 2.18636677e+01, 2.25134671e+01] #6.7 From Powell
#     alphas = [-7.69259494e+05 ,  1.57069517e+06 ,  4.83853959e+05 , -1.32479662e+07
#    ,3.13196288e+00 , -1.82910156e+01  , 7.43488770e-01 , -2.94518368e+01,
#   -2.25249306e+01 ,  2.19522184e+01  , 2.18636677e+01 ,  2.25134671e+01]#6.64 From Powell
    
    # alphas = [  1.41538746e+12,  -1.72222380e+12,   2.57813351e+12,
    #     -1.79483444e+17,   5.31067896e+11,  -3.71009826e+12,
    #     -1.72333607e+11,   3.16643058e+11,   5.44634657e+09,
    #      5.44634657e+09,   5.44634657e+09,   5.44634657e+09]4.633 From Powell
    
    #part 3
#     alphas = [ 110.85246204 ,  59.85486885 , -75.46268603 ,  12.00436449 ,  15.76120424,
#   244.19472511, -261.5698981,  -268.70619013 , 184.60143229, -137.38079724,
#    32.06041834, -154.87491841]
    # alphas = [-5.12564233e+02,  -1.08932586e+04,   9.64668964e+03,
    #     -2.19508336e+20,   9.65522860e+12,  -2.15358189e+13,
    #     -6.78977830e+01,   2.21856089e+14,   2.10870757e+01,
    #      2.09766044e+01,   2.16107982e+01,   2.08729797e+01] #0.86 From Powell
#     alphas = [1.23087264e+14 , -1.49770873e+14 ,  2.24203908e+14 , -1.56085359e+19,
#    2.51091012e+11 , -1.58643820e+12 , -1.97548916e+12 ,  9.95654809e+12,
#    4.73634191e+11  , 4.73634191e+11,   4.73634191e+11  , 4.73634191e+11]
#     alphas = [1.41538746e+12 , -1.72222380e+12  , 2.57813351e+12 , -1.79483444e+17,
#    1.98851186e+10 , -1.82425433e+10 , -2.27162625e+10 ,  3.17193513e+11,
#    5.44634656e+09  , 5.44634656e+09  , 5.44634656e+09  , 5.44634656e+09] #0.87 Powell bins
#     alphas = [-4.19755996 , 7.24741087 , 0.32561918, -6.16136174 , 0.7846708 ,  0.92218809,
#  -3.38091198, -4.81106429, -7.76693095, -4.26818569 , 5.60763459 , 8.89775721]
    
    #part 4
    # alphas = [1.41538746e+12 , -1.72222380e+12  , 2.57813351e+12 , -1.79483444e+17,
    # 1.98851186e+10 , -1.82425433e+10 , -2.27162625e+10 ,  3.17193513e+11,
    # 5.44634656e+09  , 5.44634656e+09  , 5.44634656e+09  , 5.44634656e+09, 0.0, 0.0]
    
    func = lambda x : get_result_from_alphas(src, dst, x)
    print(get_result_from_alphas(src, dst, alphas))
    src.close()
    dst.close()

if __name__ == "__main__":
    main(sys.argv[1:])