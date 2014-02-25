import readDict
import POSTagger
import nGram
import re
import UCS
import KneserNeyModel
import string
import applyRules

DEV_SET_FILE = "../data/dev.txt"
TEST_SET_FILE = "../data/test.txt"
DICTIONARY_PATH = "../data/"
DICTIONARY_FILE = "dictionary.txt"
N_GRAMS = 3
END_PUNCTUATION = [".", "?", "!", ",", ":"]
WORD = 1
FRONT_QUOTE = 0
END_PUNC_I = 3
END_QUOTE = 2
IS_CAP = 4

class Translator:
    def __init__(self):
        self.spanDict = readDict.read(DICTIONARY_PATH, DICTIONARY_FILE)
        self.tagger = POSTagger.POSTagger()
        self.lm = KneserNeyModel.KneserNeyModel()

    def translateSentence(self, sentence):

        def cleanWord(word):
            isCapitalized = False
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
                if word[0].isupper():
                    isCapitalized = True
                    word = word[0].lower() + word[1:]
            return frontQuote, word, endQuote, endPunc, isCapitalized

        def assembleWords(wordList, cleanWordTuple):
            translations = []
            for word in wordList:
                if cleanWordTuple[IS_CAP]:
                    word = word[0].upper() + word[1:]
                translations.append(cleanWordTuple[FRONT_QUOTE] + word + cleanWordTuple[END_QUOTE] + cleanWordTuple[END_PUNC_I])
            return translations


        translations = []
        prepreProcessedSentence = []
        prepreProcessedTags = []

        for word in sentence:
            cleanWordTuple = cleanWord(word)
            toTranslate = cleanWordTuple[WORD]
            prepreProcessedSentence.append(toTranslate)

        prepreProcessedTagTuples = self.tagger.tag(prepreProcessedSentence)
        prepreProcessedTags = []
        for tagTuple in prepreProcessedTagTuples:
            prepreProcessedTags.append(tagTuple[1])
        preProcessedTags, preProcessedSentence = applyRules.preProcess(prepreProcessedTags, prepreProcessedSentence)

        for word in preProcessedSentence:
            cleanWordTuple = cleanWord(word)
            toTranslate = cleanWordTuple[WORD]
            transWords = []
            if toTranslate not in self.spanDict:
                transWords = assembleWords([toTranslate], cleanWordTuple)
            else:
                transWords = assembleWords(self.spanDict[toTranslate], cleanWordTuple) 
            translations.append(transWords)
        transSentence = UCS.UCS(translations, self.lm)

        postProcessedTags, postProcessedSentence = applyRules.postProcess(preProcessedTags, transSentence)

        return postProcessedSentence
 

    def translateFile(self, fileName = DEV_SET_FILE):
        def splitLines(line):
            splitLines = []
            firstSplit = string.replace(line, ",", ",***")
            secondSplit = string.replace(firstSplit, " y ", " y*** ")
            return secondSplit.split("***")


        f = open(fileName)
        for line in f:
            sourceSplits = splitLines(line)
            target = []
            for source in sourceSplits:
                target += self.translateSentence(source.split())
            print "Spanish sentence:"
            print line
            print "English translation:"
            print " ".join(target)
            print
            print
        f.close()


def main():
  t = Translator()
  t.translateFile(DEV_SET_FILE)

if __name__ == "__main__":
    main()

