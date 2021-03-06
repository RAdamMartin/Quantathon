#!/usr/bin/python

import stockmarket as sm
import weightings as wgts
import numpy as np
import sys, getopt, math
import datetime
from scipy import optimize 


def sharpe_ratio(gains):
    print(len(gains))
    print('ret: ' + str(sum(gains)/len(gains)))
    print('std: '+str(np.std(gains)))
    return math.sqrt(252)*sum(gains)/len(gains)/np.std(gains)

def get_result_from_alphas(src, dst, alphas):
    start = 0#348
    end = 500
    mkt = sm.Market(100)
    i = 1;
    # wgt = wgts.PartTwoThreeWeight(alphas)
    # wgt = wgts.EqualWeight()
    wgt = wgts.PartFourWeight(alphas)
    # wgt = wgts.PartOneWeight()
    gains = []
    src.seek(0,0)
    dst.write('date,')
    dst.write('rp,')
    dst.write('rp to date,')
    dst.write('sum of abs(fill*weight),')
    dst.write('sum of fill*weight,')
    dst.write('up or down,')
    for n in range(100):
        dst.write(str(n)+',')
    dst.write('\n')
    
    for line in src:
        if i >= start:
            arr = line.split(', ')
            dst.write(arr[0] + ',')
            mkt.date = datetime.datetime.strptime(arr[0],"%Y%m%d")
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
            dst.write(str(vals[1])+',') #denom
            dst.write(str(vals[4])+',') #sumfills
            dst.write(str(abs(delta)/delta)+',')
            for w in vals[2]:
                dst.write(str(w)+',')
            for d in vals[3]:
                dst.write(str(d)+',')
        else :
            for n in range(105):
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
#     alphas = [-8.77519381e+05, 9.14005195e+05, 4.27731027e+05,
#         -1.45712088e+07, 1.06063059e+01, -1.26390855e+01,
#         1.64257209e+00, -4.03828123e+01, -2.25249306e+01,
#          2.19522184e+01, 2.18636677e+01, 2.25134671e+01] #6.7 From Powell
#     alphas = [-7.69259494e+05 ,  1.57069517e+06 ,  4.83853959e+05 , -1.32479662e+07
#    ,3.13196288e+00 , -1.82910156e+01  , 7.43488770e-01 , -2.94518368e+01,
#   -2.25249306e+01 ,  2.19522184e+01  , 2.18636677e+01 ,  2.25134671e+01]#6.64 From Powell
    # alphas = [-923352.272128,933037.630522,459420.822868,-14964690.9628,
    # 10.229203184,-11.6072353272,1.05610904785,-41.3899102335,
    # -12.3025940785,32.3431056715,32.0138949138,32.355858087] #6.73736946266
    
    
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
    # alphas = [1.8782638384e+15,-1.76310246294e+15,2.22561122593e+15,-5.09259689959e+20,
    #         4.94094681408e+13,-2.63145299567e+13,-8.05466827805e+13,8.51677955484e+14,
    #         4849677516.5,4849677065.54,4849676794.55,4849677707.27] #0.8707
    # alphas = [-12305744.8561,17114633.1908,1384387.44545,-204039650.192,65.9194844093,-197.737055601,82.0833150333,462.416189737,178.761685525,137.320866048,451.038278764,-350.021344633] #0.896330505151
    # alphas = [-12290958.4134,17110258.2704,1384388.29439,-204039649.694,65.9731013677,-198.145585709,82.3377351112,462.242022445,180.761195753,137.242892137,451.179192921,-349.556657818]
    alphas = [-12290958.4134,17110258.2704,1384388.29439,-204039649.694,65.9731013677,-198.143057029,82.3377431634,462.24202109,178.761195769,137.242892137,451.179192921,-349.556657818]
    
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