
def read(path, filename):
	d = dict()
	toRead = open(path+filename, r)
	for line in toRead:
		linePieces = line.split(':')
		f = linePieces[0]
		e = linePieces[1]
		e = e.split(',')
		d[f] = e
	return d 