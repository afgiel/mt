import cPickle as pickle 
import nltk
from nltk.corpus import brown

def trainBigram():
	bigramModel = nltk.NgramModel(2, brown.words())
	return bigramModel

def trainTrigram():
	trigramModel = nltk.NgramModel(3, brown.words())
	return trigramModel	