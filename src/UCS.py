from Queue import PriorityQueue as pqueue

def UCS(sentence, model):
	frontier = pqueue()
	for root in sentence[0]:
		node = [root]
		cost = model.score(node)
		frontier.put((cost, node))
	while(True):
		if frontier.empty():
			return None
		else:
			node = list(frontier.get()[1])
			if len(node) == len(sentence):
				return node, cost
			else:			
				index = len(node) 
				for nextWord in sentence[index]:
					newNode = node + [nextWord]
					cost = model.score(newNode)
					frontier.put((cost, newNode))