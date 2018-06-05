__author__ = 'shiyu'


import pickle
import sys

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def Preprocess(text):
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens]
    stops = stopwords.words('english')
    tokens = [t for t in tokens if t  not in stops]
    pst = PorterStemmer()
    tokens = [pst.stem(t) for t in tokens]
    text = ' '.join(tokens)
    return text

f = open('v.pickle','rb')
vectorizer = pickle.load(f)
f = open('m.pickle','rb')
model = pickle.load(f)

comment = sys.argv[1] #'I like to play it safe.'
processedComment = Preprocess(comment)
X = vectorizer.transform([processedComment,]).toarray()
ans = int(model.predict(X))

if ans == -1:
	print('conservative')
if ans == 1:
	print('aggressive')
