import re
import GenderClassifier

NOUN = "nc"

def removeTags(sentence, tags):
	gc = GenderClassifier.GenderClassifier()
	for index, wordOptions in enumerate(sentence):
		needsChange = False
		for word in wordOptions:
			if len(re.findall('<IT>|<THEY>', word)) > 0:
				needsChange = True
		if needsChange:
			fixTag(index, sentence, tags, gc)

def fixTag(index, sentence, tags, gc):
	wordOptions = sentence[index]
	upperPrev = False
	nounPrev = False
	if index > 0:
		for word in sentence[index-1]:
			if tags[index] == NOUN:
				nounPrev = True
			for letter in word:
				if str.isupper(letter):
					upperPrev = True
	if upperPrev or nounPrev:
		for index, word in enumerate(wordOptions):
			word = re.sub('<IT> |<THEY> ', '', word)
			wordOptions[index] = word
		return
	else:
		male = hasMale(sentence, gc)
		female = hasFemale(sentence, gc) 
		if male:
			for index, word in enumerate(wordOptions):
				word = re.sub('<IT>', 'he', word)
				wordOptions[index] = word
			return
		elif female:
			for index, word in enumerate(wordOptions):
				word = re.sub('<IT>', 'she', word)
				wordOptions[index] = word
			return
		else:
			for index, word in enumerate(wordOptions):
				word = re.sub('<IT>', 'it', word)
				word = re.sub('<THEY>', 'they', word)
				wordOptions[index] = word
			return

def hasMale(sentence, gc):
	for wordOptions in sentence:
		for word in wordOptions:
			if gc.guessGender(word) == 'm':
				return True

def hasFemale(sentence, gc):
	for wordOptions in sentence:
		for word in wordOptions:
			if gc.guessGender(word) == 'f':
				return True				
