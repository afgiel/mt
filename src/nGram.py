import nltk
from nltk.corpus import brown

class nGram:
	def __init__(self, n):
		self.n = n
		self.model = nltk.NgramModel(n, brown.words())

	def logprob(self, word, context):
		return self.model.logprob(word, context)