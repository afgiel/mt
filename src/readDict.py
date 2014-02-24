
def read(path, filename):
	d = dict()
	toRead = open(path+filename, 'r')
	for line in toRead:
		if line[0] != '#':
			linePieces = line.split(':')
			f = linePieces[0]
			e = linePieces[1]
			e = e.split(',')
			e = [x.strip() for x in e]
			if f in d: print f
			d[f] = e
	return d 