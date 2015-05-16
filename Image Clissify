import matplotlib.image as mpimg
import os
import numpy
import sys
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.externals import joblib

ATT_NUM = 210*160*3

def getImages(file_name):
    f = open(file_name)
    lines = f.readlines()
    f.close()
    images = {}
    for line in lines:
        tmp = line.strip().split(' ')
        images[tmp[0]] = int(tmp[1])
    return images

def getSamples(images,im_dir):
    X = numpy.ones((len(images),ATT_NUM))
    Y = numpy.ones((len(images)))
    keys = images.keys()
    for i,k in enumerate(keys):
        Y[i] = images[k]
        im = mpimg.imread(im_dir + k)
        data = im.reshape((ATT_NUM))
        X[i,:] = data
    return X,Y

def myPredict(svc,pca,im_dir):
    results = []
    images = os.listdir(im_dir)
    for image in images:
        im = mpimg.imread(im_dir + image)
        if im.shape[2] == 3:
    	    XT = numpy.ones((1,ATT_NUM))
            XT[0,:] = im.reshape((ATT_NUM))
            XT_r = pca.transform(XT)
            pros = svc.predict_proba(XT_r)
	    pro = pros[0,:]
            if pro.max()<0.5:
            	results.append(image + ',' + '-1' + '\r\n')
	    else:
            	results.append(image + ',' + str(pro.argmax()) + '\r\n')
        else:
            results.append(image + ',' + '-1' + '\r\n')
    return results

def saveFile(lines,file_name):
    f=open(file_name,'w')
    f.writelines(lines)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'python imageClassify imageSampleFile imageDir model_path' 
        sys.exit(0)
    im_dir = sys.argv[2]
    model_dir = sys.argv[3]
    print 'read images list ...'
    images = getImages(sys.argv[1])
    print 'load image ...'
    X,Y = getSamples(images,im_dir)
    print 'pca ...'
    if os.path.exists(model_dir+'pca.pkl'):
	pca = joblib.load(model_dir+'pca.pkl')
    else:
    	pca = PCA(n_components=8)
    	pca.fit(X)
	joblib.dump(pca,model_dir+'pca.pkl')
    print('explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_))
    print 'train with SVM ...'
    X_r = pca.transform(X)
    print 'X_r shape: ' + str(X_r.shape[0]) + ', ' + str(X_r.shape[1])
    svc = svm.SVC(probability=True)
    svc.fit(X_r, Y)
    print 'predict with SVM ...'
    results = myPredict(svc,pca,im_dir)
    saveFile(results,'imageLabels.txt')
