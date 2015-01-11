import pysam
import sys
import re
import subprocess
import os
from collections import defaultdict
from Bio import AlignIO

# reverse complement a sequence
complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
def revcomp(seq):
    reverse_complement = "".join(complement.get(base, base) for base in reversed(seq))
    return reverse_complement

# parse an LAshow read index string into a numeric ID
# the IDs are 1-based and contain commas
def lashow_idstr2idx(s):
    return int(s.replace(',', '')) - 1

# remove non-numeric characters from a string
def remove_nonnumeric(s):
    return re.sub("[^0-9]", "", s)

# parse an LAshow output file and build a map from a read index
# to the sequences that align to it
def parse_lashow(fn):
    fh = open(fn, 'r')
    
    out = defaultdict(list)

    for line in fh:

        fields = line.split()
        if len(fields) != 18:
            continue
       
        id1 = lashow_idstr2idx(fields[0])
        id2 = lashow_idstr2idx(fields[1])
        strand = fields[2]

        # 
        s = int(remove_nonnumeric(fields[8]))
        e = int(remove_nonnumeric(fields[9]))
    
        out[id1].append((id2, strand, s, e))
    return out

# write a fasta file for input into POA
def write_poa_input(overlaps, read_idx):
    fn = "poa.input.%d.fa" % (read_idx)
    fh = open(fn, "w")

    read_id1 = ref.references[read_idx]
    seq1 = ref.fetch(read_id1)
    fh.write(">%s\n%s\n" % ("poabaseread", seq1))

    n_reads = 0
    for o in overlaps[read_idx]:

        read_id2 = ref.references[o[0]]
        seq2 = ref.fetch(read_id2)

        # strand
        if o[1] == "c":
            seq2 = revcomp(seq2)

        # restrict to the part of the sequence that matches read1
        seq2 = seq2[o[2]:o[3]]

        fh.write(">%s\n%s\n" % (read_id2, seq2))
        n_reads += 1
    fh.close()
    return (fn, n_reads)

def clustal2consensus(fn):

    alignment = AlignIO.read(fn, "clustal")

    min_coverage = 3
    read_row = -1
    consensus_row = -1
    
    for (i, record) in enumerate(alignment):
        if record.id == 'poabaseread':
            read_row = i
        if record.id == 'CONSENS0':
            consensus_row = i

    if consensus_row == -1:
        return ""

    # Work out the first and last columns that contains
    # bases of the read we are correcting
    (first_col, last_col) = get_sequence_coords(alignment[read_row].seq)

    # trim the alignment
    for record in alignment:
        record.seq = record.seq[first_col:last_col+1]

    # Calculate a vector of depths along the consensus
    depths = [0] * len(alignment[read_row].seq)

    for record in alignment:
        (aln_first_col, aln_last_col) = get_sequence_coords(record.seq)
        for i in xrange(aln_first_col, aln_last_col):
            depths[i] += 1

    # Change the boundaries to only include high-depth bases
    while first_col != last_col:
        if depths[first_col] >= min_coverage:
            break
        first_col += 1

    while last_col != first_col:
        if depths[last_col] >= min_coverage:
            break
        last_col -= 1

    # Extract the consensus sequence
    consensus = str(alignment[consensus_row].seq[first_col:last_col])
    consensus = consensus.replace('-', '')

    return consensus

# Return the first and last column of the multiple alignment
# that contains a base for the given sequence row
def get_sequence_coords(seq):
    first_col = -1
    last_col = -1
    for (i, s) in enumerate(seq):
        if s != '-' and first_col == -1:
            first_col = i
        if s != '-':
            last_col = i
    return (first_col, last_col)

#
def run_poa_and_consensus(overlaps, read_idx):
    (in_fn, n_reads) = write_poa_input(overlaps, read_idx)
    out_fn = "clustal-%d.out" % (read_idx)
    cmd = "poa -read_fasta %s -clustal %s -hb poa-blosum80.mat" % (in_fn, out_fn)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    consensus =  clustal2consensus(out_fn)

    #os.remove(in_fn)
    #os.remove(out_fn)
    return (consensus, n_reads)

def run_lashow(name, start, end):
    
    out_fn = "lashow.%s-%s.out" % (start, end)
    out_fh = open(out_fn, 'w')
    cmd = "LAshow %s.las %s-%s" % (name, start, end)
    p = subprocess.Popen(cmd, shell=True, stdout=out_fh)
    p.wait()
    out_fh.close()
    return out_fn

# Args
name = sys.argv[1]
read_range = sys.argv[2]

# Open reference file
ref_fn = "%s.pp.fasta" % (name)
ref = pysam.Fastafile(ref_fn)

# Parse the range of read ids to correct
(start, end) = [ int(x) for x in read_range.split(':') ]

# Generate the LAshow file indicating overlaps
lashow_fn = run_lashow(name, start, end)

# Make a dictionary of overlaps
overlaps = parse_lashow(lashow_fn)

# Correct each read with POA
for read_idx in xrange(start, end):
    if read_idx == 4171:
        (seq, n_reads) = run_poa_and_consensus(overlaps, read_idx)

        if seq != "":
            print ">%d n_reads=%d\n%s" % (read_idx, n_reads, seq)

os.remove(lashow_fn)
