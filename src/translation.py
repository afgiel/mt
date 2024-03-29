import readDict
import POSTagger
import nGram
import re
import UCS
import KneserBigramModel
import KneserTrigramModel
import string
import applyRules
import sys
import implicitSubject

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
DROP_WORDS = ['un', 'se', 'a']

class Translator:
    def __init__(self):
        self.spanDict = readDict.read(DICTIONARY_PATH, DICTIONARY_FILE)
        self.tagger = POSTagger.POSTagger()
        self.lm = KneserBigramModel.KneserBigramModel()
        # self.lm = KneserTrigramModel.KneserTrigramModel()

    def translateFragment(self, fragment):

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
            return frontQuote, word, endQuote, endPunc, isCapitalized

        def assembleWords(wordList, cleanWordTuple):
            translations = []
            for word in wordList:
                if cleanWordTuple[IS_CAP]:
                    word = word[0].upper() + word[1:]
                translations.append(cleanWordTuple[FRONT_QUOTE] + word + cleanWordTuple[END_QUOTE] + cleanWordTuple[END_PUNC_I])
            return translations

        def getTranslatedSentence(sentenceToTranslate, posTags):
            translations = []
            for word in sentenceToTranslate:
                cleanWordTuple = cleanWord(word)
                toTranslate = cleanWordTuple[WORD]
                transWords = []
                if toTranslate.lower() not in self.spanDict:
                    transWords = assembleWords([toTranslate.lower()], cleanWordTuple)
                else:
                    if toTranslate in DROP_WORDS:
                        transWords = assembleWords(self.spanDict[toTranslate.lower()] + [''], cleanWordTuple) 
                    else:
                        transWords = assembleWords(self.spanDict[toTranslate.lower()], cleanWordTuple) 
                translations.append(transWords)

            pTags = []
            getSentenceOptions(posTags, pTags)
            if type(pTags[0]) == type(list()):
                pTags = pTags[0]
            implicitSubject.removeTags(translations, pTags)
            transSentence, transCost = UCS.UCS(translations, self.lm)
            return transSentence, transCost

        def getSentenceOptions(tupledSentencesToTranslate, sentenceOptions):
            for tupledSentence in tupledSentencesToTranslate:
                if isinstance(tupledSentence, tuple) == False:
                    sentenceOptions.append(tupledSentence)
                else:
                    getSentenceOptions(tupledSentence, sentenceOptions)


        prepreProcessedSentence = []
        prepreProcessedTags = []

        for word in fragment:
            prepreProcessedSentence.append(word)

        prepreProcessedTagTuples = self.tagger.tag(prepreProcessedSentence)
        prepreProcessedTags = []
        for tagTuple in prepreProcessedTagTuples:
            prepreProcessedTags.append(tagTuple[1])
        preProcessedTags, preProcessedSentence = applyRules.preProcess(prepreProcessedTags, prepreProcessedSentence)

        transSentence = ""
        if isinstance(preProcessedSentence, tuple):
            lowestCost = sys.maxint
            sentenceOptions = []
            getSentenceOptions(preProcessedSentence, sentenceOptions)
            for sentenceOption in sentenceOptions:
                transSentenceOption, transCost = getTranslatedSentence(sentenceOption, preProcessedTags)
                if transCost < lowestCost:
                    transSentence = transSentenceOption
        else:
            transSentence, transCost = getTranslatedSentence(preProcessedSentence, preProcessedTags)

        postProcessedTags, postProcessedSentence = applyRules.postProcess(preProcessedTags, transSentence)

        return postProcessedSentence
 

    def translateFile(self, fileName = DEV_SET_FILE):
        def splitLines(line):
            splitLines = []
            firstSplit = string.replace(line, ",", ",***")
            secondSplit = string.replace(firstSplit, " y ", " y*** ")
            return secondSplit.split("***")


        with open(fileName) as f:
            for line in f:
                sourceSplits = splitLines(line)
                target = []
                for source in sourceSplits:
                    target += self.translateFragment(source.split())
                print "Spanish sentence:"
                print line
                print "English translation:"
                print " ".join([word for word in target if word != ""])
                print
                print


def main():
  t = Translator()
  t.translateFile(DEV_SET_FILE)

if __name__ == "__main__":
    main()

