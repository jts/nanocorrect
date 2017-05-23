**This software is now deprecated, see [this blog post](http://simpsonlab.github.io/2016/02/25/deprecating-nanocorrect/) for details**

A prototype nanopore correction pipeline. It self-error-corrects OxfordNanopore data.

Dependencies:

* [daligner](https://github.com/thegenemyers/DALIGNER)
* [DAZZ_DB](https://github.com/thegenemyers/DAZZ_DB)
* [POA](http://sourceforge.net/projects/poamsa/)

These must all be on your $PATH.

Example:

First, build the DALIGNER database and compute alignments:

```./nanocorrect-overlap INPUT=reads.fasta NAME=nc```

INPUT is the path to your reads. 
The NAME variable is the prefix you want to use for the output files.

You can correct a range of reads using the python script:

```python nanocorrect.py nc 1000:1020 > corrected.fasta```

You can correct all reads using the python script:

```python nanocorrect.py nc all > corrected.fasta```

The first argument must be the same as the NAME variable above. 
The second is the indices of the reads (in the original fasta) that you want to correct.
