
import sys
from Bio import SeqIO

recs = len([rec for rec in SeqIO.parse(open(sys.argv[1]), "fasta")])

for n in xrange(0, recs, 50):
	if (n+50) > recs:
		print "%d:%d" % (n+1, recs)
	else:
		print "%d:%d" % (n+1, n+50)

