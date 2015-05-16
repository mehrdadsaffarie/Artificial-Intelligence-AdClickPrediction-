import os
import sys
if __name__ == '__main__':
    if len(sys.argv)!=3:
        print 'usage: python getImageLabel.py dir output' 
        sys.exit(1)
    Dir = sys.argv[1] 
    images={}
    bs = os.listdir(Dir + 'Beautiful/')
    images[0] = bs
    digits = os.listdir(Dir + 'digit/')
    images[1] = digits 
    games = os.listdir(Dir + 'game/')
    images[2] = games 
    mcs = os.listdir(Dir + 'Men_clothe/')
    images[3] = mcs 
    wcs = os.listdir(Dir + 'Women_clothe/')
    images[4] = wcs 
    watches = os.listdir(Dir + 'Watch/')
    images[5] = watches 
    shoes = os.listdir(Dir + 'shoe/')
    images[6] = shoes 
    f=open(sys.argv[2],'w')
    lines = []
    for i in range(0,7):
        for item in images[i]:
            line = item + ' ' + str(i) + '\r\n'
            lines.append(line)
    f.writelines(lines)
    f.close()
