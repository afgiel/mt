import readDict
import POSTagger
import nGram
import re
import UCS
import KneserNeyModel
import string

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
NOUN = "nc"
ADJ = "aq0"
VERB = "vmip3s0"
DROP_WORDS = ['un', 'se', 'a']

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

        def preProcess(tags, words):
            for i in range(len(tags)):
                if tags[i][0:2] == NOUN and not i > len(tags)-3:
                    if tags[i+2][0:2] == NOUN:
                        if words[i+1] == 'de' or words[i+1] == 'del':
                            newWords = words[:i]
                            newTags = words[:i]
                            newWords.append(words[i+2])
                            newTags.append(tags[i+2])
                            newWords.append(words[i])
                            newTags.append(tags[i])
                            newWords += words[i+3:]
                            newTags += tags[i+3:]
                            return preProcess(newTags, newWords)
                elif tags[i][0:2] == NOUN and not i > len(tags)-2:
                    if tags[i+1][0:3] == ADJ:
                        newWords = words[:i]
                        newTags = words[:i]
                        newWords.append(words[i+1])
                        newTags.append(tags[i+1])
                        newWords.append(words[i])
                        newTags.append(tags[i])
                        newWords += words[i+2:]
                        newTags += tags[i+2:]
                        return preProcess(newTags, newWords)
                elif tags[i][0:2] == NOUN and not i > len(tags)-3:
                    if tags[i+2][0:3] == ADJ and words[i+1] == 'm\xc3s':
                        newWords = words[:i]
                        newTags = words[:i]
                        newWords.append('m\xc3s')
                        newTags.append(tags[i+1])
                        newWords.append(words[i+2])
                        newTags.append(tags[i+2])
                        newWords.append(words[i])
                        newTags.append(tags[i])
                        newWords += words[i+3:]
                        newTags += tags[i+3:]
                        return preProcess(newTags, newWords)
            return tags, words

        def postProcess(tags, words):
            for i in range(len(tags)):
                if words[i] == 'no' and not i > len(tags)-2:
                    if tags[i+1] == VERB:           
                        newWords = words[:i]
                        newTags = words[:i]
                        newWords.append('does not')
                        newTags.append(tags[i])
                        if words[i+1][len(words[i+1])-1] == 's':
                            newWords.append(words[i+1][:len(words[i+1])-1])
                        newTags.append(tags[i+1])
                        newWords += words[i+2:]
                        newTags += tags[i+2:]
                        return postProcess(newTags, newWords)
                elif words[i] == 'a' and not i > len(tags)-2:
                    if words[i+1][0] in 'aeiou':                
                        newWords = words[:i]
                        newTags = words[:i]
                        newWords.append('an')
                        newTags.append(tags[i])
                        newWords += words[i+1:]
                        newTags += tags[i+1:]
                        return postProcess(newTags, newWords)
            return tags, words

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
        preProcessedTags, preProcessedSentence = preProcess(prepreProcessedTags, prepreProcessedSentence)

        for word in preProcessedSentence:
            cleanWordTuple = cleanWord(word)
            toTranslate = cleanWordTuple[WORD]
            transWords = []
            if toTranslate not in self.spanDict:
                transWords = assembleWords([toTranslate], cleanWordTuple)
            else:
                if toTranslate in DROP_WORDS:
                    transWords = assembleWords(self.spanDict[toTranslate] + [''], cleanWordTuple) 
                else:    
                    transWords = assembleWords(self.spanDict[toTranslate], cleanWordTuple) 
            translations.append(transWords)
        transSentence = UCS.UCS(translations, self.lm)

        postProcessedTags, postProcessedSentence = postProcess(preProcessedTags, transSentence)

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

