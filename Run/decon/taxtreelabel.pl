#!/usr/bin/perl -w
#
# This pscript reads in tha flat blast table with tax id in the last field
# and prints out the tax id path for each hit
#
#
# terra specific - for Aaron
#
# Usage: taxtreelabel.pl blast_file
#
# Ross Hall 2012


use strict;

if (@ARGV != 2) {
	print "Usage: taxtreelabel.pl blast_file head_id\n";
	exit(1);
}
	
my $blastfile = shift;
my $head_id = shift;

my $nodefile = "/home/nodes.dmp";
my $namefile = "/home/names.dmp";


open(NODEFILE,$nodefile) || &ErrorMessage("Cannot open file ".$nodefile);
my @nodelist = <NODEFILE>;

open(NAMEFILE,$namefile) || &ErrorMessage("Cannot open file ".$namefile);
my @namelist = <NAMEFILE>;

open(BFILE,$blastfile) || &ErrorMessage("Cannot open file ".$blastfile);

open(NOTINFILE,">not_in_tree.txt") || &ErrorMessage("Cannot open file not_in.txt");

open(INFILE,">in_tree.txt") || &ErrorMessage("Cannot open file in_tree.txt");

my %scihash;
foreach my $line (@namelist) {
	chomp($line);

	my @fa = split(/\|/,$line);
	my $key = $fa[0];
	my $name = $fa[1];
	$key =~ s/\s//g;
	$name =~ s/^\s+//g;
	$name =~ s/\s+$//g;
	if ($line =~ /scientific name/) {
		$scihash{$key} = $name;
	}	
}

my %parenthash;
my %rankhash;
my %parentnodes;
print STDERR  "reading nodes....\n";
foreach my $line (@nodelist) {
	chomp($line);
	my @fa = split(/\|/,$line);
	my $key = $fa[0];
	my $parent = $fa[1]; 
	$key =~ s/\s//g;
	$parent =~ s/\s//g;
	
	if (!exists($parentnodes{$parent})) {
		my %parentnode;
		$parentnode{'id'} = $parent;
		my @list = ();
		$parentnode{'children_list'} = \@list;
		$parentnodes{$parent} = \%parentnode;
	}	
	push(@{$parentnodes{$parent}->{'children_list'}},$key);	
			
	my $rank = $fa[2];
	$parenthash{$key} = $parent; 
	$rank =~ s/\s//g;
	$rankhash{$key} = $rank; 
}


my %subtreeDict;
&buildDict($parentnodes{$head_id}->{'children_list'},\%subtreeDict);

my $last = "";

#
# Top hits only
#
#while (<BFILE>) {
#	my $line = $_;
#	chomp($line);
#	my @fa = split(/\t/,$line);
#	my $query = $fa[0];
#	
#	if ($query ne $last) {
#		my $btax = $fa[scalar(@fa)-1];
#		if ($btax =~ /TaxonNotFound/) {
#			print STDERR "$line\n";
#		} else {
#			if (exists($subtreeDict{$btax})) {
#				print "$line\t" . $scihash{$btax} . "\n";
#			}	
#		}
#	}
#	$last = $query;	
#} 

#
# All hits - output all hits not in the the head tree
#
while (<BFILE>) {
    my $line = $_;
    chomp($line);
    my @fa = split(/\t/,$line);
  
	my $btax = $fa[scalar(@fa)-1];
	if ($btax =~ /TaxonNotFound/) {
		print STDERR "$line\n";
	} else {
		# if this species is NOT in the head tree
		if (!exists($subtreeDict{$btax})) {
			if (exists($scihash{$btax})) {
				print NOTINFILE "$line\t" . $scihash{$btax} . "\n";
			} else {
				print NOTINFILE "$line\tNo name for Tax id\n";
			}			
		} else {
			print INFILE "$line\t" . $scihash{$btax} . "\n";
		}			  
    }

} 


	
sub ErrorMessage {
	my $msg = shift;
	print STDERR "Fatal error: $msg\n";
	exit(1);	
}	   		


sub buildDict {
	my $arrayptr = shift;
	my $dictptr = shift;
	
	if (@{$arrayptr} > 0) {
		foreach my $x (@{$arrayptr}) {
			$dictptr->{$x} = 1;
			# print $scihash{$x} . "\n";
			if (exists($parentnodes{$x}->{'children_list'})) {
				&buildDict($parentnodes{$x}->{'children_list'},$dictptr);
			}	
		}
	} 
}				

