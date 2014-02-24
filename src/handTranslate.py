corpusFile = open('../data/corpus.txt', 'r')
allWords = set()
for line in corpusFile:
	words = line.split(' ')
	words = [x.strip(',.') for x in words]
	for word in words: 
		if word != '':
			allWords.add(word)
corpusFile.close()

dictionaryFile = open('../data/dictionary.txt', 'a+')
for word in allWords:
	defs = raw_input(word + ' : ')
	if defs != '':
		dictionaryFile.write(word + ':' + defs + '\n')
dictionaryFile.close()