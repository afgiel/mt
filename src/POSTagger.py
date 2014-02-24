import os.path
import nltk
from nltk.corpus import cess_esp


class POSTagger:
	def __init__(self):
		training = []
		sents = cess_esp.tagged_sents()
		for i in range(len(sents)):
			training.append(sents[i])
		self.tagger = nltk.tag.hmm.HiddenMarkovModelTagger.train(training)

	def tag(self, sentence):
		return self.tagger.tag(sentence)