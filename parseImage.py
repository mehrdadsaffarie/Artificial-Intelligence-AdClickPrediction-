# -*- coding: utf-8 -*-
import os
import codecs

def readfile(filename):
	result = {}
	ifile = open(filename)
	ad_list = ifile.readlines()
	for a in ad_list:
		tmp = a.strip('\r\n').split(',')
		result[tmp[2]]=tmp[0]
	return result

if __name__ == '__main__':
	id_map = readfile('../data/ad.txt')
	ofile = codecs.open('../data/label.txt','w','utf-8')
	os.chdir('../data/classified')

	dir_list = os.listdir('.')
	num_label = -1
	for label in dir_list:
		#print label
		num_label+=1

		file_list = os.listdir(label)
		for f in file_list:
			f = f.strip('.jpg')
			#print int(f)
			if id_map.has_key(f):
				print 'yes'
				ofile.write(id_map[f]+" "+str(num_label)+" "+label+"\r\n")

	
