import math, collections, copy
from nltk.corpus import brown

UNI_BACKOFF_COEFFICIENT = .9
BI_BACKOFF_COEFFICIENT = .95
DISCOUNT = .35
STRIP_CHARS = "<>.\",?! "

class KneserTrigramModel:
    """Kneser-Ney Backoff language model - Implements the Kneser-Ney model
    with bigrams and backoffs to laplace unigram if the given bigram does
    not exist in the training corpus."""
    def __init__(self):
        """Initialize your data structures in the constructor."""
        self.bigramCounts = collections.defaultdict(lambda : 0)
        self.trigramCounts = collections.defaultdict(lambda : 0)
        self.unigramCounts = collections.defaultdict(lambda : 1)
        self.continuationCounts = collections.defaultdict(lambda: 0)
        self.followingCounts = collections.defaultdict(lambda: 0)
        self.total = 1
        self.totalBigramCounts = 0
        print "Training Language Model..."
        self.train(brown.sents())
        print "--Training Complete--"

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
            prevWord = ""
            prevPrevWord = ""
            for word in sentence:
                word = word.strip(STRIP_CHARS)
                word = word.lower()
                currentWord = word
                self.unigramCounts[currentWord] += 1
                self.total += 1
                if prevWord != "":
                    if prevPrevWord != "":
                        trigram = (prevPrevWord, prevWord, currentWord)
                        if trigram not in self.trigramCounts:
                            self.continuationCounts[currentWord] += 1
                            self.followingCounts[(prevPrevWord, prevWord)] += 1
                        self.trigramCounts[trigram] += 1
                        self.bigramCounts[(prevWord, currentWord)] += 1
                        self.totalBigramCounts += 1
                    else:
                        self.bigramCounts[(prevWord, currentWord)] += 1
                        self.totalBigramCounts += 1
                        prevPrevWord = prevWord
                        prevWord = currentWord
                else:
                    prevWord = currentWord
        self.total += len(self.unigramCounts)


    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the 
            sentence using your language model. Use whatever data you computed in train() here.
        """


        # TODO your code here
        score = 0.0 
        prevWord = ""
        prevPrevWord = ""
        newSentence = []
        for word in sentence:
            newSentence += word.split()
        for currentWord in sentence:
            currentWord = currentWord.strip(STRIP_CHARS)
            currentWord = currentWord.lower()
            if prevWord != "":
                if prevPrevWord != "":
                    trigram = (prevPrevWord, prevWord, currentWord)
                    trigramCount = self.trigramCounts[trigram]
                    if trigramCount > 0:
                        score += math.log(max(self.trigramCounts[trigram] - DISCOUNT, 0)*len(self.trigramCounts) + DISCOUNT*self.followingCounts[(prevPrevWord, prevWord)]*self.continuationCounts[currentWord])
                        # Subtraction by 1 removes the add one count from the laplace
                        # smoothing
                        score -= math.log((self.bigramCounts[(prevPrevWord, prevWord)]) * len(self.trigramCounts))
                    elif self.bigramCounts[(prevWord, currentWord)] > 0:
                        score += math.log(self.bigramCounts[(prevWord, currentWord)]*BI_BACKOFF_COEFFICIENT)
                        score -= math.log(self.totalBigramCounts)
                    else:
                        count = self.unigramCounts[currentWord]
                        score += math.log(count * UNI_BACKOFF_COEFFICIENT)
                        score -= math.log(self.total)
                else:
                    prevPrevWord = prevWord
                    prevWord = currentWord
            else:
                prevWord = currentWord
        return -score
