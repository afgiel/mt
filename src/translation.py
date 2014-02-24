import readDict
import POSTagger
import nGram

DEV_SET_FILE = "../data/dev.txt"
TEST_SET_FILE = "../data/test.txt"
DICTIONARY_PATH = "../data/"
DICTIONARY_FILE = "dictionary.txt"
N_GRAMS = 3



class Translator:
    def __init__(self):
        self.spanDict = readDict.read(DICTIONARY_PATH, DICTIONARY_FILE)
        # self.tagger = POSTagger.POSTagger()
        # self.lm = nGram.nGram(N_GRAMS)

    def translateSentence(self, sentence):
        t = []
        for word in sentence:
            if word not in self.spanDict:
                t.append(word)
            else:
                t.append(self.spanDict[word][0])
        return t

    def translateFile(self, fileName = DEV_SET_FILE):
        f = open(fileName)
        for line in f:
            s = line.split()
            t = self.translateSentence(s)
            print "Spanish sentence:"
            print " ".join(s)
            print "English translation"
            print " ".join(t)
            print
            print
        f.close()


def main():
  t = Translator()
  t.translateFile(DEV_SET_FILE)

if __name__ == "__main__":
    main()

