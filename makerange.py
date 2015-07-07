
import sys
from Bio import SeqIO

# nanocorrect is zero-based, exclusive endpoints
recs = len([rec for rec in SeqIO.parse(open(sys.argv[1]), "fasta")])
batch_size = 50
for n in xrange(0, recs, batch_size):
	if (n + batch_size) > recs:
		print "%d:%d" % (n, recs)
	else:
		print "%d:%d" % (n, n + batch_size)

