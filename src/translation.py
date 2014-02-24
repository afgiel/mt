import readDict
import POSTagger
import nGram
import re

DEV_SET_FILE = "../data/dev.txt"
TEST_SET_FILE = "../data/test.txt"
DICTIONARY_PATH = "../data/"
DICTIONARY_FILE = "dictionary.txt"
N_GRAMS = 3
END_PUNCTUATION = [".", "?", "!", ","]
WORD = 1
FRONT_QUOTE = 0
END_PUNC_I = 3
END_QUOTE = 2

class Translator:
    def __init__(self):
        self.spanDict = readDict.read(DICTIONARY_PATH, DICTIONARY_FILE)
        # self.tagger = POSTagger.POSTagger()
        # self.lm = nGram.nGram(N_GRAMS)

    def translateSentence(self, sentence):

        def getPunctuation(word):
            frontQuote = ""
            endQuote = ""
            endPunc = ""
            if len(word) > 1:
                if word[0] == '\"':
                    frontQuote = '\"'
                    word = word[1:]
                if word[len(word)-1] in END_PUNCTUATION:
                    endPunc = word[len(word)-1]
                    word = word[:-1]
                if word[len(word)-1] == "\"":
                    endQuote = '\"'
                    word = word[:-1]
            return frontQuote, word, endQuote, endPunc

        def assembleWord(word, punc, isCapitalized):
            if isCapitalized:
                word = word[0].upper() + word[1:]
            return punc[FRONT_QUOTE] + word + punc[END_QUOTE] + punc[END_PUNC_I]



        t = []
        for word in sentence:
            cleanWordTuple = getPunctuation(word)
            tWord = cleanWordTuple[WORD]
            isCapitalized = False
            if tWord[0].isupper():
                isCapitalized = True
                tWord = tWord[0].lower() + tWord[1:]
            if tWord not in self.spanDict:
                tWord = assembleWord(tWord, cleanWordTuple, isCapitalized)
            else:
                tWord = assembleWord(self.spanDict[tWord][0], cleanWordTuple, isCapitalized) 
            t.append(tWord)
        return t

    def translateFile(self, fileName = DEV_SET_FILE):
        f = open(fileName)
        for line in f:
            s = line.split()
            t = self.translateSentence(s)
            print "Spanish sentence:"
            print " ".join(s)
            print "English translation:"
            print " ".join(t)
            print
            print
        f.close()


def main():
  t = Translator()
  t.translateFile(DEV_SET_FILE)

if __name__ == "__main__":
    main()

