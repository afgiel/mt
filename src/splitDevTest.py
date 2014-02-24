import random

corpus = open('../data/corpus.txt')
sentences = set()
for line in corpus:
	sentences.add(line)
corpus.close()

dev = random.sample(sentences, 10)
test = sentences.difference(set(dev))

devFile = open('../data/dev.txt', 'w+')
for line in dev:
	devFile.write(line + '\n')
devFile.close()

testFile = open('../data/test.txt', 'w+')
for line in test:
	testFile.write(line + '\n')
testFile.close()