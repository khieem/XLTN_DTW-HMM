import os
import re
import librosa
import numpy as np


def normalize(feature):
	normalized = np.full_like(feature, 0)
	for i in range(feature.shape[1]):
		normalized[:,i] = feature[:,i] - np.mean(feature[:,i]) # đưa trung bình về 0
		normalized[:,i] = normalized[:,i] / np.max(np.abs(normalized[:,i])) # đưa khoảng giá trị về [-1, 1]
	return normalized

def get_template(path):
	audio = librosa.load(path)[0]
	mfcc = librosa.feature.mfcc(y=audio, n_mfcc=13)
	delta = librosa.feature.delta(mfcc)
	delta2 = librosa.feature.delta(mfcc, order=2)
	return normalize(np.concatenate((mfcc, delta, delta2)))

def build_average_template(command, metric='euclidean'): # command = a b len xuong trai phai ban
	path = os.getcwd() + '/wav/train/' + command + '/'
	p_train = [path + str(i) + '.wav' for i in range(1, 4)]
	templates = [get_template(p) for p in p_train]
	#print(type(templates[0]))
	_, align01 = librosa.sequence.dtw(X=templates[0], Y=templates[1])
	_, align02 = librosa.sequence.dtw(X=templates[0], Y=templates[2])
	count = np.ones(len(templates[0][0])) # count[i] đếm số vectơ được dóng vào vị trí i của template chuẩn
	sum = templates[0].copy() # tổng của 3 template sau khi dóng

	for t, q in align01:
		count[t] += 1
		sum[:,t] += templates[1][:,q]
	
	for t, q in align02:
		count[t] += 1
		sum[:,t] += templates[2][:,q]

	average_template = sum / count

	return average_template


commands = ['a', 'b', 'len', 'xuong', 'trai', 'phai', 'ban', 'nhay']
khl = ['a', 'b', 'lên', 'xuống', 'trái', 'phải', 'bắn', 'nhảy']

templates = [build_average_template(cmd) for cmd in commands]

def recognize(path):
	template = get_template(path)
	cost = [librosa.sequence.dtw(template, templates[i])[0][-1,-1] for i in range(len(templates))]
	return khl[np.argmin(cost)]

def test():
	path = os.getcwd() + '/wav/test'
	total = 0
	correct = 0
	wrong = {'a':0, 'b':0, 'len':0, 'xuong':0, 'trai':0, 'phai':0, 'ban':0, 'nhay':0}
	for filename in os.scandir(path):
		total += 1
		label = re.search('^[a-z]+', filename.name).group()
		if label == recognize(filename):
			correct += 1
		else:
			wrong[label] = wrong[label] + 1
	print('độ chính xác: {:.2f}%\n'.format(correct/total*100))
	print(wrong)


#print(recognize('/home/khiemvn/bt/wav/test/xuong224.wav'))
test()