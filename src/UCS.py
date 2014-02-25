from Queue import PriorityQueue as pqueue

def UCS(sentence, model):
	frontier = pqueue()
	for root in sentence[0]:
		node = list(root)
		cost = model.score(root)
		frontier.put((cost, root))
	while(True):
		if frontier.empty():
			return None
		else:
			node = list(frontier.get()[1])
			if len(node) == len(sentence):
				return node
			else:			
				index = len(node) 
				for nextWord in sentence[index]:
					newNode = node + [nextWord]
					cost = model.score(newNode)
					frontier.put((cost, newNode))