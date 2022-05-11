import sounddevice as sd
from scipy.io.wavfile import write
import pickle
import librosa
import numpy as np
from hmmlearn import hmm


def normalize(feature):
    normalized = np.full_like(feature, 0)
    for i in range(feature.shape[0]):        
        normalized[i] = feature[i] - np.mean(feature[i]) # đưa trung bình về 0
        normalized[i] = normalized[i] / np.max(np.abs(normalized[i])) # đưa khoảng giá trị về [-1, 1]
    return normalized

def get_template(path):
	y, sr = librosa.load(path)
	mfcc = librosa.feature.mfcc(y = y)
	delta = librosa.feature.delta(mfcc)
	delta2 = librosa.feature.delta(mfcc, order = 2)
	return normalize(np.transpose(np.concatenate([mfcc, delta, delta2], axis = 0),[1,0]))

hmm_models = []
with open('model', 'rb') as handle:
	hmm_models = pickle.load(handle)

def predict(test_file):
	t = get_template(test_file)
	max_score = 0
	predicted_label = ""
	scores = []
	for item in hmm_models:
		model, label = item
		score = model.score(t)
		scores.append(score)
		if score > max_score:
			max_score = score
			predicted_label = label
	return predicted_label, max_score, scores


# print(predict('b1.wav'))

while input() != 'c':
	fs = 22050  # Sample rate
	seconds = 1.5  # Duration of recording
	print('Nói:')
	myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
	sd.wait()  # Wait until recording is finished
	write('output.wav', fs, myrecording)  # Save as WAV file
	print(predict('output.wav'))
