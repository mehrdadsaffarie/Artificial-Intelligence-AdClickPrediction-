import os
import numpy as np
import sys

IMG_F = 'imageLabels.txt'
TIT_F = 'titleLabels.txt'
USER_F = 'users.txt'

def readFile(f_name):
    f = open(f_name)
    lines = f.readlines()
    f.close()
    return lines

def saveFile(f_name,lines):
    f = open(f_name,'w')
    f.writelines(lines)
    f.close()

def loadImgFeatures():
    img_map = {}
    lines = readFile(IMG_F)
    for line in lines:
        item = line.strip().split(',')
        creativeID = item[0].split('.')[0]
        img_map[creativeID] = item[1]
    return img_map

def loadTitFeatures():
    tit_map = {}
    lines = readFile(TIT_F)
    for line in lines:
        item = line.strip().split(',')
        adID = item[0]
        tit_map[adID] = item[1]
    return tit_map

def loadUserFeatures():
    user_map = {}
    lines = readFile(USER_F)
    for i,line in enumerate(lines):
        if i%100000 == 0:
            print 'user i: ' + str(i)
        item = line.strip().split(',')
        userID = item[0]
        gender = item[1]
        gender_vec = gender2vec(gender)
        age = item[2]
        age_vec = age2vec(age)
        user_map[userID] = gender_vec + ' ' + age_vec 
    return user_map

def gender2vec(gender):
    if gender == '\N':
        return '0 0 1'
    if gender == '1':
        return '1 0 0'
    if gender =='2':
        return '0 1 0'

def age2vec(age):
    l = 51
    vec = np.zeros((l)) 
    if age=='\N':
        vec[50] = 1
    else:
        index = (int(age)-1)/2
        vec[index] = 1
    s = ''
    for i in range(0,l-1):
        s = s + str(vec[i]) + ' '
    return s + str(vec[l-1])

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'python toSample.py training.txt testing.txt trainSample.txt testSample.txt'
        sys.exit(0)
    s_train_f = sys.argv[1]    
    s_test_f = sys.argv[2]
    print 'load source ...'
    train_samples = readFile(s_train_f) 
    test_samples = readFile(s_test_f) 
    print 'load image features ...'
    img_map = loadImgFeatures()
    print 'load title features ...'
    tit_map = loadTitFeatures()
    print 'load user features ...'
    user_map = loadUserFeatures()
    print 'transform source records to samples ...'
    train_results = []
    for sample in train_samples:
        items = sample.strip().split(',')
        if user_map.has_key(items[0]) and tit_map.has_key(items[1]) and img_map.has_key(items[3]):
            r = user_map[items[0]]+' '+tit_map[items[1]]+' '+img_map[items[3]]+' '+items[5]
        train_results.append(r)
    test_results = []
    for sample in test_samples:
        items = sample.strip().split(',')
        if user_map.has_key(items[0]) and tit_map.has_key(items[1]) and img_map.has_key(items[3]):
            r = user_map[items[0]]+' '+tit_map[items[1]]+' '+img_map[items[3]]+' '+items[5]
        test_results.append(r)
    print('write samples to ...')
    saveFile(sys.argv[3],train_results)
    saveFile(sys.argv[4],test_results)

