import codecs
import string
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def get_label_map():
	result = {}
	infile = codecs.open('../data/label.txt','r','utf-8')
	label_list = infile.readlines()
	for l in label_list:
		tmp = l.strip('\r\n').split(' ')
		if result.has_key(int(tmp[1]))==0:
			result[int(tmp[1])]=tmp[2]
	return result

def get_train_data():
	infile1 = codecs.open('../data/word_train.txt','r','utf-8')
	infile2 = codecs.open('../data/word_test.txt','r','utf-8')
	
	X_train = []
	y_train = []
	X_test = []
	train_id = []
	test_id = []

	X_train_tmp = infile1.readlines()
	for t in X_train_tmp:
		tmp = t.split('+-+')
		X_train.append(tmp[2])
		train_id.append(tmp[0])
		y_train.append(int(tmp[1]))
	X_test_tmp = infile2.readlines()
	for t in X_test_tmp:
		tmp = t.split('+-+')
		X_test.append(tmp[1])
		test_id.append(tmp[0])
	return (X_train,X_test,y_train,train_id,test_id)


def train_and_predict(X_train,X_test,y_train):	
	count_vect = CountVectorizer().fit(X_train)
	X_train_counts = count_vect.transform(X_train)
	X_test_counts = count_vect.transform(X_test)

	clf = MultinomialNB().fit(X_train_counts, y_train)
	y_test = clf.predict_proba(X_test_counts)
	y_final = y_test.argmax(1)
	y_final[numpy.where(y_test.max(1)<0.5)]=-1

	return y_final

	#print y_final
	#for a,b in zip(X_test,y_final):
	#	if b!=-1:
	#		ofile.write(a.strip('\r\n')+'--------->'+label_map[b]+'\r\n')
	#	else:
	#		ofile.write(a.strip('\r\n')+'--------->'+'-1'+'\r\n')
	

def write_word_and_result(train_id,X_train,y_train,test_id,X_test,y_test):

	label_map = get_label_map()
	ofile = codecs.open('../data/word&result.txt','w','utf-8')
	for a,b,c in zip(train_id,X_train,y_train):
		ofile.write(a+":"+b.strip('\r\n')+'--------->'+label_map[c]+" "+str(c)+'\r\n')
	for a,b,c in zip(test_id,X_test,y_test):
		if c==-1:
			ofile.write(a+":"+b.strip('\r\n')+'--------->'+"-1"+" -1"+'\r\n')
		else:
			ofile.write(a+":"+b.strip('\r\n')+'--------->'+label_map[c]+" "+str(c)+'\r\n')
	ofile.close()

def write_result(train_id,X_train,y_train,test_id,X_test,y_test):

	label_map = get_label_map()
	ofile = codecs.open('../data/result.txt','w','utf-8')
	for a,b,c in zip(train_id,X_train,y_train):
		ofile.write(a+","+str(c)+'\r\n')
	for a,b,c in zip(test_id,X_test,y_test):
		if c==-1:
			ofile.write(a+','+"-1"+'\r\n')
		else:
			ofile.write(a+","+str(c)+'\r\n')
	ofile.close()

if __name__ == '__main__':
	
	(X_train,X_test,y_train,train_id,test_id) = get_train_data()	
	y_test = train_and_predict(X_train,X_test,y_train)
	write_result(train_id,X_train,y_train,test_id,X_test,y_test)


	


