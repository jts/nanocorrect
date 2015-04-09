#! /usr/bin/perl
#
# Fake pacbio read names
#
use strict;
use Bio::Perl;
use Getopt::Long;

my $inFile  = Bio::SeqIO->new(-file => $ARGV[0], '-format' => 'Fasta');
my $outFile = Bio::SeqIO->new(-fh => \*STDOUT, '-format' => 'Fasta');
my $id = 0;

while(my $seq = $inFile->next_seq())
{
    my $randpore = rand() % 512;
    #>SK1.m140219_055344_00127_c100584712550000001823103604281493_s1_p0/54494/0_17531
    my $header = sprintf("m000000_000000_00000_c1898213712391273/%d/%d_%d", $id++, 0, $seq->length);
    $seq->display_id($header);
    $outFile->write_seq($seq);
}
