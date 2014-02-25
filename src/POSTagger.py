import nltk

class POSTagger:
	def __init__(self):
		print "Training POS tagger..."
		training = []
		sents = nltk.corpus.cess_esp.tagged_sents()
		for i in range(len(sents)):
			training.append(sents[i])
		self.tagger = nltk.tag.hmm.HiddenMarkovModelTagger.train(training)
		print "--Training complete--"



	def tag(self, sentence):
		return self.tagger.tag(sentence)