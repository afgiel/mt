import nltk
from nltk.corpus import brown

class nGram:
	def __init__(self, n):
		self.n = n
		print "training ngram"
		self.model = nltk.NgramModel(n, brown.words())

	def logprob(self, word, context):
		return self.model.logprob(word, context)

	def getBestPermutation(self, sentence):
		permutations = set()
		permutations.add(tuple(list()))
		permutations = self.createAllPermutations(permutations, sentence, 0)
		print permutations
		best = self.chooseBestPerm(permutations)
		return best

	def createAllPermutations(self, perms, sentence, index):
		if index == len(sentence):
			return perms
		else:
			newPerms = set()
			for perm in perms:
				if isinstance(sentence[index], list):
					for option in sentence[index]:
						newPerm = list(perm)
						newPerm.append(option)
						newPerms.add(tuple(newPerm))
				else:
					newPerm = list(perm)
					newPerm.append(sentence[index])
					newPerms.add(tuple(newPerm))
			return self.createAllPermutations(newPerms, sentence, index+1)

	def evaluatePerm(self, permutation):
		score = 0.
		for index, word in enumerate(permutation):
			context = permutation[max(0, index-self.n+1):index]					
			wordScore = self.logprob(word, context)
			print word
			print context
			print wordScore
			score += wordScore
		return score

	def chooseBestPerm(self, permutations):
		bestScore = float('Inf')
		bestPerm = None
		for perm in permutations:
			score = self.evaluatePerm(perm)
			if score < bestScore:
				bestScore = score
				bestPerm = perm
		return bestPerm