NOUN = "nc"
ADJ = "aq0"
VERB = "vmip3s0"

def preProcess(tags, words):
	for i in range(len(tags)):
		if tags[i] == NOUN and not i > len(tags)-3:
			if tags[i+2] == NOUN:
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
		elif tags[i] == NOUN and not i > len(tags)-2:
			if tags[i+1] == ADJ:
				newWords = words[:i]
				newTags = words[:i]
				newWords.append(words[i+1])
				newTags.append(tags[i+1])
				newWords.append(words[i])
				newTags.append(tags[i])
				newWords += words[i+2:]
				newTags += tags[i+2:]
				return preProcess(newTags, newWords)
		elif tags[i] == NOUN and not i > len(tags)-3:
			if tags[i+2] == ADJ and words[i+1] == 'm\xc3s':
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


