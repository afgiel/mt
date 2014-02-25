import math, collections, copy
from nltk.corpus import brown

BACKOFF_COEFFICIENT = .9
DISCOUNT = .35
STRIP_CHARS = "<>.\",?!"

class KneserNeyModel:
    """Kneser-Ney Backoff language model - Implements the Kneser-Ney model
    with bigrams and backoffs to laplace unigram if the given bigram does
    not exist in the training corpus."""
    def __init__(self):
        """Initialize your data structures in the constructor."""
        self.bigramCounts = collections.defaultdict(lambda : 0)
        self.unigramCounts = collections.defaultdict(lambda : 1)
        self.continuationCounts = collections.defaultdict(lambda: 0)
        self.followingCounts = collections.defaultdict(lambda: 0)
        self.total = 1
        self.train(brown.sents())

    def train(self, corpus):
        """ Takes a corpus and trains your language model. 
            Compute any counts or other corpus statistics in this function.
        """  
        # TODO your code here
        # Tip: To get words from the corpus, try
        #    for sentence in corpus.corpus:
        #       for datum in sentence.data:  
        #         word = datum.word
        for sentence in corpus:
            previousWord = ""
            for word in sentence:
                word = word.strip(STRIP_CHARS)
                word = word.lower()
                currentWord = word
                self.unigramCounts[currentWord] += 1
                self.total += 1
                if previousWord != "":
                    bigram = (previousWord, currentWord)
                    if bigram not in self.bigramCounts:
                        self.continuationCounts[currentWord] += 1
                        self.followingCounts[previousWord] += 1
                    self.bigramCounts[bigram] += 1
                previousWord = currentWord
        self.total += len(self.unigramCounts)


    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the 
            sentence using your language model. Use whatever data you computed in train() here.
        """


        # TODO your code here
        score = 0.0 
        previousWord = ""
        newSentence = []
        for word in sentence:
            newSentence += word.split()
        for currentWord in sentence:
            currentWord = currentWord.strip(STRIP_CHARS)
            currentWord = currentWord.lower()
            if previousWord != "":
                bigram = (previousWord, currentWord)
                bigramCount = self.bigramCounts[bigram]
                if bigramCount > 0:
                    score += math.log(max(self.bigramCounts[bigram] - DISCOUNT, 0)*len(self.bigramCounts) + DISCOUNT*self.followingCounts[previousWord]*self.continuationCounts[currentWord])
                    # Subtraction by 1 removes the add one count from the laplace
                    # smoothing
                    score -= math.log((self.unigramCounts[previousWord] -1) * len(self.bigramCounts))
                else:
                    count = self.unigramCounts[currentWord]
                    score += math.log(count * BACKOFF_COEFFICIENT)
                    score -= math.log(self.total)
            previousWord = currentWord
        return -score







