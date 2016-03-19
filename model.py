#!/usr/bin/python

import stockmarket as sm
import numpy as np
import sys, getopt

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

    src = open(inputfile, 'r')
    dst = open(outputfile, 'w')

    mkt = sm.Market(100)
    i = 1;
    wgt = sm.PartOneWeight()
    gains = []
    for line in src:
        arr = line.split(', ')
        for j in range (1, len(arr), 6):
            mkt.update_stock(int(j/6), arr[j:j+6])
        if i > 2:
            mkt.set_averages()
            gains.append(mkt.calculate_delta(wgt,0,False))
        i += 1
    
    src.close()
    dst.write(str(gains)[1:-1])   
    dst.close()
    

if __name__ == "__main__":
    main(sys.argv[1:])