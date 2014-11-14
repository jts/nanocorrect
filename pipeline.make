SHELL=/bin/bash -o pipefail

#
# A pipeline to run daligner on a set of reads
#

# Our target is the local alignments file that daligner generates
all: $(NAME).las

#
# Preprocess reads to format them for dazzler
#
$(NAME).pp.fasta: $(INPUT)
	./preprocess.pl $(INPUT) > $@

#
# Make the dazzler DB, split and dust it
#
$(NAME).db: $(NAME).pp.fasta
	fasta2DB $(NAME) $^
	DBsplit -s50 $(NAME)
	DBdust $(NAME)

#
# Generate the commands to run DAligner
#
HPCcommands.txt: $(NAME).db
	HPCdaligner -t5 -d $(NAME) > $@

#
# Run DAligner to generate the local alignments
#
$(NAME).1.las: HPCcommands.txt
	/bin/bash $^

#
# Cat the .las files together
#
$(NAME).las: $(NAME).1.las
	LAcat $(NAME) > $@
	rm $(NAME).*.las

#
#
#
clean:
	rm $(NAME).pp.fasta
	DBrm $(NAME)
	rm $(NAME)
